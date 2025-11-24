import configparser
import os
from llm_utils import generate_summary_with_ollama
from output_data import save_summary_to_file

def load_config(config_path: str = None):
    """
    config.iniファイルを読み込みます。
    
    Args:
        config_path: 設定ファイルのパス（指定しない場合はプロジェクトルートのconfig.ini）
    
    Returns:
        ConfigParser: 設定オブジェクト、ファイルが存在しない場合はNone
    """
    if config_path is None:
        # デフォルトではプロジェクトルートのconfig.iniを参照
        script_dir = os.path.dirname(os.path.dirname(__file__))
        config_path = os.path.join(script_dir, 'config.ini')
    
    config = configparser.ConfigParser()
    if os.path.exists(config_path):
        config.read(config_path)
        return config
    return None

def execute_llm_summary(context_data: str, api_name: str, output_folder: str, config_path: str = None) -> bool:
    """
    LLM APIを使用してコンテキストの要約を生成し、ファイルに保存します。
    
    Args:
        context_data: LLMに送信するコンテキストデータ
        api_name: config.iniのセクション名（例: 'ollama-gemma3n'）
        output_folder: 要約ファイルの保存先フォルダ
        config_path: 設定ファイルのパス（オプション）
    
    Returns:
        bool: 処理成功時True、失敗時False
    """
    config = load_config(config_path)
    
    if not config or api_name not in config:
        print(f"Config file (config.ini) not found or [{api_name}] section missing. Skipping summary generation.")
        return False
    
    base_url = config[api_name].get('base_url', 'http://localhost:11434')
    model = config[api_name].get('model', 'gemma3n:e4b')
    
    print(f"\n--- Generating Summary with Ollama ({model}) ---")
    summary = generate_summary_with_ollama(context_data, base_url, model)
    
    print("\n=== Summary Result ===")
    print(summary)
    print("======================\n")

    # 結果保存
    if summary and not summary.startswith("Error"):
        return save_summary_to_file(summary, output_folder, model)
    else:
        print("Summary generation failed or returned an error.")
        return False
