import random
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

app = FastAPI(title="공룡 뽑기")

app.mount("/static", StaticFiles(directory="static"), name="static")


class DrawRequest(BaseModel):
    names: List[str] = Field(..., min_length=1, max_length=30)
    winners: int = Field(..., ge=0, le=30)


@app.get("/")
def read_index():
    return FileResponse("static/index.html")


@app.post("/api/draw")
def draw(req: DrawRequest):
    """
    이름 목록과 당첨 인원 수를 받아, 무작위로 당첨자를 배정해서 반환.
    입력 순서 그대로 반환하며, win 필드로 당첨 여부 표시.
    """
    names = [n.strip() for n in req.names if n.strip()]
    if not names:
        raise HTTPException(status_code=400, detail="이름을 1명 이상 입력해주세요.")
    if req.winners > len(names):
        raise HTTPException(status_code=400, detail="당첨 인원이 전체 인원보다 많을 수 없어요.")

    win_indexes = set(random.sample(range(len(names)), req.winners))
    results = [{"name": name, "win": i in win_indexes} for i, name in enumerate(names)]
    return {"results": results}


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
