import os
import time
from datetime import datetime, timedelta
from typing import List

def get_md_files(vault_path: str) -> List[str]:
    """
    指定されたVaultパス内のすべての.mdファイルを取得し、リストとして返します。
    件数を標準出力します。
    """
    md_files = []
    if not os.path.exists(vault_path):
        print(f"Error: Vault path '{vault_path}' does not exist.")
        return []

    for root, dirs, files in os.walk(vault_path):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    
    print(f"Total .md files found: {len(md_files)}")
    return md_files

def filter_by_included_folders(file_list: List[str], included_folders: List[str]) -> List[str]:
    """
    指定されたフォルダリストに含まれるファイルのみをフィルタリングします。
    更新されたリストを返し、件数を標準出力します。
    included_foldersが空の場合はフィルタリングを行いません。
    """
    if not included_folders:
        print(f"No inclusion filter applied. Count: {len(file_list)}")
        return file_list

    filtered_files = []
    # フォルダパスの正規化（OS依存の区切り文字に対応するため）
    normalized_includes = [os.path.normpath(f) for f in included_folders]
    
    for file_path in file_list:
        # ファイルパスが指定されたフォルダのいずれかを含んでいるか確認
        # 単純な文字列部分一致だと誤検知の可能性があるため、パスセパレータを考慮するか、
        # あるいは相対パスで判定するのがより厳密ですが、
        # ここではユーザーの意図（フォルダリストに含まれる）を「パスの一部にフォルダ名が含まれる」と解釈するか、
        # 「そのフォルダ配下にある」と解釈するか。
        # 通常は「そのフォルダ配下」なので、パスの包含関係をチェックします。
        
        is_included = False
        for folder in normalized_includes:
            # フォルダ名がパスの一部に含まれているか（簡易チェック）
            # より厳密には: if folder in file_path (ただしパス区切りを意識)
            if folder in file_path: 
                is_included = True
                break
        
        if is_included:
            filtered_files.append(file_path)

    print(f"Files after inclusion filter: {len(filtered_files)}")
    return filtered_files

def filter_by_excluded_folders(file_list: List[str], excluded_folders: List[str]) -> List[str]:
    """
    指定された除外フォルダリストに含まれるファイルを除外します。
    更新されたリストを返し、件数を標準出力します。
    """
    if not excluded_folders:
        print(f"No exclusion filter applied. Count: {len(file_list)}")
        return file_list

    filtered_files = []
    normalized_excludes = [os.path.normpath(f) for f in excluded_folders]

    for file_path in file_list:
        is_excluded = False
        for folder in normalized_excludes:
            if folder in file_path:
                is_excluded = True
                break
        
        if not is_excluded:
            filtered_files.append(file_path)

    print(f"Files after exclusion filter: {len(filtered_files)}")
    return filtered_files

def filter_by_recent_update(file_list: List[str], days: int) -> List[str]:
    """
    指定された期間（days）内に更新されたファイルのみをフィルタリングします。
    更新されたリストを返し、件数を標準出力します。
    """
    filtered_files = []
    now = time.time()
    cutoff_time = now - (days * 86400) # 86400 seconds in a day

    for file_path in file_list:
        try:
            mtime = os.path.getmtime(file_path)
            if mtime >= cutoff_time:
                filtered_files.append(file_path)
        except OSError as e:
            print(f"Error accessing file {file_path}: {e}")

    print(f"Files updated in the last {days} days: {len(filtered_files)}")
    return filtered_files
