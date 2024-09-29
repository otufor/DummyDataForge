# DummyDataForgeのDockerfile
FROM python:3.12-slim

WORKDIR /app

# 必要なPythonパッケージをインストール
COPY requirements.txt .
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

# PYTHONPATHを設定
ENV PYTHONPATH=/app/src:$PYTHONPATH

# アプリケーションコードをコピー
# COPY src/ /app/src/
# COPY config/ /app/config/
# COPY tests/ /app/tests/

# 入力と出力のためのボリュームを作成
VOLUME /app/input
VOLUME /app/output

# アプリケーションを実行
CMD ["python", "src/dummydataforge.py"]
