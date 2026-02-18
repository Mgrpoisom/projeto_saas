from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def read_root():
    return {"status": "Online", "projeto": "Projeto Zero"}
