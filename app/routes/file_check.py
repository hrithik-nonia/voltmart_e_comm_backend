from fastapi import HTTPException

async def file_check(file):
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
      
  return file_bytes