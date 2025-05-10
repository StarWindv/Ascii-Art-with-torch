# MIT License
# Copyright (c) 2025 星灿长风v


from .head import *


def check_cuda():
    try:
        import torch
        if torch.cuda.is_available():
            return True, torch
    except ImportError:
        return False, None

has_cuda, torch_module = check_cuda()

if has_cuda:
    torch = torch_module
    import torchvision.transforms as transforms


ENHANCED_CHARS = "@%#*+=-:. "
DEFAULT_CHAR = "▄"
DEFAULT_OUTPUT_DIR = "ASCII_PIC"


def get_terminal_size():
    """1-1: 获取终端尺寸"""
    try:
        return os.get_terminal_size()
    except OSError:
        return 80, 24

def adaptive_resize(image, target_width, target_height, enhance=False):
    """1-1: 自适应调整大小并居中"""
    orig_w, orig_h = image.size
    ratio = min(target_width/orig_w, target_height/orig_h)
    new_size = (int(orig_w*ratio), int(orig_h*ratio))

    if enhance and check_cuda():
        tensor = transforms.ToTensor()(image).unsqueeze(0)
        resized = transforms.functional.resize(tensor, new_size[::-1])
        resized = resized.squeeze().permute(1,2,0).numpy()*255
        resized = Image.fromarray(resized.astype('uint8'))
    else:
        resized = image.resize(new_size, Image.LANCZOS)

    # 居中处理
    new_img = Image.new("RGB", (target_width, target_height), (0,0,0))
    new_img.paste(resized, ((target_width-new_size[0])//2,
                            (target_height-new_size[1])//2))
    return new_img


def rgb_to_ansi(r, g, b, background=False):
    """0-1: RGB转ANSI颜色代码"""
    return f"\033[{48 if background else 38};2;{r};{g};{b}m"


def convert_frame(image, enhanced=False, fixed_size=None):
    """核心转换逻辑，支持固定尺寸"""
    if fixed_size is not None:
        cols, rows = fixed_size[0], fixed_size[1]
    else:
        cols, rows = get_terminal_size()
    target_size = (cols, rows*2)  # 使用传入的固定尺寸

    # 3-2: 增强模式预处理
    if enhanced:
        image = ImageOps.autocontrast(image, cutoff=2)

    resized = adaptive_resize(image, *target_size, enhanced)
    pixels = resized.load()

    output = []
    for y in range(0, target_size[1], 2):
        line = []
        for x in range(target_size[0]):
            try:
                upper = pixels[x, y]
                lower = pixels[x, y+1] if y+1 < target_size[1] else (0,0,0)
            except IndexError:
                upper = lower = (0,0,0)

            # 3-1: 增强模式字符选择
            if enhanced:
                brightness = (0.2126*upper[0] + 0.7152*upper[1] + 0.0722*upper[2] +
                              0.2126*lower[0] + 0.7152*lower[1] + 0.0722*lower[2])/2
                char = ENHANCED_CHARS[min(int(brightness/25.5), 9)]
            else:
                char = DEFAULT_CHAR

            line.append(f"{rgb_to_ansi(*upper)}{rgb_to_ansi(*lower, True)}{char}")
        output.append("".join(line))
    return "\n".join(output), resized