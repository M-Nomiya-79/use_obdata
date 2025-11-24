import sys
import os
import configparser

# --- 設定 ---
# Obsidian Vaultのフルパス
path_vault = r"C:/Users/MakiNomiya/Documents/obsidian_local" 

# フィルタリング条件
# 処理対象にしたいフォルダ名（パスの一部に含まれていれば対象）
included_folders = [] 

# 除外したいフォルダ名（パスの一部に含まれていれば除外）
excluded_folders = [".obsidian", ".trash", "99_temp"]

# 更新期間（日数）
days = 7
# -----------

# srcディレクトリをパスに追加してインポートできるようにする
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from obsidian_ops import (
    get_md_files,
    filter_by_included_folders,
    filter_by_excluded_folders,
    filter_by_recent_update
)
from llm_utils import prepare_context_from_files, generate_summary_with_ollama

def load_config():
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    if os.path.exists(config_path):
        config.read(config_path)
        return config
    return None

def main():
    print(f"--- Processing Vault: {path_vault} ---")

    # 1. 全.mdファイル取得
    md_files = get_md_files(path_vault)

    # 2. 包含フォルダフィルタ
    md_files = filter_by_included_folders(md_files, included_folders)

    # 3. 除外フォルダフィルタ
    md_files = filter_by_excluded_folders(md_files, excluded_folders)

    # 4. 更新期間フィルタ
    md_files = filter_by_recent_update(md_files, days)

    # 最終結果出力
    print("\n--- Final List of Files ---")
    for file_path in md_files:
        print(file_path)
    print(f"Total files in final list: {len(md_files)}")

    # 5. コンテキスト作成
    if md_files:
        print("\n--- Generating Context ---")
        context_data = prepare_context_from_files(md_files)
        
        # 確認のため、先頭500文字だけ表示
        print("\n--- Context Preview (First 500 chars) ---")
        print(context_data[:500])
        print("...\n")
        
        # 6. Ollamaで要約生成
        config = load_config()
        if config and 'OLLAMA' in config:
            base_url = config['OLLAMA'].get('base_url', 'http://localhost:11434')
            model = config['OLLAMA'].get('model', 'gemma3n:e4b')
            
            print(f"\n--- Generating Summary with Ollama ({model}) ---")
            summary = generate_summary_with_ollama(context_data, base_url, model)
            
            print("\n=== Summary Result ===")
            print(summary)
            print("======================\n")
        else:
            print("Config file (config.ini) not found or OLLAMA section missing. Skipping summary generation.")

if __name__ == "__main__":
    main()
