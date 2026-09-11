from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.utility.cloudnery import upload_image
from app.utility.jwt_support import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.routes.file_check import file_check

router = APIRouter()
security = HTTPBearer()

# ── Admin check ──
def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    if payload["role"] not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    return payload
  
# ── Upload endpoint for product ──
@router.post("/upload/image")
async def upload_product_image(
    file: UploadFile = File(...),
    admin = Depends(get_current_admin)
):
    
    file_bytes = await file_check(file)
    if not file_bytes:
        raise HTTPException(status_code= 400, detail="ya file nahi le sakte ")
    
    # 3. Cloudinary pe upload
    image_url = upload_image(file_bytes, folder="voltmart/products")
    
    return {"image_url": image_url}


# image uplode end point for signup
@router.post("/upload/profile-image")
async def upload_profile_image(file: UploadFile= File(...)):
    
    file_bytes = await file_check(file)
    if not file_bytes:
        raise HTTPException(status_code= 400, detail="ya file nahi le sakte ")
    
    # 3. Cloudinary pe upload
    image_url = upload_image(file_bytes, folder="voltmart/profile-images")
    
    return {"image_url": image_url}
    
    
    
        
