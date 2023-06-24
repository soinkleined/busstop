docker build --tag busstop-docker .
docker run --publish 8000:8000 busstop-docker
