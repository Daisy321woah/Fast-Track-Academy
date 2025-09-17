#!/usr/bin/env python3
"""
Setup script for Avatar Pipeline
===============================

This script downloads required models and sets up the environment.
"""

import os
import sys
import logging
from pathlib import Path

import gdown
import torch
import whisper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_whisper_models():
    """Download and cache Whisper models."""
    logger.info("Setting up Whisper models...")
    
    models = ["tiny", "base"]  # Start with smaller models
    
    for model_name in models:
        try:
            logger.info(f"Downloading Whisper model: {model_name}")
            whisper.load_model(model_name)
            logger.info(f"✓ {model_name} model ready")
        except Exception as e:
            logger.error(f"✗ Failed to download {model_name}: {e}")


def setup_sadtalker_models():
    """Download SadTalker models (placeholder)."""
    logger.info("Setting up SadTalker models...")
    
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Placeholder for actual SadTalker model downloads
    # In a real implementation, this would download specific model files
    logger.info("SadTalker model setup (placeholder implementation)")
    
    # Create placeholder model files
    (models_dir / "sadtalker_models.txt").write_text("Placeholder for SadTalker models")


def create_sample_assets():
    """Create sample images and audio files."""
    logger.info("Creating sample assets...")
    
    # Create directories
    Path("assets/images").mkdir(parents=True, exist_ok=True)
    Path("assets/audio").mkdir(parents=True, exist_ok=True)
    
    # Create default avatar image (Bo)
    from PIL import Image, ImageDraw, ImageFont
    
    # Create a simple avatar image
    img = Image.new('RGB', (512, 512), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple face
    # Head circle
    draw.ellipse([100, 100, 400, 400], fill='peachpuff', outline='black', width=3)
    
    # Eyes
    draw.ellipse([150, 180, 190, 220], fill='white', outline='black', width=2)
    draw.ellipse([320, 180, 360, 220], fill='white', outline='black', width=2)
    draw.ellipse([160, 190, 180, 210], fill='black')  # Left pupil
    draw.ellipse([330, 190, 350, 210], fill='black')  # Right pupil
    
    # Nose
    draw.ellipse([240, 240, 270, 270], fill='peachpuff', outline='black', width=2)
    
    # Mouth
    draw.arc([200, 300, 310, 350], start=0, end=180, fill='black', width=3)
    
    # Save avatar
    avatar_path = "assets/images/bo_default.jpg"
    img.save(avatar_path)
    logger.info(f"✓ Created default avatar: {avatar_path}")
    
    # Create sample audio file (placeholder)
    import numpy as np
    import soundfile as sf
    
    # Generate a simple tone as placeholder audio
    sample_rate = 16000
    duration = 3.0  # 3 seconds
    frequency = 440  # A4 note
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio_data = 0.3 * np.sin(2 * np.pi * frequency * t)
    
    # Add fade in/out
    fade_samples = int(0.1 * sample_rate)  # 0.1 second fade
    audio_data[:fade_samples] *= np.linspace(0, 1, fade_samples)
    audio_data[-fade_samples:] *= np.linspace(1, 0, fade_samples)
    
    audio_path = "assets/audio/sample_audio.wav"
    sf.write(audio_path, audio_data, sample_rate)
    logger.info(f"✓ Created sample audio: {audio_path}")


def check_system_requirements():
    """Check system requirements."""
    logger.info("Checking system requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        logger.error("Python 3.8+ required")
        return False
    
    # Check PyTorch
    try:
        import torch
        logger.info(f"✓ PyTorch {torch.__version__}")
        if torch.cuda.is_available():
            logger.info(f"✓ CUDA available: {torch.cuda.get_device_name()}")
        else:
            logger.info("⚠ CUDA not available - using CPU")
    except ImportError:
        logger.error("✗ PyTorch not installed")
        return False
    
    # Check other critical dependencies
    try:
        import whisper
        logger.info("✓ OpenAI Whisper available")
    except ImportError:
        logger.error("✗ OpenAI Whisper not installed")
        return False
    
    try:
        import sounddevice
        logger.info("✓ sounddevice available")
    except ImportError:
        logger.warning("⚠ sounddevice not available - microphone recording disabled")
    
    try:
        import cv2
        logger.info("✓ OpenCV available")
    except ImportError:
        logger.error("✗ OpenCV not installed")
        return False
    
    return True


def main():
    """Main setup function."""
    logger.info("Starting Avatar Pipeline setup...")
    
    # Check requirements
    if not check_system_requirements():
        logger.error("System requirements not met. Please install missing dependencies.")
        sys.exit(1)
    
    # Setup models
    setup_whisper_models()
    setup_sadtalker_models()
    
    # Create sample assets
    create_sample_assets()
    
    # Create output directory
    Path("output").mkdir(exist_ok=True)
    
    logger.info("Setup completed successfully!")
    logger.info("\nNext steps:")
    logger.info("1. Run: python avatar_pipeline.py --mode record --duration 5")
    logger.info("2. Or: python avatar_pipeline.py --mode file --audio assets/audio/sample_audio.wav")


if __name__ == "__main__":
    main()