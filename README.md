# Fast Track Academy - Avatar Pipeline

Welcome to **Fast Track Academy**, featuring an advanced **Speech-to-Text Avatar Generation Pipeline**. This project allows users to record or upload speech, transcribe it using OpenAI Whisper, and generate realistic avatar videos using SadTalker technology.

## 🎯 Key Features

### 1. Speech-to-Text Avatar Pipeline
- **Audio Input**: Record from microphone or upload audio files
- **Speech Transcription**: Powered by OpenAI Whisper for accurate speech-to-text
- **Avatar Generation**: Create realistic talking avatar videos using SadTalker
- **Full Automation**: End-to-end pipeline from speech to avatar video

### 2. Customizable Avatar (Bo)
- Use the default "Bo" avatar or upload your own photo
- Realistic lip-sync and facial animation
- Support for various image formats

### 3. Advanced Audio Processing
- High-quality audio recording (16kHz sampling rate)
- Support for multiple audio formats (WAV, MP3, etc.)
- Automatic audio preprocessing for optimal transcription

---

## 📁 Repository Structure

```
Fast-Track-Academy/
├── README.md
├── requirements.txt
├── avatar_pipeline.py          # Main pipeline script
├── setup.py                    # Setup and model download script
├── assets/
│   ├── images/
│   │   └── bo_default.jpg      # Default avatar image
│   └── audio/
│       └── sample_audio.wav    # Sample test audio
├── models/                     # Downloaded AI models
├── output/                     # Generated outputs
│   ├── recorded_audio.wav
│   ├── transcription.txt
│   └── avatar_video.mp4
└── avatar_generation/          # Additional utilities
```

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Daisy321woah/Fast-Track-Academy.git
cd Fast-Track-Academy
```

### 2. Install Dependencies
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Models and Assets
```bash
python setup.py
```

### 4. Run the Pipeline

#### Option A: Record from Microphone
```bash
python avatar_pipeline.py --mode record --duration 10
```

#### Option B: Use Audio File
```bash
python avatar_pipeline.py --mode file --audio assets/audio/sample_audio.wav
```

#### Option C: Custom Avatar
```bash
python avatar_pipeline.py --mode record --avatar /path/to/your/photo.jpg --duration 5
```

---

## 🛠 System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 4GB (8GB recommended)
- **Storage**: 2GB free space for models
- **OS**: Windows 10+, macOS 10.14+, or Linux

### Optional Requirements
- **GPU**: NVIDIA GPU with CUDA support for faster processing
- **Microphone**: For audio recording functionality
- **FFmpeg**: For advanced video processing (auto-detected)

---

## 📖 Detailed Usage

### Command Line Options

```bash
python avatar_pipeline.py [OPTIONS]

Options:
  --mode {record,file}     Input mode: record from mic or use audio file
  --audio PATH            Path to audio file (required for 'file' mode)
  --avatar PATH           Path to avatar image (default: assets/images/bo_default.jpg)
  --duration FLOAT        Recording duration in seconds (default: 10.0)
  --output DIR           Output directory (default: output)
  --whisper-model SIZE   Whisper model size: tiny/base/small/medium/large (default: base)
```

### Examples

1. **Quick Test with Default Settings**:
   ```bash
   python avatar_pipeline.py --mode record --duration 5
   ```

2. **High-Quality Transcription**:
   ```bash
   python avatar_pipeline.py --mode file --audio my_speech.wav --whisper-model large
   ```

3. **Custom Avatar with Your Photo**:
   ```bash
   python avatar_pipeline.py --mode record --avatar my_photo.jpg --duration 8
   ```

4. **Batch Processing**:
   ```bash
   python avatar_pipeline.py --mode file --audio speech1.wav --output results/video1
   python avatar_pipeline.py --mode file --audio speech2.wav --output results/video2
   ```

---

## 🔧 Configuration

### Whisper Models
- **tiny**: Fastest, least accurate (~39 MB)
- **base**: Good balance of speed/accuracy (~74 MB) - *Default*
- **small**: Better accuracy (~244 MB)
- **medium**: High accuracy (~769 MB)
- **large**: Best accuracy (~1550 MB)

### Audio Settings
- **Sample Rate**: 16kHz (optimal for Whisper)
- **Format**: WAV (recommended), MP3, FLAC supported
- **Quality**: 16-bit depth minimum

---

## 🧪 Testing

### Test with Sample Audio
```bash
# Use the provided sample audio
python avatar_pipeline.py --mode file --audio assets/audio/sample_audio.wav

# Check outputs
ls output/
# Expected: recorded_audio.wav, transcription.txt, avatar_video.mp4
```

### Test Recording (if microphone available)
```bash
python avatar_pipeline.py --mode record --duration 3
```

---

## 🐛 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: 
   ```bash
   pip install -r requirements.txt
   ```

2. **Audio Recording Fails**:
   - Check microphone permissions
   - Install system audio drivers
   - Try: `pip install pyaudio` (alternative audio backend)

3. **CUDA/GPU Issues**:
   - Install CUDA-compatible PyTorch: https://pytorch.org/get-started/locally/
   - CPU processing will work but be slower

4. **FFmpeg Not Found**:
   - Install FFmpeg: https://ffmpeg.org/download.html
   - Videos will be created without audio if FFmpeg is unavailable

5. **SadTalker Model Issues**:
   - Current implementation uses placeholder video generation
   - Full SadTalker integration requires additional setup

### Getting Help

1. Check the logs for detailed error messages
2. Ensure all dependencies are installed correctly
3. Verify input files exist and are readable
4. Try with smaller Whisper models if memory is limited

---

## 🔮 Advanced Features

### Custom Model Configuration
```python
# In avatar_pipeline.py, modify these settings:
WHISPER_MODEL = "large"  # For better transcription
SAMPLE_RATE = 22050      # Higher quality audio
```

### Batch Processing Script
```bash
# Create batch_process.py for multiple files
for audio_file in *.wav; do
    python avatar_pipeline.py --mode file --audio "$audio_file" --output "results/$(basename "$audio_file" .wav)"
done
```

---

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🔗 Links & Resources

- [OpenAI Whisper Documentation](https://github.com/openai/whisper)
- [SadTalker Repository](https://github.com/OpenTalker/SadTalker)
- [PyTorch Installation Guide](https://pytorch.org/get-started/locally/)
- [FFmpeg Download](https://ffmpeg.org/download.html)

---

**Fast Track Academy** - Empowering creativity through AI-powered tools!
