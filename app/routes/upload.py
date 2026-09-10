from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.utility.cloudnery import upload_image
from app.utility.jwt_support import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()

# ── Admin check ──
def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    if payload["role"] not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    return payload
  
# ── Upload endpoint ──
@router.post("/upload/image")
async def upload_product_image(
    file: UploadFile = File(...),
    admin = Depends(get_current_admin)
):
    # 1. File type check
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Sirf JPG, PNG, WEBP allowed hai"
        )
      
    # 2. File size check — 5MB max
    file_bytes = await file.read()
    if len(file_bytes) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File 5MB se badi nahi honi chahiye"
        )
        
    # 3. Cloudinary pe upload
    image_url = upload_image(file_bytes, folder="voltmart/products")
    
    return {"image_url": image_url}
        
