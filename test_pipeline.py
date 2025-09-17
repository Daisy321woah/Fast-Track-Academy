#!/usr/bin/env python3
"""
Test Suite for Avatar Pipeline
=============================

Simple tests to verify the pipeline components work correctly.
"""

import os
import sys
import tempfile
from pathlib import Path

def test_basic_imports():
    """Test that basic imports work."""
    print("Testing basic imports...")
    try:
        import numpy as np
        import soundfile as sf
        from PIL import Image
        print("✓ Basic imports successful")
        return True
    except ImportError as e:
        print(f"✗ Basic import failed: {e}")
        return False

def test_assets_exist():
    """Test that sample assets exist."""
    print("Testing asset files...")
    
    avatar_path = "assets/images/bo_default.jpg"
    audio_path = "assets/audio/sample_audio.wav"
    
    if not os.path.exists(avatar_path):
        print(f"✗ Avatar image missing: {avatar_path}")
        return False
    
    if not os.path.exists(audio_path):
        print(f"✗ Sample audio missing: {audio_path}")
        return False
    
    # Test loading avatar image
    try:
        from PIL import Image
        img = Image.open(avatar_path)
        print(f"✓ Avatar image loaded: {img.size}")
    except Exception as e:
        print(f"✗ Failed to load avatar image: {e}")
        return False
    
    # Test loading audio
    try:
        import soundfile as sf
        data, samplerate = sf.read(audio_path)
        print(f"✓ Sample audio loaded: {len(data)} samples at {samplerate}Hz")
    except Exception as e:
        print(f"✗ Failed to load sample audio: {e}")
        return False
    
    return True

def test_demo_script():
    """Test the demo script."""
    print("Testing demo script...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "demo.py"], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✓ Demo script ran successfully")
            return True
        else:
            print(f"✗ Demo script failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Demo script test failed: {e}")
        return False

def test_pipeline_help():
    """Test that the main pipeline shows help correctly."""
    print("Testing pipeline help...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "avatar_pipeline.py", "--help"], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and "Avatar Pipeline" in result.stdout:
            print("✓ Pipeline help works")
            return True
        else:
            print(f"✗ Pipeline help failed")
            return False
    except Exception as e:
        print(f"✗ Pipeline help test failed: {e}")
        return False

def test_pipeline_basic():
    """Test basic pipeline functionality."""
    print("Testing basic pipeline...")
    
    if not os.path.exists("assets/audio/sample_audio.wav"):
        print("✗ Sample audio not found - skipping pipeline test")
        return False
    
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, "avatar_pipeline.py", 
            "--mode", "file", 
            "--audio", "assets/audio/sample_audio.wav"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✓ Basic pipeline ran successfully")
            
            # Check output files
            if os.path.exists("output/transcription.txt"):
                print("✓ Transcription file created")
            else:
                print("✗ Transcription file missing")
                return False
                
            return True
        else:
            print(f"✗ Pipeline failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Pipeline test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Avatar Pipeline Test Suite")
    print("=" * 30)
    
    tests = [
        test_basic_imports,
        test_assets_exist,
        test_demo_script,
        test_pipeline_help,
        test_pipeline_basic,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
        print()
    
    print("=" * 30)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())