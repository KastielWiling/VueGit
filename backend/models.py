from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import List, Optional, Union, Dict
from enum import Enum
from beanie import Document
from bson import ObjectId
from pydantic.json_schema import GetJsonSchemaHandler
from pydantic_core import core_schema

# Кастомный тип для ObjectId
class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string"}

class Project(BaseModel):
    name: str
    desc: str
    something: List[str] = []
    tag: str

class FileBase(BaseModel):
    name: str
    projectID: List[PyObjectId]
    filePath: str
    tag: str

class MetaFile(FileBase):
    fps: List[int]
    frameCount: int
    frameSize: List[int]

class MetaPhoto(FileBase):
    frameCount: int

from pydantic import field_validator
from bson import ObjectId

class FileDB(Document):
    name: str
    projectID: List[PyObjectId]  # Используем наш кастомный тип
    filePath: str
    tag: str
    frameCount: int
    fps: Optional[List[int]] = []
    frameSize: Optional[List[int]] = []

    class Settings:
        name = "files"

    @field_validator('projectID', mode='before')
    def convert_project_ids(cls, v):
        if isinstance(v, list):
            converted = []
            for item in v:
                if isinstance(item, ObjectId):
                    converted.append(str(item))  # Конвертируем ObjectId в строку
                elif isinstance(item, str) and ObjectId.is_valid(item):
                    converted.append(item)  # Оставляем валидные строки
                else:
                    converted.append(item)  # Оставляем как есть (вызовет ошибку валидации)
            return converted
        return v

    @field_validator('fps', mode='before')
    def convert_fps_to_int(cls, v):
        if v is not None:
            return [int(item) if isinstance(item, float) else item for item in v]
        return v
    
class Estimate(BaseModel):
    file_id: List[PyObjectId]
    frame_interval: List[int]
    roi: List[int]
    tag: str
    settings: dict


# Модели Beanie
class ProjectDB(Project, Document):
    class Settings:
        name = "projects"

class EstimateDB(Estimate, Document):
    class Settings:
        name = "estimates"

    @field_validator('file_id', mode='before')
    def convert_file_ids(cls, v):
        if isinstance(v, list):
            converted = []
            for item in v:
                if isinstance(item, ObjectId):
                    converted.append(str(item))  # Конвертируем ObjectId в строку
                elif isinstance(item, str) and ObjectId.is_valid(item):
                    converted.append(item)  # Оставляем валидные строки
                else:
                    converted.append(item)
            return converted
        return v

class RecordBase(BaseModel):
    estimate_id: List[PyObjectId]
    frame: Union[int, List[int]]  # Может быть как числом, так и списком чисел
    record: Union[
        List[List[float]],       # Для velocimetry и meta_record
        Dict[str, List[float]],  # Для meta_crack_model (mx, my)
        List[Dict[str, float]]   # Для interface_moire
    ]
    tag: str

class RecordDB(RecordBase, Document):
    class Settings:
        name = "records"

    @field_validator('estimate_id', mode='before')
    def convert_estimate_ids(cls, v):
        if isinstance(v, list):
            return [PyObjectId(item) if isinstance(item, (str, ObjectId)) else item for item in v]
        return v

    @field_validator('record', mode='before')
    def convert_record(cls, v):
        # Если record - это словарь (как в meta_crack_model)
        if isinstance(v, dict):
            return v
        # Если record - это список списков (как в velocimetry)
        elif isinstance(v, list) and all(isinstance(item, list) for item in v):
            return v
        # Если record - это список словарей (как в interface_moire)
        elif isinstance(v, list) and all(isinstance(item, dict) for item in v):
            return v
        return v

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class User(BaseModel):
    username: str
    email: EmailStr
    password: str  # Хэшированный пароль
    role: UserRole = UserRole.USER  # По умолчанию роль "user"

class UserDB(User, Document):
    class Settings:
        name = "users"  # Название коллекции в MongoDB