import datetime
import os
import asyncio

from app.utility.auth_support import auth_support
from app.database import admin_collection
from app.utility.cloudnery import upload_image
from app.schema import Role


async def cerate_first_admin():
  email = "hrithiknonia66@gmail.com"
  # ── 1. Pehle check karo admin hai ya nahi ──
  existing = await admin_collection.find_one({"email": email})
  if existing:
    print("⚠️  Admin already exists!")
    return
  
  # ── 2. Image upload karo (optional) ──
  image_url = None
  image_path = "app/scripts/profile_img.jpeg"

  if os.path.exists(image_path):
    print("📸 Image upload ho rahi hai Cloudinary pe...")
    with open(image_path, "rb") as f:
      file_bytes = f.read()
    image_url = upload_image(file_bytes, folder="voltmart/admins")
    print(f"✅ Image uploaded: {image_url}")
  else:
    print("⚠️  Image nahi mili — admin bina photo ke banega")
    
  # ── 3. Password hash karo ──
  password = "Admin@123"
  hashed_pass = auth_support.hashed_pass(password)
  
  # ── 4. Admin document banao ──
  admin = {
    "name": "Hritik Nonia",
    "email": email,
    "password": hashed_pass,
    "role": Role.ADMIN.value,
    "image": image_url,       
    "is_active": True,
    "created_at": datetime.datetime.now(datetime.timezone.utc)
  }
  
  # ── 5. MongoDB mein insert karo ──
  result = await admin_collection.insert_one(admin)

  print(f"\n✅ Admin successfully created!")
  print(f"🆔 ID:       {result.inserted_id}")
  print(f"📧 Email:    admin@voltmart.com")
  print(f"🔑 Password: Admin@123")
  print(f"🖼️  Image:    {image_url or 'No image'}")
  print(f"\n⚠️  Production mein password zaroor change karna!")
  
asyncio.run(cerate_first_admin())