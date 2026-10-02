import os
import shutil
import glob

def reorder_for_portable_player(src_dir=".", output_dir="../YouTube_Fixed"):
    # 搜尋所有 MP3 檔案
    search_pattern = os.path.join(src_dir, "**", "*.mp3")
    mp3_files = glob.glob(search_pattern, recursive=True)

    # 嚴格按檔名排序 (001 -> 002 -> ... -> 145)
    mp3_files.sort()

    total_files = len(mp3_files)
    print(f"找到 {total_files} 個 MP3 檔案，開始依順序重新寫入至: {output_dir}\n")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for index, old_path in enumerate(mp3_files, start=1):
        filename = os.path.basename(old_path)
        new_path = os.path.join(output_dir, filename)

        # 按照 001, 002, 003... 的順序逐一複製寫入
        shutil.copy2(old_path, new_path)
        print(f"[{index:03d}/{total_files:03d}] 寫入: {filename}")

    print(f"\n✅ 完成！請將「{output_dir}」資料夾內的檔案拷貝至您的可攜式收音機/隨身碟中。")

if __name__ == "__main__":
    reorder_for_portable_player()