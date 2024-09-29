#!/bin/bash

# Dockerコンテナ内でpytestを実行
docker compose run --rm dummydataforge pytest /app/tests

# テスト実行後、コンテナを停止
docker compose down
