from typing import List

def prepare_context_from_files(file_list: List[str]) -> str:
    """
    ファイルリストの各ファイルの内容を読み込み、LLMへのコンテキストとして整形した文字列を返します。
    各ファイルの内容はファイルパスのヘッダーで区切られます。
    """
    context_parts = []
    total_chars = 0
    
    print(f"Preparing context from {len(file_list)} files...")

    for file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # コンテキストのフォーマット
            # ファイルパスを明示して、どこからどこまでがそのファイルの内容かわかるようにする
            file_context = f"\n\n--- Start of File: {file_path} ---\n{content}\n--- End of File: {file_path} ---\n"
            context_parts.append(file_context)
            total_chars += len(file_context)
            
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            # エラーがあったファイルはスキップするか、エラー情報をコンテキストに含めるか
            # ここではエラー情報を少し含める
            context_parts.append(f"\n\n--- Error reading file: {file_path} ---\n{str(e)}\n")

    full_context = "".join(context_parts)
    print(f"Context preparation complete. Total characters: {total_chars}")
    return full_context
