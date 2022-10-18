## Realtime data streaming with FastAPI and Server-Sent Events

![Server](/img/term.gif?raw=true "Terminal")
![Browser](/img/web.gif?raw=true "Browser")


## Setup
### Prerequisites
* Python 3.9+
* [poetry](https://python-poetry.org) package manager

```shell
$ git clone git@github.com:anton-petrov/sse-python-demo.git
$ cd sse-python-demo
$ poetry shell
$ poetry install
$ chmod +x ./start.sh
```

### Demo
- Run server: `./start.sh`
- Run client in browser `http://localhost:8000`
- Run client in terminal `python app/client.py` or `poetry run app/client.py`
