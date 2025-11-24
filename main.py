import sys
import os

# --- 設定 ---
# Obsidian Vaultのフルパス
path_vault = r"C:/Users/MakiNomiya/Documents/obsidian_local" 

# フィルタリング条件
# 処理対象にしたいフォルダ名（パスの一部に含まれていれば対象）
included_folders = [] 

# 除外したいフォルダ名（パスの一部に含まれていれば除外）
excluded_folders = [".obsidian", ".trash", "99_temp", "98_secret"]

# 更新期間（日数）
days = 7

# Output folder
output_folder = r"C:/Users/MakiNomiya/Documents/obsidian_local/50_ActivityReport"

# LLM API設定名リスト（config.iniのセクション名を複数指定可能）
api_names = ['ollama-gemma3n', 'ollama-gptoss']
# -----------

# srcディレクトリをパスに追加してインポートできるようにする
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from obsidian_ops import (
    get_md_files,
    filter_by_included_folders,
    filter_by_excluded_folders,
    filter_by_recent_update
)
from llm_utils import prepare_context_from_files
from execute import execute_llm_summary

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

    # LLM処理対象ファイルリスト出力
    print("\n--- LLM Processing List of Files ---")
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
        
        # 6. LLM要約実行（複数API対応）
        for api_name in api_names:
            print(f"\n{'='*60}")
            print(f"Processing with API: {api_name}")
            print(f"{'='*60}")
            execute_llm_summary(context_data, api_name, output_folder)


if __name__ == "__main__":
    main()
