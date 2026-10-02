import os
import glob

def rename_music_files(target_dir="."):
    # 搜尋 target_dir 下所有子資料夾中的 .mp3 檔案
    search_pattern = os.path.join(target_dir, "**", "*.mp3")
    mp3_files = glob.glob(search_pattern, recursive=True)

    # 依照路徑與檔名排序，確保跨資料夾的順序一致
    mp3_files.sort()

    total_files = len(mp3_files)
    print(f"找到 {total_files} 個 MP3 檔案，準備開始重命名...\n")

    for index, old_path in enumerate(mp3_files, start=1):
        directory, filename = os.path.split(old_path)
        
        # 避免重複執行時疊加編號 (若開頭已經是數字加槓，如 "001-")
        # 如果需要重新編號，可先把舊的 3 位數前綴移除
        clean_filename = filename
        if len(filename) > 4 and filename[:3].isdigit() and filename[3] == '-':
            clean_filename = filename[4:]

        # 格式化為 3 位數字編號，例如 001, 002, ..., 145
        new_filename = f"{index:03d}-{clean_filename}"
        new_path = os.path.join(directory, new_filename)

        # 執行重命名
        if old_path != new_path:
            os.rename(old_path, new_path)
            print(f"[{index:03d}/{total_files:03d}] {filename} -> {new_filename}")
        else:
            print(f"[{index:03d}/{total_files:03d}] 已是正確檔名: {filename}")

    print("\n✅ 所有檔案已成功重新命名！")

if __name__ == "__main__":
    # 預設會在執行此腳本的當前目錄生效
    rename_music_files()