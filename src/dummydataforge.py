import requests
import json
import csv
import os
import time
import glob
import yaml

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

def read_system_prompt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def process_with_ollama(text, model="phi3.5"):
    url = "http://ollama:11434/api/generate"

    system_prompt = read_system_prompt('/app/config/system_prompt.txt')
    
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
        model = "qwen2.5"
    
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
    main(model=sys.argv[1] if len(sys.argv) > 1 else None)
