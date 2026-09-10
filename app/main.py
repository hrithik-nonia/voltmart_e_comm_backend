from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.schema import schema
from app.database import db
from fastapi.middleware.cors import CORSMiddleware
from app.routes.upload import router as upload_router

app = FastAPI(title="VoltMart API")

# cross origin allow
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite ka port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# rest routes
app.include_router(upload_router)


# GraphQL endpoint
graphql_app = GraphQLRouter(schema)
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