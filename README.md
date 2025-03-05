# VueGit
## Backend setup
```
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

Frontend install

cd frontend
npm install
npm run serve

MongoDB users table
Для нормальной авторизации следует добавить табличку с пользователями к себе в БД. 
Таблица с данными прикреплена: testDB_Velocimetry_v2.users.json
