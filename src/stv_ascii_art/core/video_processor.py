# MIT License
# Copyright (c) 2025 星灿长风v


from stv_ascii_art.utils.utils import *


class VideoProcessor:
    """视频处理核心类"""
    def __init__(self, path, enhanced=False, use_gpu=False):
        self.cap = cv2.VideoCapture(path)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.enhanced = enhanced
        self.use_gpu = use_gpu

        # A-1: GPU初始化
        if use_gpu and check_cuda()[0]:
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
        if self.use_gpu and check_cuda():
            tensor = torch.from_numpy(frame).cuda().float()/255
            tensor = tensor.permute(2,0,1).unsqueeze(0)
            frame = (tensor.squeeze().permute(1,2,0).cpu().numpy()*255).astype('uint8')

        self.current_frame += 1
        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

def handle_video(input_path, enhanced=False, export=False, output_path=None, use_gpu=False, fixed_size=None):
    """视频处理入口"""
    # 在函数开始时获取并固定终端尺寸
    terminal_size = get_terminal_size() if fixed_size is None else fixed_size
    terminal_cols, terminal_rows = terminal_size[0], terminal_size[1]
    target_size = (terminal_cols, terminal_rows * 2)  # 固定初始尺寸

    processor = VideoProcessor(input_path, enhanced, use_gpu)

    if export:
        if output_path is None:
            output_dir = os.path.join(os.getcwd(), DEFAULT_OUTPUT_DIR)
            filename = f"{os.path.splitext(os.path.basename(input_path))[0]}_ascii.mp4"
            output_path = os.path.join(output_dir, filename)

        # 使用固定的初始尺寸创建视频写入器
        writer = cv2.VideoWriter(
            output_path,
            cv2.VideoWriter_fourcc(*'mp4v'),
            processor.fps,
            (terminal_cols, terminal_rows * 2)  # 固定尺寸
        )

        pbar = tqdm(total=processor.total_frames, desc="转换进度")
        for frame in processor:
            # 将固定尺寸传递给convert_frame
            ascii_art, resized = convert_frame(frame, enhanced, fixed_size=(terminal_cols, terminal_rows))
            writer.write(cv2.cvtColor(np.array(resized), cv2.COLOR_RGB2BGR))
            pbar.update(1)
        writer.release()
        return

    # 实时播放模式
    print("\033[?25l", end="")  # 隐藏光标
    try:
        start_time = time.time()
        for idx, frame in enumerate(processor):
            ascii_art, _ = convert_frame(frame, enhanced, fixed_size=None)
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