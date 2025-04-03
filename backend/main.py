from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorClient
from jose import JWTError, jwt
from passlib.hash import argon2
from datetime import datetime, timedelta
from bson import ObjectId  # Добавьте в начале файла
from typing import Optional
from beanie import init_beanie
from models import ProjectDB, FileDB, EstimateDB, RecordDB, UserDB, PyObjectId, UserRole, ActivityLog
from fastapi.middleware.cors import CORSMiddleware


# Настройки JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# OAuth2 схема
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # URL вашего Vue.js приложения
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение к MongoDB
@app.on_event("startup")
async def startup_db_client():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(
        database=client.testDB_Velocimetry_v2,
        document_models=[ProjectDB, FileDB, EstimateDB, RecordDB, UserDB, ActivityLog],  # Добавьте UserDB
    )

# Функция для хэширования пароля
def get_password_hash(password: str) -> str:
    return argon2.hash(password)

# Функция для проверки пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return argon2.verify(plain_password, hashed_password)

# Функция для создания JWT токена
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Функция для получения текущего пользователя
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await UserDB.find_one(UserDB.username == username)
    if user is None:
        raise credentials_exception
    return user

# Функция для проверки роли администратора
async def get_current_admin(current_user: UserDB = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    return current_user

# Эндпоинт для регистрации
@app.post("/register/", response_model=UserDB)
async def register(user: UserDB):
    user.password = get_password_hash(user.password)
    user.role = UserRole.USER  # По умолчанию роль "user"
    await user.create()
    return user

# Эндпоинт для авторизации
@app.post("/token/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await UserDB.find_one(UserDB.username == form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},  # Добавляем роль в токен
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Защищенный маршрут для администраторов
@app.get("/admin/")
async def admin_route(current_user: UserDB = Depends(get_current_admin)):
    return {"message": f"Hello, Admin {current_user.username}!"}

# Защищенный маршрут для всех пользователей
@app.get("/protected/")
async def protected_route(current_user: UserDB = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}!"}

# CRUD для Projects
@app.get("/projects/", response_model=list[ProjectDB])
async def get_all_projects(current_user: UserDB = Depends(get_current_user)):
    projects = await ProjectDB.find_all().to_list()
    return projects

@app.get("/projects/{project_id}", response_model=ProjectDB)
async def get_project(project_id: str):
    project = await ProjectDB.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.post("/projects/", response_model=ProjectDB)
async def create_project(project: ProjectDB):
    await project.create()
    return project

@app.put("/projects/{project_id}", response_model=ProjectDB)
async def update_project(project_id: str, project: ProjectDB):
    existing_project = await ProjectDB.get(project_id)
    if not existing_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Используем оператор $set для обновления полей
    update_data = {"$set": project.dict()}
    await existing_project.update(update_data)
    
    return existing_project

@app.delete("/projects/{project_id}")
async def delete_project(project_id: str):
    project = await ProjectDB.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    await project.delete()
    return {"message": "Project deleted"}

# Эндпоинты для админской панели
@app.get("/admin/users/", response_model=list[UserDB])
async def get_all_users(current_user: UserDB = Depends(get_current_admin)):
    users = await UserDB.find_all().to_list()
    return users

@app.post("/admin/users/", response_model=UserDB)
async def create_user(user: UserDB, current_user: UserDB = Depends(get_current_admin)):
    user.password = get_password_hash(user.password)
    await user.create()
    return user

@app.put("/admin/users/{user_id}", response_model=UserDB)
async def update_user(user_id: str, user: UserDB, current_user: UserDB = Depends(get_current_admin)):
    existing_user = await UserDB.get(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.password = get_password_hash(user.password)
    update_data = {"$set": user.dict()}
    await existing_user.update(update_data)
    
    return existing_user

@app.delete("/admin/users/{user_id}")
async def delete_user(user_id: str, current_user: UserDB = Depends(get_current_admin)):
    user = await UserDB.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await user.delete()
    return {"message": "User deleted"}

# CRUD для Files
@app.get("/files/", response_model=list[FileDB])
async def get_all_files():
    files = await FileDB.find_all().to_list()
    return files

@app.get("/files/by_project/{project_id}", response_model=list[FileDB])
async def get_files_by_project(project_id: str):
    print(f"Request for project_id: {project_id}, type: {type(project_id)}")
    
    from bson import ObjectId
    try:
        obj_id = ObjectId(project_id)
        print("Trying as ObjectId:", obj_id)
        files = await FileDB.find({"projectID": {"$in": [obj_id]}}).to_list()
        print(f"Found {len(files)} files with ObjectId")
        
        if not files:
            print("Trying as string")
            files = await FileDB.find({"projectID": {"$in": [project_id]}}).to_list()
            print(f"Found {len(files)} files with string")
            
        return files
    except Exception as e:
        print(f"Error: {str(e)}")
        files = await FileDB.find({"projectID": {"$in": [project_id]}}).to_list()
        print(f"Found {len(files)} files with string after error")
        return files
    
@app.get("/files/{file_id}", response_model=FileDB)
async def get_file(file_id: str):
    file = await FileDB.get(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file

@app.post("/files/", response_model=FileDB)
async def create_file(file: FileDB):
    # Преобразуем все projectID в ObjectId
    from bson import ObjectId
    file.projectID = [
        ObjectId(pid) if ObjectId.is_valid(pid) else pid 
        for pid in file.projectID
    ]
    await file.create()
    return file

@app.put("/files/{file_id}", response_model=FileDB)
async def update_file(file_id: str, file: FileDB):
    existing_file = await FileDB.get(file_id)
    if not existing_file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Преобразуем projectID в ObjectId
    file.projectID = [
        ObjectId(pid) if isinstance(pid, str) and ObjectId.is_valid(pid) else pid
        for pid in file.projectID
    ]
    
    await existing_file.update({"$set": file.dict()})
    return existing_file

@app.delete("/files/{file_id}")
async def delete_file(file_id: str):
    file = await FileDB.get(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    await file.delete()
    return {"message": "File deleted"}

# CRUD для Estimates
@app.get("/estimates/", response_model=list[EstimateDB])
async def get_all_estimates():
    estimates = await EstimateDB.find_all().to_list()
    return estimates

@app.get("/estimates/by_file/{file_id}", response_model=list[EstimateDB])
async def get_estimates_by_file(file_id: str):
    print(f"Request for file_id: {file_id}, type: {type(file_id)}")
    
    from bson import ObjectId
    try:
        obj_id = ObjectId(file_id)
        print("Trying as ObjectId:", obj_id)
        estimates = await EstimateDB.find({"file_id": {"$in": [obj_id]}}).to_list()
        print(f"Found {len(estimates)} estimates with ObjectId")
        
        if not estimates:
            print("Trying as string")
            estimates = await EstimateDB.find({"file_id": {"$in": [file_id]}}).to_list()
            print(f"Found {len(estimates)} estimates with string")
            
        return estimates
    except Exception as e:
        print(f"Error: {str(e)}")
        estimates = await EstimateDB.find({"file_id": {"$in": [file_id]}}).to_list()
        print(f"Found {len(estimates)} estimates with string after error")
        return estimates

@app.get("/estimates/{estimate_id}", response_model=EstimateDB)
async def get_estimate(estimate_id: str):
    estimate = await EstimateDB.get(estimate_id)
    if not estimate:
        raise HTTPException(status_code=404, detail="Estimate not found")
    return estimate
 
@app.post("/estimates/", response_model=EstimateDB)
async def create_estimate(estimate: EstimateDB):
    from bson import ObjectId
    
    print("Received estimate data:", estimate.dict())
    
    # Преобразуем file_id
    original_ids = estimate.file_id.copy()
    estimate.file_id = [
        ObjectId(pid) if isinstance(pid, str) and ObjectId.is_valid(pid) else pid
        for pid in estimate.file_id
    ]
    
    print(f"Converted file_id from {original_ids} to {estimate.file_id}")
    
    await estimate.create()
    
    created_estimate = await EstimateDB.get(estimate.id)
    print("Created estimate:", created_estimate.dict())
    
    return created_estimate

@app.put("/estimates/{estimate_id}", response_model=EstimateDB)
async def update_estimate(estimate_id: str, estimate: EstimateDB):
    existing_estimate = await EstimateDB.get(estimate_id)
    if not existing_estimate:
        raise HTTPException(status_code=404, detail="Estimate not found")
    
    # Преобразуем file_id в ObjectId
    estimate.file_id = [
        ObjectId(fid) if isinstance(fid, str) and ObjectId.is_valid(fid) else fid
        for fid in estimate.file_id
    ]
    
    await existing_estimate.update({"$set": estimate.dict()})
    return existing_estimate

@app.delete("/estimates/{estimate_id}")
async def delete_estimate(estimate_id: str):
    estimate = await EstimateDB.get(estimate_id)
    if not estimate:
        raise HTTPException(status_code=404, detail="Estimate not found")
    await estimate.delete()
    return {"message": "Estimate deleted"}

# CRUD для Records
@app.get("/records/", response_model=list[RecordDB])
async def get_all_records():
    records = await RecordDB.find_all().to_list()
    return records
    
@app.get("/records/by_estimate/{estimate_id}", response_model=list[RecordDB])
async def get_records_by_estimate(estimate_id: str):
    from bson import ObjectId
    try:
        obj_id = ObjectId(estimate_id) if ObjectId.is_valid(estimate_id) else estimate_id
        records = await RecordDB.find({"estimate_id": {"$in": [obj_id]}}).to_list()
        print(f"Found {len(records)} records with ObjectId")
        
        # Сортировка на сервере
        type_priority = {
            "meta_crack_model": 1,
            "interface_moire": 2,
            "velocimetry": 3,
            "meta_record": 4
        }
        
        records.sort(key=lambda x: (
            type_priority.get(x.tag, 4),
            x.frame if isinstance(x.frame, int) else 0
        ))
        
        return records
    except Exception as e:
        print(f"Error fetching records: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/records/{record_id}", response_model=RecordDB)
async def get_record(record_id: str):
    record = await RecordDB.get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@app.post("/records/", response_model=RecordDB)
async def create_record(record: RecordDB):
    from bson import ObjectId
    record.estimate_id = [
        ObjectId(eid) if isinstance(eid, str) and ObjectId.is_valid(eid) 
        else eid for eid in record.estimate_id
    ]
    await record.create()
    return record

@app.put("/records/{record_id}", response_model=RecordDB)
async def update_record(record_id: str, record: RecordDB):
    existing_record = await RecordDB.get(record_id)
    if not existing_record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    update_data = {"$set": record.dict()}
    await existing_record.update(update_data)
    
    return existing_record

@app.delete("/records/{record_id}")
async def delete_record(record_id: str):
    record = await RecordDB.get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    await record.delete()
    return {"message": "Record deleted"}

@app.get("/admin/activity", response_model=list[ActivityLog])
async def get_activity_logs(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    action: Optional[str] = Query(None, description="Filter by action type"),
    date_from: Optional[datetime] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[datetime] = Query(None, description="End date (YYYY-MM-DD)"),
    current_user: UserDB = Depends(get_current_admin)  # Требуем админских прав
):
    # Базовый запрос
    query = {}
    
    # Фильтрация по пользователю
    if user_id:
        query["user_id"] = user_id
    
    # Фильтрация по типу действия
    if action:
        query["action"] = action
    
    # Фильтрация по дате
    if date_from or date_to:
        query["timestamp"] = {}
        if date_from:
            query["timestamp"]["$gte"] = date_from
        if date_to:
            # Добавляем 1 день чтобы включить всю конечную дату
            query["timestamp"]["$lte"] = date_to + timedelta(days=1)
    
    # Выполняем запрос с сортировкой по времени
    logs = await ActivityLog.find(query).sort("-timestamp").to_list()
    
    return logs

from pydantic import BaseModel
class ActivityLogCreate(BaseModel):
    action: str
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    details: Optional[str] = None

@app.post("/admin/activity", response_model=ActivityLog)
async def create_activity_log(
    log_data: ActivityLogCreate,
    current_user: UserDB = Depends(get_current_user)
):
    log = ActivityLog(
        user_id=str(current_user.id),
        action=log_data.action,
        entity_type=log_data.entity_type,
        entity_id=log_data.entity_id,
        details=log_data.details or ""
    )
    await log.create()
    return log