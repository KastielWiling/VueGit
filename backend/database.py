from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models import User, Task  # Модель задачи

async def init_db():
    # Подключение к MongoDB
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    database = client.task_manager

    # Инициализация Beanie
    await init_beanie(database=database, document_models=[User, Task])