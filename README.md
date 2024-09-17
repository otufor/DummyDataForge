# DummyDataForge

DummyDataForgeは、Ollamaモデルを使用してダミーデータを生成するツールです。

## 使い方

1. inputディレクトリにcsvファイルを配置してください。
2. `./run.sh` を実行してコンテナでプログラムを起動します。ollamaサーバコンテナとdummydataforgeコンテナが起動し、自動的に終了します。
4. outputディレクトリに、ダミーデータが生成されたcsvファイルが保存されます。

## Ollamaモデル指定方法

Ollamaモデルは、コマンドライン引数を使用して指定することができます。
`./run.sh <モデル名>`

[ollamaモデル検索ページ](https://ollama.com/library)

## カスタマイズ方法

pythonスクリプトを変更する場合、docker コンテナイメージをビルドしないと反映されません。
`docker compose build` でイメージをビルドしてから、`./run.sh` を実行してください。

## 注意点

* ダミーデータ生成は、ローカルのOllamaモデルを使用して行われます。
* 使用するモデルによって、データ品質にばらつきがあります。
* 実行環境によって最適なモデルは異なります。適宜、使用するモデルやプロンプトを変更してください。
* 生成されるデータのフォーマットは安定していません。数回やり直して、適切なデータが生成されるまで試行錯誤してください。

## 必要な環境

* Docker
* Docker Compose
* Nvidia GPU
* Nvidia container toolkit

## ファイル構成

* `run.sh`: プログラム実行スクリプト
* `dummydataforge.py`: ダミーデータ生成スクリプト
* `Dockerfile`: Dockerイメージビルドファイル
* `docker-compose.yml`: Docker Compose設定ファイル
* `requirements.txt`: Pythonパッケージ依存関係ファイル

## Ollamaモデル格納場所について

Ollamaモデルは、pullにより `OLLAMA_MODELS` ディレクトリに配置されます。永続化されるため、pullされたモデルはコンテナを再起動しても削除されません。
ディスクスペースが不足している場合は、`OLLAMA_MODELS` ディレクトリを適宜削除してください。

## プログラムの説明

### ダミーデータ生成について

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

### Ollamaモデルダウンロードについて

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

