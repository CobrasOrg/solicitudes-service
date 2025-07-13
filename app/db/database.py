from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def get_database() -> AsyncIOMotorClient:
    return db.client[settings.MONGODB_DATABASE]

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    print("✅ Conectado a MongoDB exitosamente")

async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("🔌 Conexión a MongoDB cerrada") 