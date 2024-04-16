from fastapi import FastAPI

from routes.main_route import router as main_route

app = FastAPI()
app.include_router(main_route)
