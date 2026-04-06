from fastapi import Response
from fastapi import FastAPI
import random
import time
from prometheus_client import Counter, Histogram, generate_latest 

app = FastAPI()


REQUEST_COUNT = Counter("request_count", "Total request count")
ERROR_COUNT = Counter("error_count", "Total error count")
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency")


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/data")
def get_data():
    REQUEST_COUNT.inc()

    start_time = time.time()

    time.sleep(random.uniform(0.1, 0.5))

    if random.random() < 0.2:
        ERROR_COUNT.inc()
        return {"error": "Something went wrong"}

    REQUEST_LATENCY.observe(time.time() - start_time)

    return {"data": "Here is your data"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
