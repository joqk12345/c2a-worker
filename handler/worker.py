import time
from threading import Thread
import logger

def process_worker():
    while True:
        logger.notice("processing")
        time.sleep(5)

def entrypoint():
    worker_num = 1
    workers = []
    for idx in range(worker_num):
        logger.notice("start: {}", idx)
        workers.append(Thread(target=process_worker))

    for w in workers:
        w.start()

    # 等待所有线程完成
    # for w in workers:
    #     w.join()

    # logger.notice("All workers have finished.")