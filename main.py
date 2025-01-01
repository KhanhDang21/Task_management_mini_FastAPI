from fastapi import FastAPI
from routers.authentication_router import router as AuthenticationRouter
from routers.task_router import router as TaskRouter

app = FastAPI()

app.include_router(AuthenticationRouter)
app.include_router(TaskRouter)
