# use_obdata

Obsidian Vault内のMarkdownファイルをフィルタリング・集計するツールです。
指定した条件（フォルダ包含、フォルダ除外、更新期間）に基づいてファイルを抽出し、リストアップします。

## フォルダ・ファイル構成

```text
.
├── main.py                 # エントリーポイント（設定と実行）
├── src/
│   └── obsidian_ops.py     # フィルタリングロジック実装
├── pyproject.toml          # プロジェクト設定・依存関係定義
├── uv.lock                 # 依存関係ロックファイル
└── README.md               # 本ドキュメント
```

## ファイル概要

### `main.py`
本ツールの実行ファイルです。以下の設定変数を編集して使用します。
- `path_vault`: Obsidian Vaultのルートパス
- `included_folders`: 処理対象とするフォルダ名のリスト
- `excluded_folders`: 除外対象とするフォルダ名のリスト
- `days`: 抽出対象とする更新期間（日数）

### `src/obsidian_ops.py`
ファイル操作とフィルタリングのコアロジックが含まれています。
- `get_md_files`: Vault内の全Markdownファイルを取得
- `filter_by_included_folders`: 指定フォルダに含まれるファイルを抽出
- `filter_by_excluded_folders`: 指定フォルダに含まれるファイルを除外
- `filter_by_recent_update`: 最近更新されたファイルを抽出

## 実行方法

本プロジェクトはPythonパッケージマネージャーとして [uv](https://github.com/astral-sh/uv) を使用しています。

### 1. 仮想環境の構築と依存関係のインストール

プロジェクトのルートディレクトリで以下のコマンドを実行し、環境をセットアップします。

```bash
uv sync
```

### 2. 実行

セットアップ完了後、以下のコマンドでスクリプトを実行します。

```bash
uv run main.py
```

> **Note**
> 実行前に `main.py` 内の `path_vault` をご自身の環境に合わせて変更してください。
