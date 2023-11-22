#🔗 c2a-worker 
(content2audio-worker) 内容转audio的消费者服务

## 系统设计
1. fastapi 作为控制线程
2. 消费者线程组作为消费者服务，可以配置多个

## 系统api
1. 启动服务
2. 关闭服务
3. 查看服务状态
4. 