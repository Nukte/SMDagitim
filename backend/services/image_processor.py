"""
Görsel işleme servisi.
Görselleri belirtilen en-boy oranlarına (aspect ratio) göre yeniden boyutlandırır (blur padding).
"""
import io
import httpx
import logging
from PIL import Image, ImageFilter

logger = logging.getLogger(__name__)

def parse_aspect_ratio(ratio_str: str) -> float:
    """'4:5', '16:9', '1.91:1' gibi string formatındaki oranı float'a çevirir."""
    try:
        parts = ratio_str.split(':')
        if len(parts) == 2:
            return float(parts[0]) / float(parts[1])
        return float(ratio_str)
    except Exception as e:
        logger.error(f"Aspect ratio parse hatası ({ratio_str}): {e}")
        return 1.0 # Default fallback

async def adapt_image_for_platform(image_url: str, target_ratio_str: str) -> tuple[bytes, str]:
    """
    Görseli MinIO'dan indirir, bulanık arka plan (blur padding) yöntemiyle 
    hedef en-boy oranına uydurur ve byte olarak döndürür.
    
    Returns: (image_bytes, content_type)
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(image_url)
            if resp.status_code != 200:
                raise Exception(f"Görsel indirilemedi: {image_url}")
            image_data = resp.content

        # Pillow ile aç
        img = Image.open(io.BytesIO(image_data))
        
        # Orijinal boyutlar
        orig_w, orig_h = img.size
        orig_ratio = orig_w / orig_h
        
        # Hedef oran
        target_ratio = parse_aspect_ratio(target_ratio_str)
        
        # Eğer oran çok yakınsa işlem yapmaya gerek yok (%2 tölerans)
        if abs(orig_ratio - target_ratio) < 0.02:
            logger.info("Orijinal oran hedefe çok yakın, işlem yapılmadı.")
            # Convert to RGB to be safe if RGBA and saving as JPEG
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                bg = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    bg.paste(img, mask=img.split()[3])
                else:
                    bg.paste(img)
                img = bg
            
            output = io.BytesIO()
            img.save(output, format="JPEG", quality=90)
            return output.getvalue(), "image/jpeg"

        # Yeni boyutları hesapla (çözünürlüğü çok düşürmemek için büyük kenarı baz al)
        if target_ratio > orig_ratio:
            # Hedef daha yatay, genişliği artır, yüksekliği sabit tut
            target_h = orig_h
            target_w = int(orig_h * target_ratio)
        else:
            # Hedef daha dikey, yüksekliği artır, genişliği sabit tut
            target_w = orig_w
            target_h = int(orig_w / target_ratio)
            
        logger.info(f"Yeniden boyutlandırma: {orig_w}x{orig_h} -> {target_w}x{target_h} ({target_ratio_str})")

        # 1. Arka planı oluştur (Bulanık)
        # Orijinal resmi hedef boyuta kaplayacak şekilde (cover) büyüt/küçült
        bg_img = img.copy()
        
        # Cover resize
        bg_orig_ratio = bg_img.size[0] / bg_img.size[1]
        if target_ratio > bg_orig_ratio:
            # Genişliğe göre uydur, yüksekliği kırp
            new_bg_w = target_w
            new_bg_h = int(target_w / bg_orig_ratio)
        else:
            # Yüksekliğe göre uydur, genişliği kırp
            new_bg_h = target_h
            new_bg_w = int(target_h * bg_orig_ratio)
            
        bg_img = bg_img.resize((new_bg_w, new_bg_h), Image.Resampling.LANCZOS)
        
        # Center crop
        left = (bg_img.size[0] - target_w) / 2
        top = (bg_img.size[1] - target_h) / 2
        right = (bg_img.size[0] + target_w) / 2
        bottom = (bg_img.size[1] + target_h) / 2
        bg_img = bg_img.crop((left, top, right, bottom))
        
        # Blur uygula (şiddetli bulanıklık)
        bg_img = bg_img.filter(ImageFilter.GaussianBlur(radius=30))
        
        # Parlaklığı biraz düşür ki ana resim öne çıksın
        bg_img = bg_img.point(lambda p: p * 0.7)

        # 2. Ön planı (orijinal resim) hedef boyuta sığacak şekilde küçült (fit)
        fg_img = img.copy()
        fg_img.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
        
        # Eğer fg_img RGBA ise (saydamlık varsa)
        if fg_img.mode == 'RGBA':
            mask = fg_img.split()[3]
            paste_x = (target_w - fg_img.size[0]) // 2
            paste_y = (target_h - fg_img.size[1]) // 2
            bg_img.paste(fg_img, (paste_x, paste_y), mask=mask)
        else:
            paste_x = (target_w - fg_img.size[0]) // 2
            paste_y = (target_h - fg_img.size[1]) // 2
            bg_img.paste(fg_img, (paste_x, paste_y))

        # Sonucu kaydet
        if bg_img.mode in ('RGBA', 'P'):
            bg_img = bg_img.convert('RGB')
            
        output = io.BytesIO()
        bg_img.save(output, format="JPEG", quality=90)
        
        return output.getvalue(), "image/jpeg"
        
    except Exception as e:
        logger.error(f"Görsel işleme hatası: {e}")
        raise e
