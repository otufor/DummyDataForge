# DummyDataForgeのDockerfile
FROM python:3.9-slim

WORKDIR /app

# 必要なPythonパッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY dummydataforge.py .

# 入力と出力のためのボリュームを作成
VOLUME /app/input
VOLUME /app/output

# アプリケーションを実行
CMD ["python", "dummydataforge.py"]
