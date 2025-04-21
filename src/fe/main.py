from fastapi import FastAPI
import time

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Python Trading App running."}

@app.get("/trade")
def simulate_trade():
    time.sleep(0.1)  # simulate processing time
    return {"result": "Trade executed"}