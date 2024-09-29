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
* `src/dummydataforge.py`: ダミーデータ生成スクリプト
* `config/config.yaml`: 設定ファイル
* `config/system_prompt.txt`: システムプロンプトファイル
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

## 実行結果の例

以下は、入力ファイルと出力ファイルの例です。

### 入力ファイル (input/input1.csv)

```csv
id,first_name,last_name,email,phone_number,address,date_of_birth,credit_card_number,balance
1,佐藤,太郎,taro.sato@tokyomail.jp,080-1234-5678,"東京都新宿区西新宿1-23-7 シティハイツ西新宿305号",1985-06-15,4111222233334444,325000
2,鈴木,花子,hanako.suzuki@osakaweb.co.jp,090-8765-4321,"大阪府大阪市中央区難波5-1-60 なんばスカイオ25階",1990-11-22,5555666677778888,780500
3,田中,一郎,ichiro.tanaka@fukuokanet.jp,070-2468-1357,"福岡県福岡市博多区博多駅前3-2-1 博多三越ライオン像前",1978-03-30,3782822463100005,52000
4,山田,美咲,misaki.yamada@sapporolink.com,080-3692-5801,"北海道札幌市中央区大通西4-6-1 札幌大通ビルディング8階",1993-09-10,6011111122223333,460000
5,伊藤,健太,kenta.ito@nagoyabiz.jp,090-1597-5310,"愛知県名古屋市中区栄2-17-1 名古屋広小路ビル10階",1988-12-03,3566002020360505,195000
```

### 出力ファイル (output/input1_dummy.csv)

```csv
id,first_name,last_name,email,phone_number,address,date_of_birth,credit_card_number,balance
1,渡辺,太郎,tarou.watanabe@example.com,080-1234-5678,東京都渋谷区代々木2-3-1 渡辺ビルディング305号,1985-06-15,1234567890123456,325000
2,田中,花子,kana.tanaka@example.com,090-8765-4321,大阪府大阪市北区梅田2-3-1 梅田ビルディング25階,1990-11-22,9876543210987654,780500
3,鈴木,一郎,isao.suzuki@example.com,070-2468-1357,福岡県福岡市博多区博多駅前4-1-1 三越ビルディング,1978-03-30,6543210987654321,52000
4,山下,美咲,miho.yamashita@example.com,080-3692-5801,北海道札幌市中央区大通西5-6-1 札幌ビルディング8階,1993-09-10,4567891234567890,460000
5,井上,健太,kentaro.imai@example.com,090-1597-5310,愛知県名古屋市中区栄3-17-1 名古屋広小路ビル10階,1988-12-03,7654321098765432,195000
```

この例では、入力ファイルのデータ構造を保持しながら、個人情報を匿名化したダミーデータが生成されています。名前、メールアドレス、住所、クレジットカード番号などが変更されていますが、日付、電話番号形式、残高などの構造は維持されています。
