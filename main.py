import sys
import os
import configparser
from datetime import datetime

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

# Output folder
output_folder = r"C:/Users/MakiNomiya/Documents/obsidian_local/50_ActivityReport"
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
        # ユーザーの設定に合わせてセクション名を指定
        target_section = 'ollama-gemma3n'
        
        if config and target_section in config:
            base_url = config[target_section].get('base_url', 'http://localhost:11434')
            model = config[target_section].get('model', 'gemma3n:e4b')
            
            print(f"\n--- Generating Summary with Ollama ({model}) ---")
            summary = generate_summary_with_ollama(context_data, base_url, model)
            
            print("\n=== Summary Result ===")
            print(summary)
            print("======================\n")

            # 7. 結果保存
            if summary and not summary.startswith("Error"):
                # フォルダ作成
                if not os.path.exists(output_folder):
                    try:
                        os.makedirs(output_folder)
                        print(f"Created output folder: {output_folder}")
                    except OSError as e:
                        print(f"Error creating output folder: {e}")
                        return

                # ファイル名生成: YYYYMMDD-HHMM_summary_[model-name].md
                timestamp = datetime.now().strftime("%Y%m%d-%H%M")
                # モデル名に含まれるファイルシステムで使用できない文字を置換
                safe_model_name = model.replace(":", "-").replace("/", "-").replace("\\", "-")
                filename = f"{timestamp}_summary_{safe_model_name}.md"
                output_path = os.path.join(output_folder, filename)
                
                try:
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(summary)
                    print(f"Summary saved to: {output_path}")
                except IOError as e:
                    print(f"Error saving summary to file: {e}")

        else:
            print(f"Config file (config.ini) not found or [{target_section}] section missing. Skipping summary generation.")

if __name__ == "__main__":
    main()
