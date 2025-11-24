import sys
import os

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

if __name__ == "__main__":
    main()
