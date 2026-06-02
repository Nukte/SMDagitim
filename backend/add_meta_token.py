import requests
from database import SessionLocal
from models.db_models import OAuthToken
from config import get_settings

db = SessionLocal()
settings = get_settings()

ACCESS_TOKEN = settings.META_ACCESS_TOKEN

if not ACCESS_TOKEN:
    print("Error: META_ACCESS_TOKEN is not set in environment or config.")
    exit(1)

res = requests.get("https://graph.facebook.com/v19.0/me/accounts", params={"access_token": ACCESS_TOKEN})
data = res.json()
print("Pages Response:", data)

if "data" in data:
    for page in data["data"]:
        page_token = page.get("access_token")
        page_id = page.get("id")
        page_name = page.get("name")
        
        # Facebook Page
        fb_token = db.query(OAuthToken).filter(OAuthToken.account_id == page_id).first()
        if not fb_token:
            fb_token = OAuthToken(platform="facebook", account_id=page_id, account_name=page_name, access_token=page_token)
            db.add(fb_token)
            print(f"Added FB Page: {page_name}")
        else:
            fb_token.access_token = page_token
            print(f"Updated FB Page: {page_name}")
            
        # Instagram Account
        if page_token:
            ig_res = requests.get(f"https://graph.facebook.com/v19.0/{page_id}", params={"fields": "instagram_business_account", "access_token": page_token})
            ig_data = ig_res.json()
            
            if "instagram_business_account" in ig_data and ig_data["instagram_business_account"]:
                ig_id = ig_data["instagram_business_account"]["id"]
                ig_info_res = requests.get(f"https://graph.facebook.com/v19.0/{ig_id}", params={"fields": "username", "access_token": page_token})
                ig_name = ig_info_res.json().get("username", f"IG-{ig_id}")
                
                ig_token = db.query(OAuthToken).filter(OAuthToken.account_id == ig_id).first()
                if not ig_token:
                    ig_token = OAuthToken(platform="instagram", account_id=ig_id, account_name=ig_name, access_token=page_token)
                    db.add(ig_token)
                    print(f"Added IG Account: {ig_name}")
                else:
                    ig_token.access_token = page_token
                    print(f"Updated IG Account: {ig_name}")

db.commit()
db.close()
print("Done")
