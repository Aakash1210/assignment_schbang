# Ad Metrics API Project



## Setup Instructions

- Set Up a Virtual Environment
python3 -m venv .venv

- Activate the Virtual Environment
(macos,linux)
source .venv/bin/activate

(windows)
.venv\Scripts\activate

- Install Dependencies
pip install -r requirements.txt

- Configure Environment Variables (change into .env)
DATABASE_URL=postgresql://youruser:yourpassword@localhost:5432/yourdbname

- Run Database Migrations (/app) inside app folder
alembic upgrade head

- Run the FastAPI Application (run inside the /app )
uvicorn main:app --reload