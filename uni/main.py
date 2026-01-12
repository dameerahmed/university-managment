from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from uni.routes import (
    users_routes,
    teachers_routes,
    batches_routes,
    students_routes,
    results_routes,
    subjects_routes,
    departments_routes,
)

app = FastAPI(title="UMS API", swagger_ui_parameters={"persistAuthorization": True})


# React usually port 3000 par chalta hai
origins = [
    "http://localhost:3000",  # React ka address
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Saari requests allow karein (GET, POST, DELETE)
    allow_headers=["*"],
)


app.include_router(users_routes.router)
app.include_router(teachers_routes.router)
app.include_router(batches_routes.router)
app.include_router(students_routes.router)
app.include_router(results_routes.router)
app.include_router(subjects_routes.router)
app.include_router(departments_routes.router)


def start():
    uvicorn.run("uni.main:app", host="127.0.0.1", port=8000, reload=True)
