import os
import io
import json
import uuid
import logging
import requests
from typing import Optional, Dict, Any, Tuple
import google.generativeai as genai


logger = logging.getLogger(__name__)

# Fallback image service based on keywords
def get_fallback_image(keyword: str) -> str:
    return f"https://loremflickr.com/1080/1080/{keyword.replace(' ', ',')}"

async def generate_ai_content(
    topic: str,
    generate_image: bool,
    brand_profile: Dict[str, Any],
    ai_settings: Dict[str, Any]
) -> Tuple[str, list, Optional[str], Optional[str]]:
    """
    Yapay zeka ile metin, hashtag ve görsel oluşturur.
    Returns: (content_text, hashtags_list, media_url, media_key)
    """
    provider = ai_settings.get("provider", "gemini")
    api_key = ai_settings.get("api_key")
    
    if not api_key:
        raise ValueError("AI API Key bulunamadı. Lütfen ayarlardan API Key ekleyin.")

    brand_name = brand_profile.get("brand_name", "")
    tone = brand_profile.get("tone", "Profesyonel")
    target_audience = brand_profile.get("target_audience", "Genel izleyici")
    keywords = brand_profile.get("keywords", [])
    
    prompt = f"""
    Aşağıdaki marka profili ve konu için bir sosyal medya gönderisi hazırla:
    
    Marka Adı: {brand_name}
    Marka Tonu: {tone}
    Hedef Kitle: {target_audience}
    Anahtar Kelimeler: {', '.join(keywords)}
    
    Konu: {topic}
    
    Lütfen yanıtını JSON formatında ver. Aşağıdaki yapıyı kullan:
    {{
        "content": "Gönderi metni buraya gelecek...",
        "hashtags": ["hashtag1", "hashtag2"],
        "image_prompt": "Görsel üretimi için ingilizce ve detaylı bir prompt"
    }}
    """

    content = ""
    hashtags = []
    image_prompt = topic

    try:
        if provider.lower() == "gemini":
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(ai_settings.get("model_name", "gemini-2.5-flash"))
            response = model.generate_content(prompt)
            text_response = response.text
            
            # JSON kısmını temizle
            if "```json" in text_response:
                text_response = text_response.split("```json")[1].split("```")[0].strip()
            elif "```" in text_response:
                text_response = text_response.split("```")[1].strip()
                
            try:
                data = json.loads(text_response)
                content = data.get("content", "")
                hashtags = data.get("hashtags", [])
                image_prompt = data.get("image_prompt", topic)
            except json.JSONDecodeError:
                content = text_response
                hashtags = ["AI", "Content"]
        
        elif provider.lower() == "openai":
            # pyrefly: ignore [missing-import]
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=ai_settings.get("model_name", "gpt-4o"),
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            data = json.loads(response.choices[0].message.content)
            content = data.get("content", "")
            hashtags = data.get("hashtags", [])
            image_prompt = data.get("image_prompt", topic)
        
        else:
            raise ValueError(f"Desteklenmeyen AI sağlayıcısı: {provider}")
            
    except Exception as e:
        logger.error(f"Metin üretimi hatası: {e}")
        raise ValueError(f"İçerik üretilirken hata oluştu: {str(e)}")

    media_url = None
    media_key = None
    
    # Görsel üretimi mock (Gemini resmi olarak henüz image generation sdk'da stabil desteklemiyor)
    # Gerçek uygulamada DALL-E, Midjourney vb. bağlanabilir.
    if generate_image:
        try:
            # Şimdilik Unsplash'ten rastgele görsel çekelim veya DALL-E kullanalım
            if provider.lower() == "openai":
                # pyrefly: ignore [missing-import]
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                img_response = client.images.generate(
                    model="dall-e-3",
                    prompt=image_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                media_url = img_response.data[0].url
                
                # İstersen MinIO'ya indirebilirsin
                # Ancak URL doğrudan frontend'e dönülebilir
                
            else:
                # Gemini için placeholder görsel dönüyoruz (veya kelimeye göre arama)
                search_word = hashtags[0] if hashtags else "technology"
                search_word = search_word.replace("#", "")
                media_url = f"https://loremflickr.com/1080/1080/{search_word}"
                
        except Exception as e:
            logger.error(f"Görsel üretimi hatası: {e}")
            # Hata olsa da content dönsün
            pass

    return content, hashtags, media_url, media_key

async def analyze_brand_file(file_content: bytes, filename: str, ai_settings: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dosya içeriğini okuyup yapay zeka ile analiz eder ve marka kimliği JSON'ı döner.
    """
    provider = ai_settings.get("provider", "gemini")
    api_key = ai_settings.get("api_key")
    
    if not api_key:
        raise ValueError("AI API Key bulunamadı. Lütfen ayarlardan API Key ekleyin.")

    # 1. Metni Çıkar
    text = ""
    ext = filename.lower().split('.')[-1] if '.' in filename else ""
    
    try:
        if ext == "pdf":
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(file_content))
            for page in reader.pages:
                text += page.extract_text() + "\n"
        elif ext in ["docx", "doc"]:
            import docx
            doc = docx.Document(io.BytesIO(file_content))
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif ext == "txt":
            text = file_content.decode('utf-8')
        else:
            raise ValueError(f"Desteklenmeyen dosya formatı: {ext}")
            
    except Exception as e:
        logger.error(f"Dosya okuma hatası: {e}")
        raise ValueError(f"Dosya okunurken bir hata oluştu: {str(e)}")

    if not text.strip():
        raise ValueError("Dosya içi boş veya okunabilir metin bulunamadı.")

    # 2. AI Prompt
    prompt = f"""
    Aşağıdaki döküman bir şirketin veya kişinin 'Marka Kimliği (Brand Identity)' belgesidir.
    Lütfen metni analiz et ve aşağıdaki bilgileri çıkararak SADECE JSON formatında döndür.

    Çıkarılacak alanlar:
    - "brand_name": Markanın veya kişinin adı (bulunamazsa boş bırak)
    - "tone": Markanın dili/tonu (örn: Profesyonel, Eğlenceli, Kurumsal vs.)
    - "target_audience": Hedef kitle özeti (1-2 cümle)
    - "keywords": Markayı veya içeriği anlatan 5-10 adet anahtar kelime (liste formatında)

    Döküman Metni:
    {text[:8000]}  # İlk 8000 karakteri analiz et (Token limiti için)

    Yanıtını sadece JSON olarak ver:
    {{
        "brand_name": "...",
        "tone": "...",
        "target_audience": "...",
        "keywords": ["...", "..."]
    }}
    """

    # 3. AI Çağrısı
    result = {
        "brand_name": "",
        "tone": "",
        "target_audience": "",
        "keywords": []
    }

    try:
        if provider.lower() == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(ai_settings.get("model_name", "gemini-2.5-flash"))
            response = model.generate_content(prompt)
            text_response = response.text
            
            # JSON kısmını temizle
            if "```json" in text_response:
                text_response = text_response.split("```json")[1].split("```")[0].strip()
            elif "```" in text_response:
                text_response = text_response.split("```")[1].strip()
                
            data = json.loads(text_response)
            result.update(data)
            
        elif provider.lower() == "openai":
            # pyrefly: ignore [missing-import]
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=ai_settings.get("model_name", "gpt-4o"),
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            data = json.loads(response.choices[0].message.content)
            result.update(data)
            
        else:
            raise ValueError(f"Desteklenmeyen AI sağlayıcısı: {provider}")
            
    except Exception as e:
        logger.error(f"Marka analizi hatası: {e}")
        raise ValueError(f"Marka dosyası analiz edilirken hata oluştu: {str(e)}")

    return result

async def translate_content(content: str, hashtags: list, target_language: str, ai_settings: Dict[str, Any]) -> Tuple[str, list]:
    """
    Gönderi metnini ve hashtagleri hedef dile çevirir.
    """
    provider = ai_settings.get("provider", "gemini")
    api_key = ai_settings.get("api_key")
    
    if not api_key:
        raise ValueError("AI API Key bulunamadı. Lütfen ayarlardan API Key ekleyin.")
        
    prompt = f"""
    Aşağıdaki sosyal medya gönderisini ve hashtagleri SADECE {target_language} diline çevir.
    Markanın tonunu ve orijinal mesajın hissiyatını koru.
    
    Orijinal Metin:
    {content}
    
    Orijinal Hashtagler:
    {', '.join(hashtags)}
    
    Yanıtını aşağıdaki gibi SADECE JSON formatında ver:
    {{
        "content": "Çevrilmiş metin...",
        "hashtags": ["çevrilmiş_hashtag1", "çevrilmiş_hashtag2"]
    }}
    """
    
    translated_content = content
    translated_hashtags = hashtags
    
    try:
        if provider.lower() == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(ai_settings.get("model_name", "gemini-2.5-flash"))
            response = model.generate_content(prompt)
            text_response = response.text
            
            if "```json" in text_response:
                text_response = text_response.split("```json")[1].split("```")[0].strip()
            elif "```" in text_response:
                text_response = text_response.split("```")[1].strip()
                
            data = json.loads(text_response)
            translated_content = data.get("content", content)
            translated_hashtags = data.get("hashtags", hashtags)
            
        elif provider.lower() == "openai":
            # pyrefly: ignore [missing-import]
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=ai_settings.get("model_name", "gpt-4o"),
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            data = json.loads(response.choices[0].message.content)
            translated_content = data.get("content", content)
            translated_hashtags = data.get("hashtags", hashtags)
            
        else:
            raise ValueError(f"Desteklenmeyen AI sağlayıcısı: {provider}")
            
    except Exception as e:
        logger.error(f"Çeviri hatası: {e}")
        # Hata durumunda orijinal metni dön
        pass
        
    return translated_content, translated_hashtags
