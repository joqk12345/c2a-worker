import threading
import logger
import apis as _apis_
from handler import worker
from fastapi import FastAPI
app = FastAPI()

# hook
async def startup_event():
    # 在应用程序启动时执行的操作
    logger.notice("应用程序启动")

app.add_event_handler("startup", startup_event)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/api/state")
async def state():
    return _apis_.c2a.state()

@app.get("/api/start")
async def start():
    return _apis_.c2a.start()

@app.get("/api/stop")
async def stop():
    return _apis_.c2a.stop()


def run_fastapi():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,reload=True)



if __name__ == '__main__':
    run_fastapi()
    threading.Thread(target=run_fastapi)
    logger.notice("start worker")
    worker.main()