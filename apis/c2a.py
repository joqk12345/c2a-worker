import socket

running = False

def start():
    global running
    running = True
    return state()

def state():
    response = {
        "host": socket.gethostname(),
        "state": "running" if running else "stopped",
    }
    return response


def stop():
    global running
    running = False
    return state()