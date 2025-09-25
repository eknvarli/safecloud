from fastapi import FastAPI
from app.routers import scan
from app.database import Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="SafeCloud Backend",
    description="Python vulnerability scanner with SQLite",
    version="0.1.0"
)

app.include_router(scan.router, prefix="/scan", tags=["Scan"])

@app.get("/")
def root():
    return {"message": "SafeCloud Backend is running!"}
