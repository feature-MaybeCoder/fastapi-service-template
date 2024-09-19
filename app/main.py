import fastapi as fa
from app.api import router

fa_app = fa.FastAPI()
fa_app.include_router(router)
