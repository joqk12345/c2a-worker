#🔗 c2a-worker 
(content2audio-worker) 内容转audio的消费者服务

## 系统设计
1. fastapi 作为控制线程
2. 消费者线程组作为消费者服务，可以配置多个

## 系统api
1. 启动服务
2. 关闭服务
3. 查看服务状态



## 异步服务设计
1. 什么是event_loop？
2. 他的原理是什么？
2. 异步服务的执行方式

## 不同种类的导入类型
1. 应用导入字符串
```Markdown
导入字符串是指将模块或对象的导入路径表示为一个字符串。在Python中，我们可以使用导入字符动态地导入模块、类、函数或对象。
导入字符串的一般格式是 module_name:object_name。其中，module_name 是模块的名称或路径，object_name 是模块中的对象名称，可以是类、函数或变量等。

例如，如果我们有一个名为 my_module 的模块，其中定义了一个名为 my_function 的函数，我们可以使用导入字符串 'my_module:my_function' 来表示这个函数。

导入字符串通常在需要动态导入模块或对象的场景下使用，例如在框架或应用程序服务器中根据配置或用户输入来导入特定的模块或对象。

在前面的示例中，我提到了一个应用程序的导入字符串 'myapp:app'。这是一个假设的示例，其中 'myapp' 是模块名，'app' 是模块中的对象名，可能是一个应用程序实例或函数等。具体的导入字符串格式取决于你的应用程序的结构和要求。

通过使用导入字符串，我们可以在运行时根据需要动态地导入模块或对象，从而实现更灵活和可配置的代码结构。
```

2. fastapi的执行执行方式
 ### 1. Python通过 __main__导入 
1. 需要增加__main__ 函数，导入方式也是应用字符串导入

```python
if __name__ == '__main__':
import uvicorn
uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

2. 执行代码如下

```python
     python  main:app  --reload
```

### 2. 通过uniconv 
没有__main__函数
  ```python
  uvicorn main:app --reload
```

### 3. 通过thread方式

1. 需要一个函数的引用
2. 需要一个单独的执行环境

```python
import threading
def run_fastapi():
    import uvicorn
    #uvicorn.run("main:app", host="0.0.0.0", port=8000,reload=True)
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

def start():
    fastapithread = threading.Thread(target=run_fastapi)
    fastapithread.start()
    fastapithread.join()
    
if __name__ == '__main__':
    start()
```
- [ ] 注意reload机制在线程环境中执行会报错，

### 4. 多线程服务设计

1. 使用一个fastapi的线程来执行服务管理
2. 使用一个线程组来执行worker

worker.py
```python
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
```
main.py
```python
import threading
from  handler import worker
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


```

### 5. 不同线程间通信




### 控制脚本的设计


#### 项目结构


# 参考资料
1. [runthecode](https://fastapi.tiangolo.com/tutorial/#run-the-code)
2. [epool机制](https://www.cnblogs.com/littlecarry/p/17127936.html)