import os
import shutil
from datetime import datetime


def log_message(message):
    """
    ログを見やすく表示する関数
    時刻つきで表示する
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {message}")


def get_file_category(filename, file_types):
    """
    ファイル名から分類先のフォルダ名を返す
    該当しない場合は「その他」を返す
    """
    lower_name = filename.lower()

    for folder_name, extensions in file_types.items():
        if folder_name == "その他":
            continue

        for ext in extensions:
            if lower_name.endswith(ext):
                return folder_name

    return "その他"


def make_unique_path(file_path):
    """
    同名ファイルが存在する場合、
    自動で (1), (2), (3)... を付けて別名にする
    """
    if not os.path.exists(file_path):
        return file_path

    folder = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    name, ext = os.path.splitext(filename)

    counter = 1
    while True:
        new_filename = f"{name}({counter}){ext}"
        new_path = os.path.join(folder, new_filename)

        if not os.path.exists(new_path):
            return new_path

        counter += 1


def move_file_safely(source_path, dest_folder):
    """
    ファイルを安全に移動する
    同名があれば別名に変更してから移動する
    """
    os.makedirs(dest_folder, exist_ok=True)

    filename = os.path.basename(source_path)
    dest_path = os.path.join(dest_folder, filename)

    safe_dest_path = make_unique_path(dest_path)

    shutil.move(source_path, safe_dest_path)
    return safe_dest_path


def organize_files(target_folder, file_types):
    """
    指定フォルダ内のファイルを分類して移動するメイン処理
    """
    if not os.path.exists(target_folder):
        raise FileNotFoundError(f"指定したフォルダが存在しません: {target_folder}")

    if not os.path.isdir(target_folder):
        raise NotADirectoryError(f"指定したパスはフォルダではありません: {target_folder}")

    log_message("ファイル整理を開始します")
    log_message(f"対象フォルダ: {target_folder}")

    file_count = 0
    moved_count = 0
    error_count = 0

    try:
        items = os.listdir(target_folder)
    except Exception as e:
        raise Exception(f"フォルダの中身を取得できませんでした: {e}")

    for filename in items:
        source_path = os.path.join(target_folder, filename)

        if not os.path.isfile(source_path):
            continue

        file_count += 1

        try:
            category = get_file_category(filename, file_types)
            dest_folder = os.path.join(target_folder, category)

            moved_path = move_file_safely(source_path, dest_folder)

            log_message(f"移動成功: {filename} → {moved_path}")
            moved_count += 1

        except Exception as e:
            log_message(f"エラー: {filename} の移動に失敗しました")
            log_message(f"詳細: {e}")
            error_count += 1

    log_message("ファイル整理が完了しました")
    log_message(f"処理対象ファイル数: {file_count}")
    log_message(f"移動成功数: {moved_count}")
    log_message(f"エラー数: {error_count}")


def main():
    """
    ここを自分の環境に合わせて書き換えて使う
    """
    target_folder = r"ここに整理したいフォルダのパスを入力"

    file_types = {
        "画像": [".jpg", ".png", ".jpeg", ".gif", ".bmp", ".webp"],
        "動画": [".mp4", ".mov", ".avi", ".mkv"],
        "ドキュメント": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
        "その他": []
    }

    try:
        organize_files(target_folder, file_types)
    except Exception as e:
        log_message("重大なエラーが発生しました")
        log_message(f"詳細: {e}")


if __name__ == "__main__":
    main()