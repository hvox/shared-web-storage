import json
from fastapi import FastAPI, HTTPException
from pathlib import Path
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
users: dict[str, dict] = {}


# app.mount("/X/", StaticFiles(directory=Path(__file__).parent.parent / "data" / "x"), name="static")


@app.get("/{user}/{path:path}")
def get_file(user: str, path: str):
    absolute_path = Path(__file__).parent.parent / "data" / user / path
    if not absolute_path.is_file(follow_symlinks=False):
        raise HTTPException(404, "File not found")
    # print(absolute_path)
    # return str(absolute_path)
    return FileResponse(path=absolute_path, media_type="text/plain")


if __name__ == "__main__":
    __import__("uvicorn").run(app, host="0.0.0.0", port=8000)
