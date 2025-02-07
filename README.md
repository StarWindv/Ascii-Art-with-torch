# ASCII Art 转换工具 🎨⇄⌨️

将图片/视频实时转换为高性能ASCII艺术，支持终端预览与文件导出，提供GPU加速和增强模式！

---
<table>
  <tr>
    <td><img src="demo/herta2_ascii.png" width="100%" /></td>
    <td><img src="demo/details-1.png" width="100%" /></td>
  </tr>
</table>

<table >
  <tr>
    <td align="center"><img src="demo/generating.gif" width="75%" /></td>
  </tr>
</table>

## ✨ 功能亮点

- **双模式支持**：基础模式(`▄`字符) / 增强模式(`@%#*+=-:. `渐变字符)
- **硬件加速**：自动检测CUDA，支持GPU加速处理（需安装PyTorch）
- **智能适配**：根据终端尺寸自适应缩放并居中显示
- **多媒体支持**：
  - 图片：即时预览+保存处理后的PNG
  - 视频：实时播放（30FPS+）或导出MP4文件
- **ANSI真彩色**：精确还原原始色彩空间

---

## 🛠️ 安装依赖

```bash
pip install pillow opencv-python numpy tqdm
pip install torch torchvision
```

---

## 🚀 使用指南

### 基本命令

```bash
python stv_ascii.py [输入路径] [选项]
```

### 选项说明

| 参数  | 缩写  | 说明  |
| --- | --- | --- |
| `--output` | `-o` | 自定义输出路径 |
| `--video` | `-v` | 视频模式 |
| `--enhanced` | `-e` | 启用增强字符集 |
| `--export` | `-x` | 导出视频文件（仅视频模式） |
| `--gpu` | `-g` | 启用GPU加速 |

### 使用示例

1. **图片转ASCII**（终端预览+保存）
  
  ```bash
  python stv_ascii.py input.jpg -e -g
  ```
  
2. **视频实时播放**
  
  ```bash
  python stv_ascii.py input.mp4 -v -e
  ```
  注意，这个功能受电脑性能和终端字体大小影响，当清晰度过高时，将无法保证播放流畅。
  
3. **高质量导出ASCII视频**
  
  ```bash
  python stv_ascii.py input.mp4 -v -x -e -o output.mp4
  ```
  注意，当处在导出模式时将不会播放艺术帧。
  注意，当导出开始后，请不要调整当前标签页的字体大小。

---

## 📝 已知不足

1. **终端依赖**  
  实时预览效果受终端模拟器性能及ANSI支持程度影响
  
2. **分辨率限制**  
  输出尺寸固定为当前终端窗口大小（可手动调整终端后重试）
  
3. **GPU兼容性**  
  需要正确配置CUDA环境，部分AMD显卡可能无法加速
  
4. **大文件处理**  
  4K以上视频建议使用导出模式而非实时播放
  
5. **字符精度**  
  增强模式仅支持10级灰度，极端暗光场景可能丢失细节
  

---

## 🤝 参与贡献

欢迎提交PR或Issue！  
推荐方向：更多字符集支持、自动调整字符大小、音频支持

**[📜 MIT许可证](LICENSE)**
