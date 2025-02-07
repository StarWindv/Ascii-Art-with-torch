# ASCII Art Conversion Tool 🎨⇄⌨️

Real-time conversion of images/videos into high-performance ASCII art with terminal preview and file export support, featuring GPU acceleration and enhanced modes!

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

## ✨ Key Features

- **Dual Modes**: Basic mode (`▄` characters) / Enhanced mode (`@%#*+=-:. ` gradient characters)
- **Hardware Acceleration**: Automatic CUDA detection with GPU acceleration (requires PyTorch)
- **Smart Adaptation**: Auto-scales and centers output based on terminal dimensions
- **Multimedia Support**:
  - Images: Instant preview + save as PNG
  - Videos: Real-time playback (30FPS+) or MP4 export
- **ANSI True Color**: Accurately preserves original color space

---

## 🛠️ Installation

```bash
pip install pillow opencv-python numpy tqdm
pip install torch torchvision
```

---

## 🚀 Usage Guide

### Basic Command

```bash
python stv_ascii.py [input_path] [options]
```

### Options

| Parameter | Short | Description |
| --- | --- | --- |
| `--output` | `-o` | Custom output path |
| `--video` | `-v` | Video mode |
| `--enhanced` | `-e` | Enable enhanced charset |
| `--export` | `-x` | Export video file (video mode only) |
| `--gpu` | `-g` | Enable GPU acceleration |

### Examples

1. **Image to ASCII** (Preview + Save)
  
  ```bash
  python stv_ascii.py input.jpg -e -g
  ```
  
2. **Real-time Video Playback**
  
  ```bash
  python stv_ascii.py input.mp4 -v -e
  ```
  Note: Performance depends on system specs and terminal font size. High resolutions may affect smoothness.
  
3. **High-quality Video Export**
  
  ```bash
  python stv_ascii.py input.mp4 -v -x -e -o output.mp4
  ```
  Note: Art frames won't play during export mode. Avoid changing terminal font size after export starts.

---

## 📝 Known Limitations

1. **Terminal Dependency**  
  Real-time preview quality varies by terminal emulator's ANSI support and performance
  
2. **Resolution Lock**  
  Output size matches current terminal window dimensions (adjust terminal manually)
  
3. **GPU Compatibility**  
  Requires proper CUDA setup. Partial AMD GPU support
  
4. **Large File Handling**  
  For 4K+ videos, use export mode instead of real-time playback
  
5. **Character Precision**  
  Enhanced mode supports 10 grayscale levels. Extreme low-light details may be lost

---

## 🤝 Contribution

Welcome PRs and Issues!  
Suggested directions: More charset support, auto-character sizing, audio integration

**[📜 MIT License](LICENSE)**
