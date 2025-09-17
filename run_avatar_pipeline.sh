#!/bin/bash

set -e

echo "=== Fast-Track-Academy: One-Click Avatar Video Pipeline ==="

# 1. Check for Python 3.8+
PYTHON_CMD="python3"
if ! command -v $PYTHON_CMD &>/dev/null; then
    PYTHON_CMD="python"
    if ! command -v $PYTHON_CMD &>/dev/null; then
        echo "Python 3.8+ is required but was not found. Please install Python 3.8 or higher."
        exit 1
    fi
fi

PY_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PY_MAJOR=$(echo $PY_VERSION | cut -d. -f1)
PY_MINOR=$(echo $PY_VERSION | cut -d. -f2)
if [ "$PY_MAJOR" -lt "3" ] || { [ "$PY_MAJOR" -eq "3" ] && [ "$PY_MINOR" -lt "8" ]; }; then
    echo "Python 3.8+ is required. Found Python $PY_VERSION"
    exit 1
fi

# 2. Check for pip
if ! command -v pip &>/dev/null && ! command -v pip3 &>/dev/null; then
    echo "pip is required but was not found. Please install pip."
    exit 1
fi

PIP_CMD="pip"
if ! command -v $PIP_CMD &>/dev/null; then
    PIP_CMD="pip3"
fi

# 3. Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    $PYTHON_CMD -m venv venv
fi

# 4. Activate virtual environment
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# 5. Install dependencies
echo "Installing required Python packages..."
$PIP_CMD install --upgrade pip
$PIP_CMD install -r requirements.txt

# 6. Download Whisper and SadTalker models if needed (placeholder, customize as needed)
echo "Ensuring Whisper and SadTalker models are present..."
mkdir -p models
if [ ! -f "models/whisper_model.pt" ]; then
    echo "Downloading Whisper model (placeholder)..."
    # Insert Whisper model download command here, e.g.:
    # python -m whisper download tiny --output_dir models
    echo "(Please manually download or update this section for real model fetching.)"
fi
if [ ! -f "models/sadtalker_model.ckpt" ]; then
    echo "Downloading SadTalker model (placeholder)..."
    # Insert SadTalker model download command here, e.g.:
    # wget -O models/sadtalker_model.ckpt <SadTalker model URL>
    echo "(Please manually download or update this section for real model fetching.)"
fi

# 7. Prompt for input
echo
echo "Choose input mode:"
echo "1) Record from microphone"
echo "2) Use audio file"
read -p "Enter 1 or 2: " mode_choice

if [ "$mode_choice" == "1" ]; then
    read -p "Enter duration of recording in seconds (default: 10): " duration
    duration=${duration:-10}
    MODE="record"
    ARGS="--mode record --duration $duration"
elif [ "$mode_choice" == "2" ]; then
    read -p "Enter path to audio file: " audio_file
    if [ ! -f "$audio_file" ]; then
        echo "Audio file not found: $audio_file"
        exit 1
    fi
    read -p "Enter path to avatar image (press Enter to use default): " avatar_image
    if [ -n "$avatar_image" ] && [ ! -f "$avatar_image" ]; then
        echo "Avatar image not found: $avatar_image"
        exit 1
    fi
    MODE="file"
    ARGS="--mode file --audio \"$audio_file\""
    if [ -n "$avatar_image" ]; then
        ARGS="$ARGS --avatar \"$avatar_image\""
    fi
else
    echo "Invalid choice."
    exit 1
fi

# 8. Run the pipeline
echo ""
echo "Running avatar generation pipeline..."
eval "$PYTHON_CMD avatar_pipeline.py $ARGS"

echo ""
echo "If successful, the generated video should be in the output directory."
echo "=== Done ==="