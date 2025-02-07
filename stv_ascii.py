# MIT License

# Copyright (c) 2025 星灿长风v

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import os
import sys
import time
from tqdm import tqdm
from PIL import Image, ImageOps
import cv2
import numpy as np

# 硬件加速检测
try:
    import torch
    import torchvision.transforms as transforms
    HAS_TORCH = True
except Exception as e:
    print(f"\033[31m由于问题 \033[96m{e}\033[31m\n\t而无法使用GPU加速\033[0m")
    HAS_TORCH = False

# 全局配置
ENHANCED_CHARS = "@%#*+=-:. "  # 增强模式字符集
DEFAULT_CHAR = "▄"             # 默认模式字符
DEFAULT_OUTPUT_DIR = "ASCII_PIC"

def check_cuda():
    """A-1: 检测CUDA可用性"""
    if not HAS_TORCH:
        return False
    return torch.cuda.is_available()

def get_terminal_size():
    """1-1: 获取终端尺寸"""
    try:
        return os.get_terminal_size()
    except OSError:
        return (80, 24)

def adaptive_resize(image, target_width, target_height, enhance=False):
    """1-1: 自适应调整大小并居中"""
    orig_w, orig_h = image.size
    ratio = min(target_width/orig_w, target_height/orig_h)
    new_size = (int(orig_w*ratio), int(orig_h*ratio))
    
    if enhance and HAS_TORCH:
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

def convert_frame(image, enhanced=False):
    """核心转换逻辑，支持两种模式"""
    cols, rows = get_terminal_size()
    target_size = (cols, rows*2)  # 每字符占两像素高度
    
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

def save_ascii_image(image, path):
    """2-1/2-2: 保存ASCII图片"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    image.save(path)

def handle_image(input_path, output_path=None, enhanced=False, use_gpu=False):
    """图片处理入口"""
    try:
        img = Image.open(input_path)
    except FileNotFoundError:
        print(f"文件未找到: {input_path}")
        return
    
    # A-1/A-2: GPU加速
    if use_gpu and check_cuda():
        img = img.convert("RGB")
        tensor = transforms.ToTensor()(img).cuda()
        img = transforms.ToPILImage()(tensor.cpu())
    
    ascii_art, resized_img = convert_frame(img, enhanced)
    print("\n".join([line + "\033[0m" for line in ascii_art.split("\n")]))
    
    # 保存输出
    if output_path is None:
        output_dir = os.path.join(os.getcwd(), DEFAULT_OUTPUT_DIR)
        filename = f"{os.path.splitext(os.path.basename(input_path))[0]}_ascii.png"
        output_path = os.path.join(output_dir, filename)
    
    save_ascii_image(resized_img, output_path)
    print(f"已保存到: {output_path}")

class VideoProcessor:
    """视频处理核心类"""
    def __init__(self, path, enhanced=False, use_gpu=False):
        self.cap = cv2.VideoCapture(path)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.enhanced = enhanced
        self.use_gpu = use_gpu
        
        # A-1: GPU初始化
        if use_gpu and check_cuda():
            self.device = torch.device("cuda")
            # 已移除OpenCV GPU设置

    def __iter__(self):
        self.current_frame = 0
        return self
    
    def __next__(self):
        ret, frame = self.cap.read()
        if not ret:
            raise StopIteration
        
        # GPU加速处理
        if self.use_gpu and HAS_TORCH:
            tensor = torch.from_numpy(frame).cuda().float()/255
            tensor = tensor.permute(2,0,1).unsqueeze(0)
            frame = (tensor.squeeze().permute(1,2,0).cpu().numpy()*255).astype('uint8')
        
        self.current_frame += 1
        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

def handle_video(input_path, enhanced=False, export=False, output_path=None, use_gpu=False):
    """视频处理入口"""
    processor = VideoProcessor(input_path, enhanced, use_gpu)
    
    if export:
        # 视频导出模式
        if output_path is None:
            output_dir = os.path.join(os.getcwd(), DEFAULT_OUTPUT_DIR)
            filename = f"{os.path.splitext(os.path.basename(input_path))[0]}_ascii.mp4"
            output_path = os.path.join(output_dir, filename)
        
        # 视频写入器
        writer = cv2.VideoWriter(
            output_path, 
            cv2.VideoWriter_fourcc(*'mp4v'), 
            processor.fps, 
            (get_terminal_size()[0], get_terminal_size()[1]*2)
        )
        
        # 进度条
        pbar = tqdm(total=processor.total_frames, desc="转换进度")
        for frame in processor:
            _, resized = convert_frame(frame, enhanced)
            writer.write(cv2.cvtColor(np.array(resized), cv2.COLOR_RGB2BGR))
            pbar.update(1)
        writer.release()
        return
    
    # 实时播放模式
    print("\033[?25l", end="")  # 隐藏光标
    try:
        start_time = time.time()
        for idx, frame in enumerate(processor):
            ascii_art, _ = convert_frame(frame, enhanced)
            # 1-2: 无闪烁刷新
            print(f"\033[H{ascii_art}\033[0m", end="", flush=True)
            
            # 精确帧率控制
            expected = start_time + (idx / processor.fps)
            sleep_time = expected - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)
    finally:
        print("\033[?25h")  # 恢复光标
        processor.cap.release()

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="ASCII Art 转换工具")
    parser.add_argument("input", help="输入文件路径")
    parser.add_argument("-o", "--output", help="输出路径")
    parser.add_argument("-v", "--video", action="store_true", help="视频模式")
    parser.add_argument("-e", "--enhanced", action="store_true", help="增强模式")
    parser.add_argument("-x", "--export", action="store_true", help="导出视频文件")
    parser.add_argument("-g", "--gpu", action="store_true", help="启用GPU加速")
    
    args = parser.parse_args()
    
    if args.video:
        handle_video(
            args.input,
            enhanced=args.enhanced,
            export=args.export,
            output_path=args.output,
            use_gpu=args.gpu
        )
    else:
        handle_image(
            args.input,
            output_path=args.output,
            enhanced=args.enhanced,
            use_gpu=args.gpu
        )

if __name__ == "__main__":
    main()
