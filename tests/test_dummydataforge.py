import pytest
import os
import csv
from unittest.mock import patch, MagicMock
from src.dummydataforge import read_csv_file, write_csv_file, read_system_prompt, process_with_ollama, process_file, is_already_downloaded, pull_model
import json

@pytest.fixture
def sample_csv_file(tmp_path):
    file_path = tmp_path / "sample.csv"
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['名前', '年齢', '職業'])
        writer.writerow(['山田太郎', '30', '会社員'])
        writer.writerow(['佐藤花子', '25', '学生'])
    return file_path

def test_read_csv_file(sample_csv_file):
    headers, data = read_csv_file(sample_csv_file)
    assert headers == ['名前', '年齢', '職業']
    assert data == [['山田太郎', '30', '会社員'], ['佐藤花子', '25', '学生']]

def test_write_csv_file(tmp_path):
    output_file = tmp_path / "output.csv"
    headers = ['名前', '年齢', '職業']
    data = [['鈴木一郎', '35', '自営業'], ['田中美香', '28', 'デザイナー']]
    write_csv_file(output_file, headers, data)
    
    with open(output_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        read_headers = next(reader)
        read_data = list(reader)
    
    assert read_headers == headers
    assert read_data == data

def test_read_system_prompt(tmp_path):
    prompt_file = tmp_path / "system_prompt.txt"
    prompt_content = "これはテスト用のシステムプロンプトです。"
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt_content)
    
    result = read_system_prompt(prompt_file)
    assert result == prompt_content

@patch('src.dummydataforge.requests.post')
def test_process_with_ollama(mock_post):
    mock_response = MagicMock()
    mock_response.iter_lines.return_value = [json.dumps({"response": "ダミーデータ1\nダミーデータ2"}).encode('utf-8')]
    mock_post.return_value = mock_response

    result = process_with_ollama("テストデータ", model="test_model")
    assert result == "ダミーデータ1\nダミーデータ2"

@patch('src.dummydataforge.process_with_ollama')
def test_process_file(mock_process_with_ollama, sample_csv_file, tmp_path):
    mock_process_with_ollama.return_value = "ダミー太郎,40,エンジニア\nダミー花子,35,医師"
    output_file = tmp_path / "output_dummy.csv"
    
    process_file(sample_csv_file, output_file, "test_model")
    
    headers, data = read_csv_file(output_file)
    assert headers == ['名前', '年齢', '職業']
    assert data == [['ダミー太郎', '40', 'エンジニア'], ['ダミー花子', '35', '医師']]

@patch('src.dummydataforge.requests.post')
def test_is_already_downloaded(mock_post):
    mock_post.return_value.text = '{"status": "success"}'
    assert is_already_downloaded("test_model") == True

    mock_post.return_value.text = '{"error": "model not found"}'
    assert is_already_downloaded("non_existent_model") == False

@patch('src.dummydataforge.requests.post')
def test_pull_model(mock_post):
    mock_post.return_value.json.return_value = {"status": "success"}
    pull_model("test_model")
    mock_post.assert_called_once()

if __name__ == "__main__":
    pytest.main()