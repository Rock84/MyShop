from fastapi import FastAPI

from src.datebase.models import Base

app = FastAPI()

@app.get('/')
def test():
    return {'DB_NAME': Base.engine.url}
