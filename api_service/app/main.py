# from fastapi import FastAPI

# from api_service.app.routers.predict import router as predict_router
# from config.settings import settings


# app = FastAPI(title=settings.app_name, version="1.0.0")
# app.include_router(predict_router, tags=["predictions"])


# @app.get("/")
# def root() -> dict[str, str]:
#     return {
#         "message": "Fraud Detection API is running.",
#         "docs": "/docs",
#         "health": "/health",
#     }


# @app.get("/health")
# def health() -> dict[str, str]:
#     return {"status": "ok"}

# from fastapi import FastAPI, Request
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
# from api_service.app.routers.predict import router as predict_router
# from fastapi.middleware.cors import CORSMiddleware

# import os

# app = FastAPI()
# app.include_router(predict_router)

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# app.mount(
#     "/static",
#     StaticFiles(directory=os.path.join(BASE_DIR, "static")),
#     name="static"
# )

# # Templates folder
# templates = Jinja2Templates(directory="templates")


# @app.get("/")
# def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # allow all (for development)
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )



from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from api_service.app.routers.predict import router as predict_router
import os

app = FastAPI()

# ✅ ADD THIS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})