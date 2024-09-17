# DummyDataForge

DummyDataForgeは、Ollamaモデルを使用してダミーデータを生成するツールです。

## 使い方

1. inputディレクトリにcsvファイルを配置してください。
2. `docker-compose up -d ollama` を実行してOllamaコンテナを起動します。
3. `docker-compose run --rm dummydataforge` を実行してダミーデータを生成します。
4. outputディレクトリに、ダミーデータが生成されたcsvファイルが保存されます。

## 必要なファイル

* `dummydataforge.py`: ダミーデータ生成スクリプト
* `Dockerfile`: Dockerイメージビルドファイル
* `docker-compose.yml`: Docker Compose設定ファイル
* `requirements.txt`: Pythonパッケージ依存関係ファイル

## Ollamaモデル

Ollamaモデルは、pullにより `OLLAMA_MODELS` ディレクトリに配置されます。

## ダミーデータ生成

ダミーデータ生成は、`dummydataforge.py` スクリプトによって行われます。このスクリプトは、Ollamaモデルを使用して入力ファイルからダミーデータを生成します。

```python
def process_file(input_file, output_file, model):
    print(f"Processing file: {input_file}")
    headers, data = read_csv_file(input_file)
    
    data_str = "\n".join([",".join(row) for row in data])
    
    result = process_with_ollama(data_str, model)
    dummy_data = [row.split(',') for row in result.strip().split('\n')]
    
    write_csv_file(output_file, headers, dummy_data)
    print(f"Dummy data saved to: {output_file}")
```

## Ollamaモデルダウンロード

Ollamaモデルは、`pull_model` 関数によって自動的にダウンロードされます。
pullされていないモデルが指定された場合は、ダウンロードに時間がかかります。

```python
def pull_model(model):
    print(f"Pulling model: {model}")
    url = "http://ollama:11434/api/pull"
    data = f"""{{
        "name": "{model}"
    }}"""
    response = requests.post(url, data=data)
    print(f"Complete pull model: {model}")
```

## 注意点

* ダミーデータ生成は、ローカルのOllamaモデルを使用して行われます。
* 使用するモデルによって、データ品質にばらつきがあります。
* 実行環境によって最適なモデルは異なります。適宜、使用するモデルやプロンプトを変更してください。
* 生成されるデータのフォーマットは安定していません。数回やり直して、適切なデータが生成されるまで試行錯誤してください。
