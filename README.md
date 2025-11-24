# use_obdata

A tool to filter and aggregate Markdown files within an Obsidian Vault.
It extracts and lists files based on specified conditions such as folder inclusion, folder exclusion, and update period.
It also generates a context string from the filtered files, sends it to a local LLM (Ollama) for summarization, and saves the result.

## Folder and File Structure

```text
.
├── main.py                 # Entry point (configuration and execution)
├── config.ini              # Configuration file for LLM settings (not tracked by git)
├── src/
│   ├── obsidian_ops.py     # Filtering logic implementation
│   └── llm_utils.py        # LLM context generation and API utilities
├── pyproject.toml          # Project configuration and dependency definitions
├── uv.lock                 # Dependency lock file
├── README.md               # This document (English)
└── README_JA.md            # Documentation (Japanese)
```

## File Overview

### `main.py`
The executable file for this tool. Edit the following configuration variables before use:
- `path_vault`: Root path of your Obsidian Vault
- `included_folders`: List of folder names to include in processing
- `excluded_folders`: List of folder names to exclude from processing
- `days`: Update period (in days) to filter files by
- `output_folder`: Directory path where summary files will be saved

It executes the filtering process, generates an LLM context, requests a summary from Ollama, and saves the result to a Markdown file.

### `config.ini`
Configuration file for Ollama API settings. Create this file in the root directory.
Example:
```ini
[ollama-gemma3n]
base_url = http://localhost:11434
model = gemma3n:e4b
```

### `src/obsidian_ops.py`
Contains the core logic for file operations and filtering.
- `get_md_files`: Retrieves all Markdown files in the Vault
- `filter_by_included_folders`: Extracts files contained in specified folders
- `filter_by_excluded_folders`: Excludes files contained in specified folders
- `filter_by_recent_update`: Extracts files updated recently

### `src/llm_utils.py`
Utilities for preparing data for LLMs and interacting with the API.
- `prepare_context_from_files`: Formats file content into a single context string.
- `generate_summary_with_ollama`: Sends the context to Ollama and retrieves the summary.

## Usage

This project uses [uv](https://github.com/astral-sh/uv) as the Python package manager.

### 1. Setup Virtual Environment and Install Dependencies

Run the following command in the project root directory to set up the environment.

```bash
uv sync
```

### 2. Configuration

1.  Update `path_vault` and `output_folder` in `main.py` to match your environment.
2.  Create `config.ini` and configure your Ollama settings.

### 3. Execution

Run the script with the following command.

```bash
uv run main.py
```

The summary will be saved in the `output_folder` with a filename like `YYYYMMDD-HHMM_summary_[model-name].md`.
