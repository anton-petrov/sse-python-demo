import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from datetime import datetime
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from starlette.responses import FileResponse
import time
import os
import threading
import logging
import queue
from app.sunpos import *

STREAM_DELAY = 1
RETRY_TIMEOUT = 1500

logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

queue = queue.Queue()

real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)

app.mount("/client", StaticFiles(directory=f"{dir_path}/../client"), name="client")

async def data_generator(request):
    id: int = 0
    while True:
        if await request.is_disconnected():
            logger.info("client disconnected")
            break
        if not queue.empty():
            id += 1
            next = queue.get()
            # https://datatracker.ietf.org/doc/html/rfc8895
            yield f"event: sun_position\nid: {id}\nretry: {RETRY_TIMEOUT}\ndata: {json.dumps(next)}\n\n"


@app.get('/stream-data')
async def stream_data(request: Request):
    event_generator = data_generator(request)
    return EventSourceResponse(event_generator)

@app.get('/')
async def get_index():
    return FileResponse('client/client.html')

def worker():
    while threading.main_thread().is_alive():
        queue.put(sunpos_now_krasnodar())
        time.sleep(STREAM_DELAY)

threading.Thread(target=worker).start()

if __name__ == '__main__':
    print('running uvicorn webserver')
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True, reload=True)
