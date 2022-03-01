# DDOS cluster client

❤️ Русский корабль, иди нахуй! ❤️

### With python:

**Requirements:**
- python 3.8 and higher

**Install:**
```shell
pip install -r requirements.txt
```

**Run:**
```shell
python main.py [-h] --name NAME [--threads THREADS]

options:
  -h, --help         show this help message and exit
  --name NAME        Client name
  --threads THREADS  Threads count
```

### With docker

**Requirements:**
- docker

**Build image:**
```shell
docker build -t ddoscluster-client .
```

**Run container:**
```shell
docker run ddoscluster-client --name 'Your custom name' --threads 100
```