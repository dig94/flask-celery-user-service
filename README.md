# flask-celery-user-service
A simple Flask REST API integrated with Celery for asynchronous background tasks using Redis as a broker.
This project demonstrates user CRUD operations with MySQL and background welcome email task processing via Celery.

FLASK_APP/
├── app.py                    # Flask entrypoint
├── celery_app.py              # Celery configuration
├── celery_status.py           # Task status check example
├── controller/
│   ├── __init__.py
│   ├── user_controller.py     # User CRUD + Celery trigger
│   ├── product_controller.py  # (Optional future use)
│   └── test_controller.py
├── model/
│   ├── __init__.py
│   └── user_model.py          # MySQL operations + Marshmallow validation
├── tasks/
│   ├── __init__.py
│   └── user_tasks.py          # Celery task for sending welcome email
├── test.py                    # Celery task performance test
├── Dockerfile
├── requirements.txt
└── dump.rdb                   # Redis dump file


⚙️ Setup Instructions

1️⃣ Clone the repository

git clone https://github.com/<your-username>/flask-celery-app.git
cd flask-celery-app

2️⃣ Create and activate virtual environment

python3 -m venv flask-env
source flask-env/bin/activate  # on macOS/Linux
flask-env\Scripts\activate     # on Windows


3️⃣ Install dependencies

pip install -r requirements.txt

4️⃣ Set up MySQL

Create database and table:

CREATE DATABASE flask_tutorial;
USE flask_tutorial;

CREATE TABLE user (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50),
  email VARCHAR(100),
  phone VARCHAR(20),
  role VARCHAR(50),
  password VARCHAR(100)
);

5️⃣ Start Redis

You can use Docker:
docker run -d -p 6379:6379 redis

6️⃣ Start Celery worker

In one terminal:

celery -A celery_app.celery worker --loglevel=info

You should see:

worker@hostname ready.

7️⃣ Start Flask app

In another terminal:

python app.py

The Flask app will start on:
👉 http://127.0.0.1:5003

🧩 API Endpoints
Method	Endpoint	Description
GET	/user/signup	Health/test route
GET	/user/getAll	Get all users
POST	/user/addone	Add new user + trigger Celery email
PUT	/user/update	Update user details
DELETE	/user/delete/<id>	Delete user by ID
PATCH	/user/patch/<id>	Partial update
GET	/user/page/limit/<limit>/page/<page>	Pagination support


📬 Example CURL Requests

➕ Add User

curl -X POST http://127.0.0.1:5003/user/addone \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "role": "Admin",
    "password": "secret123"
  }'

Response:

{
  "message": "User added successfully",
  "db_result": {"message": "User added successfully"},
  "email_task_id": "4fcbcd47-2c1d-4d3e-9f4d-1234abcde567"
}

🔍 Check Celery Task Status

python celery_status.py

🧠 How It Works

When a new user is added via /user/addone,
Flask validates and stores the record in MySQL.

If the payload contains "email",
Celery asynchronously sends a “welcome email” (simulated).

Redis acts as the broker and backend, tracking task results.

You can monitor task execution via celery_status.py.

🐞 Troubleshooting
Issue	                                    Solution
redis.exceptions.ConnectionError	    Ensure Redis is running on port 6379
ModuleNotFoundError: tasks.user_tasks	Run Celery from project root
Celery tasks not executing	            Confirm include=["tasks.user_tasks"] in celery_app.py
Flask cannot import modules	            Use relative imports and project root as working directory
