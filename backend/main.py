from fastapi import FastAPI
from config import settings

app=FastAPI(title=settings.PROJECT_NAME)

@app.get("/")
def root_read():
    return {"message":f"Welcome to the {settings.PROJECT_NAME}!"}

