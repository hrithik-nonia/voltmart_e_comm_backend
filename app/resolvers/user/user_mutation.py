import strawberry
from app.database import temp_user, users_collection
from app.utility.auth_support import auth_support
from app.utility.jwt_support import create_token
from datetime import datetime, timedelta, timezone
from app.utility.otp_service import generate_otp, send_otp_email
from app.utility.roles import Role
from app.utility.auth_model import UserData, AuthPayload



# ── Mutation ──────────────────────────────
@strawberry.type
class UserMutation:
  
  # create user 
  @strawberry.mutation
  async def sign_up(self,name:str, email: str, password: str ,image_url : str)-> bool:
    # find user
    user = await users_collection.find_one({"email": email})
    if user:
        raise Exception("Tera Palhe Se Account Hai")
      
    # temp data base me user check kiya
    user_in_temp_db= await temp_user.find_one({"data.email": email})
    if user_in_temp_db:
      raise Exception("Otp Send Kar Diya Hai Usse Fill Karo")
    
    # password hashing
    hashed_password = auth_support.hashed_pass(password)
    
    # generate otp
    otp = generate_otp()
    
    # send otp
    await send_otp_email(email, otp)
    
    # create time
    now = datetime.now(timezone.utc)
    
    user = {
        "data": {
            "name":name,
            "email": email,
            "password": hashed_password,
            "otp": otp,
            "role": Role.USER.value,
            "image_url": image_url
        },
        "created_at": now,
        "expires_at": now + timedelta(minutes=5)
    }
    
    await temp_user.insert_one(user)
    return True
  
  
  # otp verify
  @strawberry.mutation
  async def otp_verify(self,email: str, otp: str )-> bool:
    # find user
    user = await temp_user.find_one({"data.email":email})
    
    if not user:
      raise Exception("Otp Expire Ho Gya")
    
    if user["data"]["otp"] != otp:
      raise Exception("Otp Galat Hai")
    
    # permanent user banao
    new_user = {
        "name": user["data"]["name"],
        "email": user["data"]["email"],
        "password": user["data"]["password"],
        "role": user["data"]["role"],
        "image": user["data"]["image_url"],
        "is_active": True,
        "created_at": datetime.now(timezone.utc)
    }
    
    # users_collection mein save karo
    await users_collection.insert_one(new_user)
    
    # temp_user se delete karo
    await temp_user.delete_one({"data.email": email})
    
    return True
    
    
  # user login
  @strawberry.mutation
  async def user_login(self, email: str, password: str)-> AuthPayload:
    user = await users_collection.find_one({"email": email})
    if not user:
      raise Exception("User Not Found")
    
    # 2. Password verify karo
    is_valid = auth_support.verify_pass(password, user["password"])
    if not is_valid:
      raise Exception("Email ya password galat hai")
    
    # 3. Active check
    if not user.get("is_active", True):
        raise Exception("Account disabled hai")
      
    # 4. Token banao
    token = create_token(str(user["_id"]), user["role"])
    
    # 5. UserData object banao ✅
    user_data = UserData(
      id=str(user["_id"]),        # ← ObjectId → string
      name=user["name"],
      email=user["email"],
      role=user["role"],
      image=user.get("image")     # ← None bhi ho sakta hai
    )

    return AuthPayload(
        token=token,
        message="Login successful",
        user= user_data
    )
    
    
       
    
  
  
  
  
  
    
    
      
    