# Installation Guide - Avatar Pipeline

## Quick Demo (No Heavy Dependencies)

To quickly test the pipeline concept without installing large AI models:

```bash
# 1. Clone the repository
git clone https://github.com/Daisy321woah/Fast-Track-Academy.git
cd Fast-Track-Academy

# 2. Install minimal dependencies
pip install Pillow numpy soundfile

# 3. Create sample assets
python -c "
from PIL import Image, ImageDraw
import numpy as np
import soundfile as sf
import os

# Create directories
os.makedirs('assets/images', exist_ok=True)
os.makedirs('assets/audio', exist_ok=True)

# Create default avatar image
img = Image.new('RGB', (512, 512), color='lightblue')
draw = ImageDraw.Draw(img)
draw.ellipse([100, 100, 400, 400], fill='peachpuff', outline='black', width=3)
draw.ellipse([150, 180, 190, 220], fill='white', outline='black', width=2)
draw.ellipse([320, 180, 360, 220], fill='white', outline='black', width=2)
draw.ellipse([160, 190, 180, 210], fill='black')
draw.ellipse([330, 190, 350, 210], fill='black')
draw.ellipse([240, 240, 270, 270], fill='peachpuff', outline='black', width=2)
draw.arc([200, 300, 310, 350], start=0, end=180, fill='black', width=3)
img.save('assets/images/bo_default.jpg')

# Create sample audio
sample_rate = 16000
duration = 3.0
t = np.linspace(0, duration, int(sample_rate * duration))
audio_data = 0.3 * np.sin(2 * np.pi * 440 * t)
fade_samples = int(0.1 * sample_rate)
audio_data[:fade_samples] *= np.linspace(0, 1, fade_samples)
audio_data[-fade_samples:] *= np.linspace(1, 0, fade_samples)
sf.write('assets/audio/sample_audio.wav', audio_data, sample_rate)
print('Sample assets created!')
"

# 4. Run the demo
python demo.py
```

## Full Installation (With AI Models)

For the complete experience with real speech-to-text and avatar generation:

### Prerequisites

- Python 3.8+
- 4GB+ RAM (8GB recommended)
- 2GB+ free disk space

### Step 1: Environment Setup

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
# Install PyTorch (choose appropriate version for your system)
# CPU version:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# GPU version (if you have CUDA):
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install other dependencies
pip install -r requirements.txt
```

### Step 3: Setup Models and Assets

```bash
python setup.py
```

### Step 4: Test Installation

```bash
# Test with sample audio file
python avatar_pipeline.py --mode file --audio assets/audio/sample_audio.wav

# Test with microphone (if available)
python avatar_pipeline.py --mode record --duration 5
```

## Troubleshooting

### Common Issues

1. **PyTorch Installation Issues**:
   - Visit https://pytorch.org/get-started/locally/ for platform-specific instructions
   - For older systems, try CPU-only version first

2. **Audio Recording Problems**:
   ```bash
   # Install system audio dependencies (Ubuntu/Debian)
   sudo apt-get install portaudio19-dev
   
   # Alternative audio backend
   pip install pyaudio
   ```

3. **FFmpeg Not Found**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install ffmpeg
   
   # macOS
   brew install ffmpeg
   
   # Windows: Download from https://ffmpeg.org/download.html
   ```

4. **Memory Issues**:
   - Use smaller Whisper models: `--whisper-model tiny`
   - Close other applications
   - Consider using CPU-only PyTorch

### System-Specific Notes

**Windows**:
- Use Command Prompt or PowerShell
- May need Visual Studio Build Tools for some packages

**macOS**:
- May need Xcode Command Line Tools: `xcode-select --install`

**Linux**:
- May need additional system packages for audio/video processing

## Performance Optimization

- **GPU Acceleration**: Install CUDA-compatible PyTorch for faster processing
- **Model Selection**: Balance between speed and accuracy
  - `tiny`: Fastest, good for testing
  - `base`: Good balance (default)
  - `large`: Best accuracy, slower

## What's Included

After successful installation, you'll have:

- ✅ Speech recording capability
- ✅ OpenAI Whisper transcription
- ✅ Basic avatar video generation
- ✅ Sample avatar image (Bo)
- ✅ Sample audio file
- ✅ Complete pipeline automation

## Next Steps

1. Try with your own audio files
2. Use your own avatar photos
3. Experiment with different Whisper models
4. Customize the pipeline for your needs

For more details, see the main README.md file.