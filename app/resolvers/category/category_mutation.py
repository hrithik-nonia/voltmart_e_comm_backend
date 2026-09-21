import strawberry
from strawberry.types import Info
from app.resolvers.category.category_type import CreateCategory, CreateCategoryResponse
from app.utility.auth_support import auth_support
from app.database import users_collection, category_collection
from bson import ObjectId
from app.utility.helper_functions import plural_to_singular


@strawberry.type
class CategoryMutation:
  
  @strawberry.mutation
  async def create_category(self, info: Info, input: CreateCategory) -> CreateCategoryResponse:

      user_id = auth_support.get_user_from_info(info)
      if not user_id:
          raise Exception("Token Missing")

      get_admin = await users_collection.find_one({"_id": ObjectId(user_id)})

      if get_admin["role"] not in ["admin", "superadmin"]:
          raise Exception("Tu Admin Nahi Hai")
        
      # icon
      icon = plural_to_singular(input.name)
      
      # slug
      slug = input.name.lower()

      # Duplicate check
      existing = await category_collection.find_one({"slug": slug})
      if existing:
          raise Exception("Yeh category pehle se hai")

      # Save karo
      await category_collection.insert_one({
          "name": input.name,
          "description": input.description,
          "is_active": input.is_active,
          "slug": slug,
          "icon": icon
      })

      return CreateCategoryResponse(message=f"{input.name} Category ban gayi ✅")
    
    
    
    
    
    