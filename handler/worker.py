import time
from threading import Thread
import logger
from apis.c2a import state


def process_worker():
    while True:
        logger.notice("running state:{}", state())
        runnning_state = state()['state']
        if(runnning_state == "running"):
            logger.notice("processing")
            time.sleep(5)
        else:
            logger.swarn(5,"current running state :{},wait for a moment",runnning_state)


def entrypoint():
    worker_num = 4
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