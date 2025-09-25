from fastapi import FastAPI
from app.routers import scan
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="SafeCloud Backend",
    description="Python vulnerability scanner with SQLite",
    version="0.1.0"
)

origins = ["http://localhost:3000"]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)


app.include_router(scan.router, prefix="/scan", tags=["Scan"])

@app.get("/")
def root():
    return {"message": "SafeCloud Backend is running!"}
