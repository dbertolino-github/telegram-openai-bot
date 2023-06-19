import os
import logging.config

from fastapi import FastAPI

# setup loggers
folder_path = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
logging.config.fileConfig(os.path.join(folder_path, 'logging.conf'), disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)  # the __name__ resolve to "main" since we are at the root of the project.

app = FastAPI()

@app.get("/health")
def read_root():
    return {"status": "ok"}