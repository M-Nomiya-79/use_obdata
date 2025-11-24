# use_obdata

Obsidian Vault内のMarkdownファイルをフィルタリング・集計するツールです。
指定した条件（フォルダ包含、フォルダ除外、更新期間）に基づいてファイルを抽出し、リストアップします。
また、抽出したファイルの内容を結合し、ローカルLLM（Ollama）を使用して要約を生成・保存する機能も備えています。

## フォルダ・ファイル構成

```text
.
├── main.py                 # エントリーポイント（設定と実行）
├── config.ini              # LLM設定用ファイル（Git管理対象外）
├── src/
│   ├── obsidian_ops.py     # フィルタリングロジック実装
│   └── llm_utils.py        # LLMコンテキスト生成・API連携ユーティリティ
├── pyproject.toml          # プロジェクト設定・依存関係定義
├── uv.lock                 # 依存関係ロックファイル
├── README.md               # ドキュメント（英語）
└── README_JA.md            # 本ドキュメント（日本語）
```

## ファイル概要

### `main.py`
本ツールの実行ファイルです。以下の設定変数を編集して使用します。
- `path_vault`: Obsidian Vaultのルートパス
- `included_folders`: 処理対象とするフォルダ名のリスト
- `excluded_folders`: 除外対象とするフォルダ名のリスト
- `days`: 抽出対象とする更新期間（日数）
- `output_folder`: 要約ファイルの保存先フォルダパス

フィルタリング処理を実行した後、LLM用コンテキストを生成し、Ollamaに要約をリクエストして結果をMarkdownファイルとして保存します。

### `config.ini`
Ollama APIの設定ファイルです。ルートディレクトリに作成してください。
設定例:
```ini
[ollama-gemma3n]
base_url = http://localhost:11434
model = gemma3n:e4b
```

### `src/obsidian_ops.py`
ファイル操作とフィルタリングのコアロジックが含まれています。
- `get_md_files`: Vault内の全Markdownファイルを取得
- `filter_by_included_folders`: 指定フォルダに含まれるファイルを抽出
- `filter_by_excluded_folders`: 指定フォルダに含まれるファイルを除外
- `filter_by_recent_update`: 最近更新されたファイルを抽出

### `src/llm_utils.py`
LLM向けのデータ準備とAPI連携を行うユーティリティです。
- `prepare_context_from_files`: ファイル内容を整形してコンテキスト文字列を作成します。
- `generate_summary_with_ollama`: コンテキストをOllamaに送信し、要約を取得します。

## 実行方法

本プロジェクトはPythonパッケージマネージャーとして [uv](https://github.com/astral-sh/uv) を使用しています。

### 1. 仮想環境の構築と依存関係のインストール

プロジェクトのルートディレクトリで以下のコマンドを実行し、環境をセットアップします。

```bash
uv sync
```

### 2. 設定

1.  `main.py` 内の `path_vault` と `output_folder` をご自身の環境に合わせて変更してください。
2.  `config.ini` を作成し、Ollamaの設定を行ってください。

### 3. 実行

以下のコマンドでスクリプトを実行します。

```bash
uv run main.py
```

要約結果は `output_folder` に `YYYYMMDD-HHMM_summary_[model-name].md` という形式のファイル名で保存されます。
