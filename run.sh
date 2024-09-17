docker compose up -d ollama
docker compose run --rm dummydataforge python /app/dummydataforge.py $1
docker compose down
