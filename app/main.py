from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter
from app.schema import schema
from app.database import db
from fastapi.middleware.cors import CORSMiddleware
from app.routes.upload import router as upload_router
from app.routes.export import router as export_router

app = FastAPI(title="VoltMart API")

# cross origin allow
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite ka port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# request setup for verify token
async def get_context(request: Request):
    return {"request": request} 

# rest routes
app.include_router(upload_router)
app.include_router(export_router)


# GraphQL endpoint
graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {"message": "VoltMart API is running ✅"}

@app.on_event("startup")
async def startup():
    # MongoDB connection check
    try:
        await db.command("ping")
        print("✅ MongoDB connected successfully")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        
    # TTL index — 5 minute baad auto delete
    await db.temp_user.create_index(
        "expires_at",
        expireAfterSeconds=0
    )
    print("✅ TTL index created")
    
    # Email index — fast search ke liye
    await db.users_collection.create_index(
        "data.email",
        unique=True  # ← duplicate email nahi aayega
    )
    
    print("✅ Indexes created")