import os
import json
import uvicorn
import requests
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from basicInfo import *

load_dotenv()

app = FastAPI()

@app.get("/instagram")
async def get_instagram():
    basic_info = get_basic_info()
    showInstagramPosts(basic_info)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
