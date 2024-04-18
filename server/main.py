from fastapi import FastAPI
import logging

from routes.main_route import router as main_route

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

app = FastAPI()
app.include_router(main_route)
