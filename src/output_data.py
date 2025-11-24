import os
from datetime import datetime

def save_summary_to_file(summary: str, output_folder: str, api_name: str) -> bool:
    """
    LLMの要約結果をMarkdownファイルとして保存します。
    
    Args:
        summary: 保存する要約テキスト
        output_folder: 保存先フォルダパス
        api_name: 使用したAPI設定名（config.iniのセクション名、ファイル名に使用）
    
    Returns:
        bool: 保存成功時True、失敗時False
    """
    # フォルダ作成
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
            print(f"Created output folder: {output_folder}")
        except OSError as e:
            print(f"Error creating output folder: {e}")
            return False

    # ファイル名生成: YYYYMMDD-HHMM_summary_[api-name].md
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    # API名に含まれるファイルシステムで使用できない文字を置換
    safe_api_name = api_name.replace(":", "-").replace("/", "-").replace("\\", "-")
    filename = f"{timestamp}_summary_{safe_api_name}.md"
    output_path = os.path.join(output_folder, filename)
    
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"Summary saved to: {output_path}")
        return True
    except IOError as e:
        print(f"Error saving summary to file: {e}")
        return False
