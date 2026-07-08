import random

from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="로또번호 생성기")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_index():
    """메인 페이지 반환"""
    return FileResponse("static/index.html")


@app.get("/api/lotto")
def generate_lotto(games: int = Query(default=5, ge=1, le=20)):
    """
    로또 번호를 생성해서 반환하는 API.
    games: 생성할 게임 수 (기본 5게임, 최대 20게임)
    """
    result = []
    for _ in range(games):
        numbers = sorted(random.sample(range(1, 46), 6))
        result.append(numbers)
    return {"games": result}


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
