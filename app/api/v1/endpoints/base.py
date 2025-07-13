from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.db.mongodb import mongodb

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "healthy"} 