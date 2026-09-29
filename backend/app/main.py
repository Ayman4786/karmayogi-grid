from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.router import router


app = FastAPI(
    title="Karmayogi-Grid API",
    version="1.0.0",
)


# ------------------------------------------------------------
# CORS
# ------------------------------------------------------------
# Allow the local React/Vite frontend to communicate
# with the FastAPI backend during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)