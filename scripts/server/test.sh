HOST='' \
PORT='' \
PROJECT='' \
docker compose exec server python3 -m unittest discover -s bigbytes --failfast
