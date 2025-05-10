# MIT License
# Copyright (c) 2025 星灿长风v


from stv_ascii_art.utils.utils import *


def save_ascii_text(ascii_art, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        # 每行末尾添加颜色重置代码
        processed = "\n".join([line + "\033[0m" for line in ascii_art.split("\n")])
        f.write(processed)


def save_ascii_image(image, path):
    """2-1/2-2: 保存ASCII图片"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    image.save(path)


def handle_image(input_path, output_path=None, enhanced=False, use_gpu=False, fixed_size=None):
    """图片处理入口"""
    try:
        img = Image.open(input_path).convert("RGB")
    except FileNotFoundError:
        print(f"文件未找到: {input_path}")
        return

    # A-1/A-2: GPU加速
    if use_gpu and check_cuda()[0]:
        img = img.convert("RGB")
        tensor = transforms.ToTensor()(img).cuda()
        img = transforms.ToPILImage()(tensor.cpu())

    ascii_art, resized_img = convert_frame(img, enhanced, fixed_size=None)
    print("\n".join([line + "\033[0m" for line in ascii_art.split("\n")]))

    # 保存输出
    if output_path is None:
        output_dir = os.path.join(os.getcwd(), DEFAULT_OUTPUT_DIR)
        filename = f"{os.path.splitext(os.path.basename(input_path))[0]}_ascii.png"
        output_path = os.path.join(output_dir, filename)

    save_ascii_image(resized_img, output_path)
    print(f"已保存图片到: {output_path}")

    # 新增：保存ANSI文本文件
    text_output_dir = os.path.join(os.getcwd(), DEFAULT_OUTPUT_DIR, "ANSI")
    text_filename = f"{os.path.splitext(os.path.basename(input_path))[0]}_ansi.txt"
    text_output_path = os.path.join(text_output_dir, text_filename)
    save_ascii_text(ascii_art, text_output_path)
    print(f"已保存ASCII文本到: {text_output_path}")
