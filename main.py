import logging
import uvicorn
from fastapi import FastAPI, Depends, Request
from typing import Union
from routers import auth, system
from database import engine
from db import auth_model
from pathlib import Path
from fastapi.security import OAuth2PasswordBearer
from logs.custom_logging import CustomizeLogger

logger = logging.getLogger(__name__)

config_path = Path("logs/logging_config.json")


auth_model.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_app() -> FastAPI:
    app = FastAPI(title='CustomLogger', debug=False)
    logger = CustomizeLogger.make_logger(config_path)
    app.logger = logger

    return app


app = create_app()


app.include_router(auth.router, dependencies=[Depends(oauth2_scheme)])
app.include_router(system.router)
logger = CustomizeLogger.make_logger(config_path)


@app.get("/")
def read_root(request: Request):
    logging.info("logging info log!!")
    logger.info("make logger log!!")
    print("request value : ", request.headers['authorization'])

    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == '__main__':
    uvicorn.run(app, port=8000)
