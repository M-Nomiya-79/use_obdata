# use_obdata

A tool to filter and aggregate Markdown files within an Obsidian Vault.
It extracts and lists files based on specified conditions such as folder inclusion, folder exclusion, and update period.
It also generates a context string from the filtered files, suitable for input into Large Language Models (LLMs).

## Folder and File Structure

```text
.
├── main.py                 # Entry point (configuration and execution)
├── src/
│   ├── obsidian_ops.py     # Filtering logic implementation
│   └── llm_utils.py        # LLM context generation utilities
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

It executes the filtering process and then generates a preview of the LLM context.

### `src/obsidian_ops.py`
Contains the core logic for file operations and filtering.
- `get_md_files`: Retrieves all Markdown files in the Vault
- `filter_by_included_folders`: Extracts files contained in specified folders
- `filter_by_excluded_folders`: Excludes files contained in specified folders
- `filter_by_recent_update`: Extracts files updated recently

### `src/llm_utils.py`
Utilities for preparing data for LLMs.
- `prepare_context_from_files`: Reads the content of the filtered files and formats them into a single context string with headers/footers, making it ready for LLM consumption.

## Usage

This project uses [uv](https://github.com/astral-sh/uv) as the Python package manager.

### 1. Setup Virtual Environment and Install Dependencies

Run the following command in the project root directory to set up the environment.

```bash
uv sync
```

### 2. Execution

After setup is complete, run the script with the following command.

```bash
uv run main.py
```

> **Note**
> Please update `path_vault` in `main.py` to match your environment before running.
