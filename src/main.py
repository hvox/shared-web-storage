import json
from fastapi import FastAPI, HTTPException
from pathlib import Path
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import APIKeyHeader
import fastapi.security
from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.security import APIKeyHeader, APIKeyQuery, APIKeyCookie
from typing import Optional
import fastapi.security


app = FastAPI()
users: dict[str, dict] = {}


# app.mount("/X/", StaticFiles(directory=Path(__file__).parent.parent / "data" / "x"), name="static")


SESSIONS = {"bubik", "aboba", "granted"}
api_key_header = APIKeyCookie(name="session-id")


async def get_session_id(api_key: str = Depends(api_key_header)):
    if api_key not in SESSIONS:
        raise HTTPException(status_code=403, detail="Invalid session id")
    return api_key


@app.get("/secure")
def secure_route(api_key: str = Depends(get_session_id)):
    return {"message": "Access granted", "api_key": api_key}


@app.get("/auth")
def secure_route(response: Response):
    x = hex(hash(str(len(SESSIONS))))[-4:]
    SESSIONS.add(x)
    response.set_cookie("session-id", x)
    return {"session-id": x}


@app.get("/{user}/{path:path}")
def get_file(user: str, path: str, api_key: str = Depends(get_session_id)):
    absolute_path = Path(__file__).parent.parent / "data" / user / path
    if not absolute_path.is_file(follow_symlinks=False):
        raise HTTPException(404, "File not found")
    # print(absolute_path)
    # return str(absolute_path)
    return FileResponse(path=absolute_path, media_type="text/plain")


if __name__ == "__main__":
    __import__("uvicorn").run(app, host="0.0.0.0", port=8000)
