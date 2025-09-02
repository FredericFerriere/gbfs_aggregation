import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler

from constants import GBFS_URL, DATA_UPDATE_FREQ_MINUTES
from gbfs_importer.generic_importer import GenericImporter
from db_handling.db_utility import create_db_and_tables


def import_data():
    importer = GenericImporter()
    importer.import_data(GBFS_URL)

    return


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(import_data, "interval", minutes=DATA_UPDATE_FREQ_MINUTES)
    scheduler.start()
    yield


def create_app():
    """
    Initialising the API, setting up the db if empty, launching a first data import
    :return:
    """
    create_db_and_tables()
    import_data()

    app = FastAPI(lifespan=lifespan)

    origins = [
        "http://localhost:3000"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

