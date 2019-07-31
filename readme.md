# sm-reddit

`mv secrets.py _secrets.py`

`docker build -t sm-reddit .`

`docker pull ianad/sm-reddit`

`docker run -it -p 8888:8888 -e JUPYTER_ENABLE_LAB=yes ianad/sm-reddit`