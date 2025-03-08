# Ad Metrics API Project



## Setup Instructions

- Set Up a Virtual Environment
python3 -m venv .venv

- Activate the Virtual Environment
source .venv/bin/activate

- Install Dependencies
pip install -r requirements.txt

- Configure Environment Variables (change into .env)
DATABASE_URL=postgresql://youruser:yourpassword@localhost:5432/yourdbname

- Config into alembic.ini
add this sqlalchemy.url= postgresql://youruser:yourpassword@localhost:5432/yourdbname
- Run Database Migrations
alembic upgrade head

- Run the FastAPI Application
uvicorn app.main:app --reload