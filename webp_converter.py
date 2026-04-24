import os
import sys
from PIL import Image
from plyer import notification

def main():
    # 獲取拖曳進來的檔案路徑列表
    input_files = sys.argv[1:]

    if not input_files:
        print("請直接將圖片檔案拖拽到此圖示上！")
        return

    # 1. 定義桌面輸出路徑
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    output_folder = os.path.join(desktop_path, "WebP_Converted")

    # 2. 檢查並建立資料夾
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    converted_count = 0

    for file_path in input_files:
        try:
            file_name, file_ext = os.path.splitext(os.path.basename(file_path))
            
            # 排除非圖片格式
            if file_ext.lower() not in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
                continue

            # 3. 處理圖片
            with Image.open(file_path) as img:
                # 轉為 RGB (避免 PNG 透明層在某些狀況下報錯，或保持 WebP 兼容性)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGBA")
                else:
                    img = img.convert("RGB")

                # 4. 壓縮邏輯：檢查檔案大小
                file_size = os.path.getsize(file_path)
                # 若超過 1MB (1,048,576 Bytes)，品質設為 75，否則 90
                quality = 70 if file_size > 1024 * 1024 else 90

                # 5. 儲存
                save_path = os.path.join(output_folder, f"{file_name}.webp")
                img.save(save_path, "WEBP", quality=quality, method=6)
                converted_count += 1

        except Exception as e:
            print(f"錯誤: {file_path} 轉換失敗 - {e}")

        if converted_count > 0:
         os.startfile(output_folder)

if __name__ == "__main__":
    main()
