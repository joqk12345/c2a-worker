import threading
from fastapi import FastAPI
import logger
import apis as _apis_
from handler import worker

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
    # uvicorn.run("main:app", host="0.0.0.0", port=8000,reload=True)
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

def start():
    # 多线程配合
    fastapithread = threading.Thread(target=run_fastapi)

    # 每个线程都进入线程入口函数启动线程执行
    fastapithread.start()
    worker.entrypoint()

    # 每个线程都出发等待结果
    fastapithread.join()

if __name__ == '__main__':
    start()


