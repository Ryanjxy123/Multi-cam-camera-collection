from PIL import Image
import os, re

frames_dir = "./frames"
output_dir = "./frames_cropped"
os.makedirs(output_dir, exist_ok=True)

def get_num(filename):
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else -1

# 按文件名中的数字排序
png_files = sorted(
    [f for f in os.listdir(frames_dir) if f.lower().endswith(".png")],
    key=get_num
)

target_ratio = 16 / 9
target_size = (1280, 720)  # ✅ 目标分辨率（宽，高）

for idx, filename in enumerate(png_files):
    input_path = os.path.join(frames_dir, filename)
    img = Image.open(input_path)
    width, height = img.size
    current_ratio = width / height

    # === 比例裁剪 ===
    if abs(current_ratio - target_ratio) < 1e-3:
        img_cropped = img
    elif current_ratio > target_ratio:
        # 宽 > 高 → 按高度裁剪宽度（左右居中）
        new_width = round(height * target_ratio)
        left = (width - new_width) // 2
        img_cropped = img.crop((left, 0, left + new_width, height))
    else:
        # 高 > 宽 → 按宽度裁剪高度（上下居中）
        new_height = round(width / target_ratio)
        top = (height - new_height) // 2
        img_cropped = img.crop((0, top, width, top + new_height))

    # === 缩放到固定分辨率 ===
    img_resized = img_cropped.resize(target_size, Image.LANCZOS)

    new_w, new_h = img_resized.size
    assert (new_w, new_h) == target_size, f"{filename} 尺寸错误！"

    output_path = os.path.join(output_dir, f"{idx}.png")
    img_resized.save(output_path)
    print(f"已处理: {filename} → {output_path} ({new_w}x{new_h})")

print("✅ 全部图片裁剪并缩放完成！输出尺寸为 1280×720")
