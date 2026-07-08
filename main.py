import random

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="로또번호 생성기")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_index():
    """메인 페이지 반환"""
    return FileResponse("static/index.html")


@app.get("/api/lotto")
def generate_lotto():
    """
    로또 번호 1게임을 생성해서 반환.
    main: 정렬된 6개 번호
    bonus: 나머지 중 무작위 보너스 번호 1개 (main과 중복 없음)
    """
    picked = random.sample(range(1, 46), 7)
    main_numbers = sorted(picked[:6])
    bonus_number = picked[6]
    return {"main": main_numbers, "bonus": bonus_number}


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
