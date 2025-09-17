#!/usr/bin/env python3
"""
Demo Script - Avatar Pipeline Test
==================================

A simplified demonstration of the avatar pipeline that works without
installing all heavy dependencies like Whisper and PyTorch.
"""

import os
import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def mock_transcription(audio_path: str) -> str:
    """Mock transcription for demo purposes."""
    if "sample_audio" in audio_path:
        return "Hello, this is Bo speaking from Fast Track Academy. Welcome to our speech-to-text avatar generation pipeline!"
    else:
        return "This is a mock transcription of your audio file. In the full version, OpenAI Whisper would provide real speech-to-text transcription."


def create_demo_video(audio_path: str, avatar_path: str, output_path: str, transcription: str):
    """Create a demo video file with metadata."""
    try:
        # Create a simple text file as demo "video"
        with open(output_path.replace('.mp4', '_demo.txt'), 'w') as f:
            f.write("DEMO AVATAR VIDEO\n")
            f.write("================\n\n")
            f.write(f"Audio Source: {audio_path}\n")
            f.write(f"Avatar Image: {avatar_path}\n")
            f.write(f"Transcription: {transcription}\n")
            f.write(f"Output Path: {output_path}\n\n")
            f.write("In the full implementation, this would be a video file\n")
            f.write("showing the avatar speaking the transcribed text.\n")
        
        logger.info(f"Demo video metadata created: {output_path.replace('.mp4', '_demo.txt')}")
        return output_path.replace('.mp4', '_demo.txt')
        
    except Exception as e:
        logger.error(f"Error creating demo video: {e}")
        raise


def demo_pipeline():
    """Run a demonstration of the pipeline."""
    logger.info("Starting Avatar Pipeline Demo...")
    
    # Check if sample files exist
    audio_path = "assets/audio/sample_audio.wav"
    avatar_path = "assets/images/bo_default.jpg"
    
    if not os.path.exists(audio_path):
        logger.error(f"Sample audio not found: {audio_path}")
        logger.error("Please run: python setup.py first")
        return False
    
    if not os.path.exists(avatar_path):
        logger.error(f"Avatar image not found: {avatar_path}")
        logger.error("Please run: python setup.py first")
        return False
    
    # Create output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Mock transcription
    logger.info("Step 1: Transcribing audio (mock)...")
    transcription = mock_transcription(audio_path)
    
    # Save transcription
    transcript_path = os.path.join(output_dir, "demo_transcription.txt")
    with open(transcript_path, 'w', encoding='utf-8') as f:
        f.write(transcription)
    
    logger.info(f"Transcription: '{transcription}'")
    logger.info(f"Saved to: {transcript_path}")
    
    # Step 2: Create demo video
    logger.info("Step 2: Generating avatar video (demo)...")
    video_path = os.path.join(output_dir, "demo_avatar_video.mp4")
    demo_video_path = create_demo_video(audio_path, avatar_path, video_path, transcription)
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("DEMO PIPELINE COMPLETED!")
    logger.info("="*50)
    logger.info(f"Input Audio: {audio_path}")
    logger.info(f"Avatar Image: {avatar_path}")
    logger.info(f"Transcription: {transcript_path}")
    logger.info(f"Demo Video: {demo_video_path}")
    logger.info("="*50)
    logger.info("\nTo run the full pipeline with real AI models:")
    logger.info("1. Install full dependencies: pip install -r requirements.txt")
    logger.info("2. Run: python avatar_pipeline.py --mode file --audio assets/audio/sample_audio.wav")
    
    return True


def main():
    """Main demo function."""
    try:
        success = demo_pipeline()
        if success:
            print("\n🎉 Demo completed successfully!")
            print("Check the 'output' directory for results.")
        else:
            print("\n❌ Demo failed. Please check the logs above.")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Demo interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()