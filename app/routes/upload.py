from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.utility.cloudnery import upload_image
from app.routes.file_check import file_check
from app.routes.get_current_user_for_rest import get_current_admin

router = APIRouter()

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
    
    
    
        
