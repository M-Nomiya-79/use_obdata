from typing import List
import requests
import json

def prepare_context_from_files(file_list: List[str]) -> str:
    """
    ファイルリストの各ファイルの内容を読み込み、LLMへのコンテキストとして整形した文字列を返します。
    各ファイルの内容はファイルパスのヘッダーで区切られます。
    """
    context_parts = []
    total_chars = 0
    
    print(f"Preparing context from {len(file_list)} files...")

    for file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # コンテキストのフォーマット
            # ファイルパスを明示して、どこからどこまでがそのファイルの内容かわかるようにする
            file_context = f"\n\n--- Start of File: {file_path} ---\n{content}\n--- End of File: {file_path} ---\n"
            context_parts.append(file_context)
            total_chars += len(file_context)
            
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            # エラーがあったファイルはスキップするか、エラー情報をコンテキストに含めるか
            # ここではエラー情報を少し含める
            context_parts.append(f"\n\n--- Error reading file: {file_path} ---\n{str(e)}\n")

    full_context = "".join(context_parts)
    print(f"Context preparation complete. Total characters: {total_chars}")
    return full_context

def generate_summary_with_ollama(context: str, base_url: str, model: str) -> str:
    """
    Ollama APIを使用して、与えられたコンテキストの要約を生成します。
    """
    prompt = f"""
以下のテキストは、Obsidian Vaultから抽出された複数のMarkdownファイルの内容です。
これらのファイルの内容を統合して、重要なポイントを日本語で要約してください。
ファイルごとの区切りは '--- Start of File: ... ---' で示されています。

# コンテキストデータ
{context}

# 指示
上記の内容を要約してください。
"""
    
    url = f"{base_url}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    print(f"Sending request to Ollama ({url}) with model '{model}'...")
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return result.get("response", "No response field in JSON")
        
    except requests.exceptions.RequestException as e:
        return f"Error communicating with Ollama: {e}"
