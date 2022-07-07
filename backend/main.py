from fastapi import FastAPI
import Log_paser as log

app = FastAPI()


@app.get("/ping")
def ping():
    return "pong"


@app.get("/ip")
def ip():
    return log.get_location()


@app.get("/request")
def request():
    return log.get_request()
