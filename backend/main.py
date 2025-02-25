from fastapi import FastAPI, HTTPException
from models import Task, User
from database import init_db
from beanie import PydanticObjectId
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Укажите адрес вашего фронтенда
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

@app.on_event("startup")
async def startup_db_client():
    await init_db()

# Pydantic модель для создания задачи
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

# Pydantic модель для обновления задачи
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# Pydantic модель для создания пользователя
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    is_admin: bool = False

# Создание задачи
@app.post("/tasks/", response_model=Task)
async def create_task(task: TaskCreate):
    new_task = Task(**task.dict())
    await new_task.insert()
    return new_task

# Получение всех задач
@app.get("/tasks/", response_model=list[Task])
async def get_all_tasks():
    tasks = await Task.find_all().to_list()
    return tasks

# Получение задачи по ID
@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: PydanticObjectId):
    task = await Task.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Обновление задачи
@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: PydanticObjectId, task: TaskUpdate):
    existing_task = await Task.get(task_id)
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await existing_task.update({"$set": task.dict(exclude_unset=True)})
    return existing_task

# Удаление задачи
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: PydanticObjectId):
    task = await Task.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await task.delete()
    return {"message": "Task deleted"}

# Эндпоинты для пользователей
@app.post("/admin/users/", response_model=User)
async def create_user(user: UserCreate):  # Используем UserCreate
    new_user = User(**user.dict())
    await new_user.insert()
    return new_user

@app.get("/admin/users/", response_model=List[User])
async def get_all_users():
    users = await User.find_all().to_list()
    return users

@app.put("/admin/users/{user_id}", response_model=User)
async def update_user(user_id: PydanticObjectId, user: UserCreate):  # Используем UserCreate
    existing_user = await User.get(user_id)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await existing_user.update({"$set": user.dict(exclude_unset=True)})
    return existing_user

@app.delete("/admin/users/{user_id}")
async def delete_user(user_id: PydanticObjectId):
    user = await User.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await user.delete()
    return {"message": "User deleted"}