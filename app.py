from fastapi import FastAPI, Query
from parser import get_tenders

app = FastAPI(title="Tender API")

@app.get("/tenders")
def tenders(max: int = Query(10, ge=1, le=100)):
    """
    Получить список тендеров.
    Параметр max - максимальное количество (по умолчанию 10, максимум 100).
    """
    tenders_list = get_tenders(max_count=max)
    return {"count": len(tenders_list), "tenders": tenders_list}