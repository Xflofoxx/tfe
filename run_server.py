import uvicorn

if __name__ == "__main__":
    # Avvio in sviluppo locale
    uvicorn.run("src.fair_evaluator.main:app", host="127.0.0.1", port=8000, reload=True)
