import requests
import json
import csv
import os
import time
import glob

def read_csv_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        data = list(reader)
    return headers, data

def write_csv_file(file_path, headers, data):
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

def process_with_ollama(text, model="llama2"):
    url = "http://ollama:11434/api/generate"

    system_prompt_jp = """
        あなたの任務は、システムテスト用のダミーデータを生成するツールを模倣することです。顧客情報、企業データ、金額などの機密情報を架空かつ現実的な代替データに置き換えてください。元のデータの構造と特徴を維持しながら、以下のガイドラインに従ってください：

        1. データの整合性を維持：
        - 元のデータの形式を保持（テキスト、数値、日付など）。
        - 元のデータセットと同じレコード数を維持。

        2. データパターンの再現：
        - 各フィールドの長さの範囲（最小と最大）を一致させる。
        - 数値フィールドの現実的な範囲を維持（年齢、価格、数量など）。
        - 日付の範囲と形式を元のデータと一致させる。

        3. 文字タイプの多様性を確保：
        - 適切な場合、大文字と小文字を混在させる。
        - 元々含まれていた場合、数字や特殊文字を含める。
        - 元のデータに存在する場合、アクセント文字や日本語以外の文字を使用。

        4. フィールド固有の特徴を維持：
        - 名前：多様な架空の名前を生成（長さや文化的起源の変化を含む）。
        - 住所：様々な形式の現実的な住所を作成（番地、マンション名、郵便番号など）。
        - メールアドレス：多様なドメイン名を持つ現実的なメールアドレス形式を生成。
        - 電話番号：一般的な形式と市外局番に従った番号を作成。

        5. データ関係の保持：
        - 関連フィールド間の論理的な接続を維持（生年月日と年齢など）。
        - 複数のレコードにまたがる繰り返し情報の一貫性を確保。

        6. 機密情報の匿名化：
        - すべての個人情報を架空のデータに置き換える。
        - 実際の金額を現実的だが無関係な金額に置き換える。

        7. 企業データの変更：
        - 企業名、ブランド名、商品名を架空のものに置き換える。
        - 業界や企業規模などの特徴を維持しつつ、識別不可能にする。

        8. 制御された変動性の導入：
        - システムの限界をテストするために、非常に長いまたは短いエントリなどのエッジケースを含める。
        - 元のデータに存在する場合、一部のレコードに欠損値またはヌル値を生成。

        9. 全体的なデータ分布の維持：
        - 数値フィールドの値の一般的な分布を再現（年齢層、収入帯など）。
        - カテゴリカルデータの頻度を保持（製品タイプ、顧客セグメントなど）。

        10. 日本語固有の特徴を考慮：
        - 氏名には適切な日本語の氏名を使用。
        - 住所には日本の住所形式を使用（都道府県、市区町村、丁目、番地など）。
        - 日本語の文字種（ひらがな、カタカナ、漢字）のバランスを元のデータと同様に保つ。

        11. 出力形式：
        - データ内容のみを出力し、説明や追加のテキストは含めない。
        - 各フィールドを適切な区切り文字（カンマ、タブなど）で区切り、一貫した形式を維持する。


        この指示に基づいてダミーデータを生成し、元のデータの機密性を保護しながら、システムを包括的にテストできるデータセットを作成してください。出力は直接データファイルとして使用できるよう、データ内容のみを生のcsvとして生成してください。
    """
    system_prompt = """
        Your task is to mimic a tool that generates dummy data for system testing. Replace sensitive information such as customer information, company data and monetary amounts with fictitious and realistic alternative data. Follow the guidelines below while maintaining the structure and characteristics of the original data:

        1. maintain data integrity:
         - Preserve the format of the original data (text, numbers, dates, etc.).
         - Maintain the same number of records as the original data set. 2.

        2. reproduce data patterns:
         - match the length range (minimum and maximum) of each field.
         - Maintain realistic ranges for numeric fields (age, price, quantity, etc.).
         - Match the range and format of dates to the original data. 3.

        3. ensure diversity of character types:
         - mix upper and lower case where appropriate.
         - Include numbers and special characters, if originally included.
         - Use accented or non-Japanese characters if present in the original data. 4.

        4. maintain field-specific characteristics:
         - Names: generate a variety of fictitious names (including variations in length and cultural origin).
         - Addresses: generate realistic addresses in a variety of formats (street numbers, apartment names, zip codes, etc.).
         - Email Addresses: Generate realistic email address formats with a variety of domain names.
         - Telephone numbers: Generate numbers according to common formats and area codes. 5.

        5. data relationship retention:
         - maintain logical connections between related fields (e.g., birth date and age).
         - Ensure consistency of repeated information across multiple records. 6.

        6. anonymizing sensitive information:
         - replacing all personal information with fictitious data.
         - Replace actual amounts with realistic but irrelevant amounts. 7.

        7. modification of company data:
         - replacing company names, brand names, and product names with fictitious ones.
         - 8. introduction of controlled variability:
         - make the company unidentifiable while maintaining characteristics such as industry, company size, etc.

        8. introducing controlled variability:
         - include edge cases, such as very long or short entries, to test the limits of the system.
         - Produce missing or null values for some records when present in the original data.

        9. maintaining overall data distribution:
         - reproducing the general distribution of values for numeric fields (age groups, income bands, etc.).
         - Maintain categorical data frequencies (product type, customer segment, etc.). 10.

        10. take into account Japanese-specific characteristics:
         - use appropriate Japanese names for names.
         - Use Japanese address format for addresses (e.g., prefecture, city, ward, town, street, house number).
         - Maintain the same balance of Japanese character types (hiragana, katakana, and kanji) as in the original data. 11.

        11. output format:
         - output only the data content, do not include descriptions or additional text.
         - Separate each field with an appropriate delimiter (comma, tab, etc.) to maintain a consistent format.

        Generate dummy data based on these instructions to create a data set that allows comprehensive testing of the system while protecting the confidentiality of the original data. Please generate only the data content as raw csv so that the output can be used directly as a data file
        Don't write Note.
    """
    
    jsondata = {
        "model": f"{model}",
        "prompt": f"System: {system_prompt}\n\nUser: Please convert the following data to dummy data according to the guidelines:\n\n{text}\n\n",
        "stream": False
    }

    max_retries = 5
    retry_delay = 5

    for attempt in range(max_retries):
        try:
            # print(f"url: {url}")
            # print(f"data: {data}")
            response = requests.post(url, json=jsondata, timeout=1200)
            # response = requests.post(url, data=data, timeout=100)
            response.raise_for_status()
            # print(f"response: {response.json()}")
            # print(f"\n\nresponse.result: {response.result}")
            
            result = ""
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    response_data = json.loads(decoded_line)
                    if 'response' in response_data:
                        result += response_data['response']
            return result
        except requests.exceptions.ConnectionError as e:
            print(f"Error connecting: {e}")
        except requests.exceptions.Timeout as e:
            print(f"Timeout error: {e}")
        except requests.exceptions.HTTPError as e:
                print(f"HTTP error occurred: {e}")
                print(f"URL: {url}")
                print(f"Data: {jsondata}")
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"Error connecting to Ollama. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                return f"Error: Failed to connect to Ollama after {max_retries} attempts. {str(e)}"

def process_file(input_file, output_file, model):
    print(f"Processing file: {input_file}")
    headers, data = read_csv_file(input_file)
    
    data_str = "\n".join([",".join(row) for row in data])
    
    result = process_with_ollama(data_str, model)
    # print(f"result: {result}")
    
    dummy_data = [row.split(',') for row in result.strip().split('\n')]
    
    write_csv_file(output_file, headers, dummy_data)
    print(f"Dummy data saved to: {output_file}")

def is_already_downloaded(model):
    url = "http://ollama:11434/api/show"
    data = f"""{{
        "name": "{model}"
    }}"""    
    response = requests.post(url, data=data)
    # print(response.text)  # レスポンスのテキストを確認
 
    try:
        # print(response.json())
        if "not found" in response.text:
            return False
        else:
            return True
    except json.decoder.JSONDecodeError as e:
        print(f"JSON デコード エラー: {e}")
        return True

def pull_model(model):
    print(f"Pulling model: {model}")
    url = "http://ollama:11434/api/pull"
    data = f"""{{
        "name": "{model}"
    }}"""
    response = requests.post(url, data=data)
    # print(response.json())
    print(f"Complete pull model: {model}")

def main(model=None):
    input_dir = "/app/input"
    output_dir = "/app/output"
    if not model:
        model = "7shi/tanuki-dpo-v1.0:8b-q6_K"
        model = "lucas2024/karakuri-lm-8x7b-instruct-v0.1:q5_k_m"
        model = "phi3.5"
        model = "phi3.5:3.8b-mini-instruct-q8_0"
        model = "7shi/borea-phi-3.5-coding:3.8b-mini-instruct-q6_K"
        model = "7shi/borea-phi-3.5-jp:3.8b-mini-instruct-q6_K"
    
    # input ディレクトリ内のファイルを処理
    for input_file in glob.glob(os.path.join(input_dir, '*')):
        # .git* ファイルは処理対象外
        if os.path.basename(input_file).startswith('.git'):
            continue

        filename = os.path.basename(input_file)
        name, ext = os.path.splitext(filename)
        output_file = os.path.join(output_dir, f"{name}_dummy{ext}")
        
        if not is_already_downloaded(model):
            pull_model(model)
        process_file(input_file, output_file, model)
    
    print("全ファイルの処理が完了しました。")

if __name__ == "__main__":
    import sys
    main(model=sys.argv[1])
