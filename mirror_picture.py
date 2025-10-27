import os
import re
from PIL import Image, ImageOps

def natural_sort_key(filename):
    """
    自然排序的key函数，确保数字按照数值大小排序
    例如：0.png, 1.png, 2.png, ..., 10.png, 11.png
    """
    # 将文件名分割成数字和非数字部分
    parts = re.split(r'(\d+)', filename)
    # 将数字部分转换为整数进行比较
    return [int(part) if part.isdigit() else part for part in parts]

def mirror_images(input_folder, output_folder):
    """
    将输入文件夹中的所有图片进行左右镜像，并保存到输出文件夹
    按照文件名的数字顺序进行处理
    :param input_folder: 输入图片文件夹路径
    :param output_folder: 输出图片文件夹路径
    """
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 获取所有图片文件
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    image_files = [f for f in os.listdir(input_folder) 
                   if f.lower().endswith(image_extensions)]
    
    # 按照自然顺序排序（确保0.png, 1.png, 2.png...10.png的正确顺序）
    image_files.sort(key=natural_sort_key)
    
    # 按顺序处理每个图片
    for idx, filename in enumerate(image_files):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        try:
            # 打开图片
            img = Image.open(input_path)
            
            # 左右镜像
            mirrored_img = ImageOps.mirror(img)
            
            # 保存镜像图片
            mirrored_img.save(output_path)
            
            print(f"已处理 [{idx + 1}/{len(image_files)}]: {filename}")
            
        except Exception as e:
            print(f"处理 {filename} 时出错: {e}")
    
    print(f"\n处理完成！共处理 {len(image_files)} 张图片")

if __name__ == "__main__":
    input_folder = "./frames_cropped"          # 原始图片所在文件夹
    output_folder = "./frames_mirror"  # 镜像图片保存文件夹
    
    mirror_images(input_folder, output_folder)
    print("所有图片镜像完成！")