import os
import shutil
import glob

def rename_and_reorder_tracks(src_dir=".", output_dir="../YouTube_Fixed_101_245", start_num=101):
    # 搜尋所有 .mp3 檔案
    search_pattern = os.path.join(src_dir, "**", "*.mp3")
    mp3_files = glob.glob(search_pattern, recursive=True)

    # 依原始路徑與檔名排序，確保 145 首歌曲順序不變
    mp3_files.sort()

    total_files = len(mp3_files)
    end_num = start_num + total_files - 1
    print(f"找到 {total_files} 個 MP3 檔案，準備將編號改為 {start_num} ~ {end_num} 並寫入至: {output_dir}\n")

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    for index, old_path in enumerate(mp3_files, start=start_num):
        filename = os.path.basename(old_path)

        # 清除舊有的 3 位數前綴 (例如 "001-")
        clean_filename = filename
        if len(filename) > 4 and filename[:3].isdigit() and filename[3] == '-':
            clean_filename = filename[4:]

        # 產生新的檔名 (101-婉曲 - ..., 102-..., 到 245-...)
        new_filename = f"{index:03d}-{clean_filename}"
        new_path = os.path.join(output_dir, new_filename)

        # 按順序寫入新檔案 (確保 FAT32 檔案目錄條目順序正確)
        shutil.copy2(old_path, new_path)
        print(f"[{index:03d}/{end_num}] {filename} -> {new_filename}")

    print(f"\n✅ 處理完成！請將「{os.path.abspath(output_dir)}」內的檔案複製到可攜式收音機/隨身碟中。")

if __name__ == "__main__":
    rename_and_reorder_tracks()