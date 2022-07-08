import uvicorn

from fastapi import FastAPI, Depends
from mangum import Mangum
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from config import get_settings
from dependencies import get_db
from routers import api


app = FastAPI(openapi_url=f"{get_settings().api_str}/openapi.json")

app.include_router(api.api_router)


@app.get("/ping")
def health(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1;")
    except OperationalError:
        raise HTTPException(status_code=500, detail="DB not ready")
    return "pong"


handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
