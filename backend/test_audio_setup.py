#!/usr/bin/env python3
"""
Test script to check audio processing setup and dependencies.
"""

def test_audio_setup():
    """Test audio processing setup and dependencies."""
    print("🔍 Testing Audio Processing Setup...")
    print("=" * 50)
    
    # Test 1: Check FFmpeg availability
    print("\n1. Checking FFmpeg availability...")
    try:
        from app.functions.audio_processor import check_ffmpeg_available
        ffmpeg_available = check_ffmpeg_available()
        if ffmpeg_available:
            print("✅ FFmpeg is available")
        else:
            print("❌ FFmpeg is not available (will use pydub fallback)")
    except Exception as e:
        print(f"❌ Error checking FFmpeg: {e}")
    
    # Test 2: Check pydub
    print("\n2. Checking pydub...")
    try:
        from pydub import AudioSegment
        print("✅ pydub is available")
    except ImportError as e:
        print(f"❌ pydub not available: {e}")
    
    # Test 3: Check Google Cloud Speech
    print("\n3. Checking Google Cloud Speech...")
    try:
        from google.cloud import speech
        print("✅ Google Cloud Speech is available")
    except ImportError as e:
        print(f"❌ Google Cloud Speech not available: {e}")
    
    # Test 4: Check audio processor imports
    print("\n4. Checking audio processor imports...")
    try:
        from app.functions.audio_processor import (
            detect_audio_format, 
            convert_audio_format, 
            transcribe_audio, 
            process_audio_receipt
        )
        print("✅ All audio processor functions imported successfully")
    except Exception as e:
        print(f"❌ Audio processor import error: {e}")
    
    # Test 5: Check ffmpeg-python
    print("\n5. Checking ffmpeg-python...")
    try:
        import ffmpeg
        print("✅ ffmpeg-python is available")
    except ImportError as e:
        print(f"❌ ffmpeg-python not available: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Setup Summary:")
    print("- If FFmpeg is available: Full audio format support")
    print("- If only pydub: Limited format support (MP3, WAV, etc.)")
    print("- If Google Cloud Speech works: Audio transcription available")
    print("\n💡 To install FFmpeg:")
    print("  - Windows: choco install ffmpeg")
    print("  - Or download from: https://ffmpeg.org/download.html")

if __name__ == "__main__":
    test_audio_setup() 