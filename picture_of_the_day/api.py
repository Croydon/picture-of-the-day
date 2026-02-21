import io
import json
import logging
import os 
import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import Response


api = FastAPI()
logger = logging.getLogger("picture-of-the-day")


@api.get("/")
def read_root(request: Request):
    user_agent = request.headers.get('user-agent')
    return {"Hello": "World", "User-Agent": user_agent, "pwd": os.getcwd()}

def run_server(args):
    uvicorn.run(api, host="0.0.0.0", port=args.port)
