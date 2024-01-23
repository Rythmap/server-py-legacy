from routes.main_route import router as main_route
from fastapi import FastAPI
import uvicorn

app = FastAPI()
app.include_router(main_route)
