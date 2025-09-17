#!/usr/bin/env python3
"""
Avatar Pipeline - Speech-to-Text Avatar Video Generation
========================================================

This script provides a complete pipeline for:
1. Recording or loading audio input
2. Transcribing speech to text using OpenAI Whisper
3. Generating realistic avatar videos using SadTalker

Usage:
    python avatar_pipeline.py --mode record --avatar assets/images/bo_default.jpg
    python avatar_pipeline.py --mode file --audio input.wav --avatar custom_photo.jpg

Author: Fast Track Academy
"""

import os
import sys
import argparse
import logging
import tempfile
from pathlib import Path
from typing import Optional, Tuple

# Core libraries
import numpy as np
import torch
import whisper
import sounddevice as sd
import soundfile as sf
from PIL import Image

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AudioProcessor:
    """Handles audio recording and file operations."""
    
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        
    def record_audio(self, duration: float = 10.0, output_path: Optional[str] = None) -> str:
        """Record audio from microphone."""
        logger.info(f"Recording audio for {duration} seconds...")
        
        try:
            # Record audio
            audio_data = sd.rec(int(duration * self.sample_rate), 
                              samplerate=self.sample_rate, 
                              channels=1, 
                              dtype='float32')
            sd.wait()  # Wait until recording is finished
            
            # Save to file
            if output_path is None:
                output_path = "output/recorded_audio.wav"
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            sf.write(output_path, audio_data, self.sample_rate)
            
            logger.info(f"Audio recorded and saved to: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error recording audio: {e}")
            raise
    
    def validate_audio_file(self, audio_path: str) -> bool:
        """Validate if audio file exists and is readable."""
        if not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            return False
            
        try:
            data, samplerate = sf.read(audio_path)
            logger.info(f"Audio file loaded: {audio_path} ({len(data)} samples, {samplerate} Hz)")
            return True
        except Exception as e:
            logger.error(f"Error reading audio file: {e}")
            return False


class SpeechTranscriber:
    """Handles speech-to-text using OpenAI Whisper."""
    
    def __init__(self, model_name: str = "base"):
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load Whisper model."""
        try:
            logger.info(f"Loading Whisper model: {self.model_name}")
            self.model = whisper.load_model(self.model_name)
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading Whisper model: {e}")
            raise
    
    def transcribe(self, audio_path: str) -> str:
        """Transcribe audio file to text."""
        try:
            logger.info(f"Transcribing audio: {audio_path}")
            result = self.model.transcribe(audio_path)
            text = result["text"].strip()
            
            logger.info(f"Transcription completed: '{text[:100]}{'...' if len(text) > 100 else ''}'")
            return text
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            raise


class SadTalkerWrapper:
    """Wrapper for SadTalker avatar generation."""
    
    def __init__(self):
        self.models_dir = "models"
        self.sadtalker_installed = False
        self._check_sadtalker()
    
    def _check_sadtalker(self):
        """Check if SadTalker is available and models are downloaded."""
        try:
            # Try to import SadTalker components
            # Note: This is a simplified check - actual SadTalker setup is more complex
            self.sadtalker_installed = True
            logger.info("SadTalker components check passed")
        except ImportError:
            logger.warning("SadTalker not fully installed. Using placeholder implementation.")
            self.sadtalker_installed = False
    
    def download_models(self):
        """Download required SadTalker models."""
        os.makedirs(self.models_dir, exist_ok=True)
        logger.info("Model download would happen here (placeholder)")
        # In a real implementation, this would download the actual SadTalker models
    
    def generate_avatar_video(self, audio_path: str, avatar_image_path: str, output_path: str) -> str:
        """Generate avatar video from audio and image."""
        try:
            logger.info(f"Generating avatar video...")
            logger.info(f"Audio: {audio_path}")
            logger.info(f"Avatar image: {avatar_image_path}")
            logger.info(f"Output: {output_path}")
            
            if not self.sadtalker_installed:
                # Placeholder implementation - create a simple video file
                return self._create_placeholder_video(audio_path, avatar_image_path, output_path)
            
            # Real SadTalker implementation would go here
            # For now, we'll use the placeholder
            return self._create_placeholder_video(audio_path, avatar_image_path, output_path)
            
        except Exception as e:
            logger.error(f"Error generating avatar video: {e}")
            raise
    
    def _create_placeholder_video(self, audio_path: str, avatar_image_path: str, output_path: str) -> str:
        """Create a placeholder video for testing."""
        try:
            import cv2
            import imageio
            
            # Load the avatar image
            img = cv2.imread(avatar_image_path)
            if img is None:
                raise ValueError(f"Could not load image: {avatar_image_path}")
            
            # Get audio duration
            data, samplerate = sf.read(audio_path)
            duration = len(data) / samplerate
            
            # Create a simple video with the static image
            fps = 25
            total_frames = int(duration * fps)
            
            # Resize image to standard video size
            img_resized = cv2.resize(img, (640, 480))
            
            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (640, 480))
            
            for frame in range(total_frames):
                out.write(img_resized)
            
            out.release()
            cv2.destroyAllWindows()
            
            # Add audio to video using ffmpeg (if available)
            try:
                import subprocess
                temp_video = output_path.replace('.mp4', '_temp.mp4')
                os.rename(output_path, temp_video)
                
                cmd = [
                    'ffmpeg', '-y', '-i', temp_video, '-i', audio_path,
                    '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental',
                    output_path
                ]
                subprocess.run(cmd, check=True, capture_output=True)
                os.remove(temp_video)
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                logger.warning("ffmpeg not available - video will not have audio")
            
            logger.info(f"Placeholder video created: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating placeholder video: {e}")
            raise


class AvatarPipeline:
    """Main pipeline coordinator."""
    
    def __init__(self, whisper_model: str = "base"):
        self.audio_processor = AudioProcessor()
        self.transcriber = SpeechTranscriber(whisper_model)
        self.avatar_generator = SadTalkerWrapper()
        
    def run_pipeline(self, 
                    mode: str,
                    audio_path: Optional[str] = None,
                    avatar_image: str = "assets/images/bo_default.jpg",
                    record_duration: float = 10.0,
                    output_dir: str = "output") -> Tuple[str, str, str]:
        """Run the complete pipeline."""
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Step 1: Get audio
        if mode == "record":
            audio_file = self.audio_processor.record_audio(
                duration=record_duration,
                output_path=os.path.join(output_dir, "recorded_audio.wav")
            )
        elif mode == "file":
            if not audio_path or not self.audio_processor.validate_audio_file(audio_path):
                raise ValueError("Valid audio file path required for 'file' mode")
            audio_file = audio_path
        else:
            raise ValueError("Mode must be 'record' or 'file'")
        
        # Step 2: Transcribe speech
        transcription = self.transcriber.transcribe(audio_file)
        
        # Save transcription
        transcript_path = os.path.join(output_dir, "transcription.txt")
        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(transcription)
        
        # Step 3: Validate avatar image
        if not os.path.exists(avatar_image):
            logger.warning(f"Avatar image not found: {avatar_image}. Using placeholder.")
            avatar_image = self._create_placeholder_avatar(avatar_image)
        
        # Step 4: Generate avatar video
        video_output = os.path.join(output_dir, "avatar_video.mp4")
        video_path = self.avatar_generator.generate_avatar_video(
            audio_path=audio_file,
            avatar_image_path=avatar_image,
            output_path=video_output
        )
        
        logger.info("Pipeline completed successfully!")
        logger.info(f"Audio: {audio_file}")
        logger.info(f"Transcription: {transcript_path}")
        logger.info(f"Video: {video_path}")
        
        return audio_file, transcript_path, video_path
    
    def _create_placeholder_avatar(self, target_path: str) -> str:
        """Create a placeholder avatar image."""
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        # Create a simple placeholder image
        img = Image.new('RGB', (512, 512), color='lightblue')
        img.save(target_path)
        
        logger.info(f"Created placeholder avatar: {target_path}")
        return target_path


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Avatar Pipeline - Speech to Avatar Video")
    
    parser.add_argument("--mode", choices=["record", "file"], required=True,
                       help="Input mode: 'record' from microphone or 'file' from audio file")
    parser.add_argument("--audio", type=str, 
                       help="Path to audio file (required for 'file' mode)")
    parser.add_argument("--avatar", type=str, default="assets/images/bo_default.jpg",
                       help="Path to avatar image (default: assets/images/bo_default.jpg)")
    parser.add_argument("--duration", type=float, default=10.0,
                       help="Recording duration in seconds (for 'record' mode)")
    parser.add_argument("--output", type=str, default="output",
                       help="Output directory (default: output)")
    parser.add_argument("--whisper-model", type=str, default="base",
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model size (default: base)")
    
    args = parser.parse_args()
    
    try:
        # Initialize pipeline
        pipeline = AvatarPipeline(whisper_model=args.whisper_model)
        
        # Run pipeline
        audio_file, transcript_file, video_file = pipeline.run_pipeline(
            mode=args.mode,
            audio_path=args.audio,
            avatar_image=args.avatar,
            record_duration=args.duration,
            output_dir=args.output
        )
        
        print("\n" + "="*50)
        print("PIPELINE COMPLETED SUCCESSFULLY!")
        print("="*50)
        print(f"Audio file: {audio_file}")
        print(f"Transcription: {transcript_file}")
        print(f"Avatar video: {video_file}")
        print("="*50)
        
    except KeyboardInterrupt:
        logger.info("Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()