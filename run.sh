docker compose up -d ollama
docker compose run --rm dummydataforge python /app/src/dummydataforge.py $1
docker compose down
