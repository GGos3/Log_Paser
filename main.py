from typing import Union
from fastapi import FastAPI
import par

app = FastAPI()


@app.get("/ping")
def read_root():
    return "pong"


@app.get("/ip")
def ip():
    return par.get_ip()
