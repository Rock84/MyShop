from fastapi import FastAPI

from src.settings.settings import settings

app = FastAPI()

@app.get('/')
def test():
    return {'DB_NAME': settings.db_url}
