from fastapi import FastAPI

app=FastAPI(title="TaskFlow API")

@app.get("/")
def root_read():
    return {"message":"Welcome to the TaskFlow application!"}

