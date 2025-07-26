#!/usr/bin/env python3
"""
Test script to verify audio processing functionality.
"""

import os
import tempfile
from app.functions.audio_processor import (
    detect_audio_format,
    detect_audio_encoding,
    convert_audio_format,
    transcribe_audio,
    check_ffmpeg_available
)

def create_test_audio():
    """Create a simple test audio file for testing."""
    try:
        from pydub import AudioSegment
        from pydub.generators import Sine
        
        # Create a simple sine wave audio
        audio = Sine(440).to_audio_segment(duration=2000)  # 2 seconds at 440Hz
        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        
        # Save as WAV
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            audio.export(temp_file.name, format="wav")
            return temp_file.name
    except Exception as e:
        print(f"Could not create test audio: {e}")
        return None

def test_audio_processing():
    """Test audio processing functionality."""
    print("🧪 Testing Audio Processing...")
    print("=" * 50)
    
    # Test 1: Check FFmpeg availability
    print("\n1. Checking FFmpeg availability...")
    ffmpeg_available = check_ffmpeg_available()
    print(f"FFmpeg available: {ffmpeg_available}")
    
    # Test 2: Create test audio
    print("\n2. Creating test audio...")
    test_audio_path = create_test_audio()
    if test_audio_path:
        print(f"✅ Test audio created: {test_audio_path}")
        
        # Test 3: Read and process test audio
        print("\n3. Testing audio processing...")
        try:
            with open(test_audio_path, 'rb') as f:
                audio_bytes = f.read()
            
            # Test format detection
            detected_format = detect_audio_format(audio_bytes, "test.wav")
            print(f"✅ Format detection: {detected_format}")
            
            # Test encoding detection
            detected_encoding = detect_audio_encoding(audio_bytes, "test.wav")
            print(f"✅ Encoding detection: {detected_encoding}")
            
            # Test conversion
            try:
                converted_audio = convert_audio_format(audio_bytes, detected_format)
                print(f"✅ Audio conversion successful: {len(converted_audio)} bytes")
            except Exception as e:
                print(f"❌ Audio conversion failed: {e}")
            
            # Clean up
            os.unlink(test_audio_path)
            print("✅ Test audio cleaned up")
            
        except Exception as e:
            print(f"❌ Audio processing test failed: {e}")
            if test_audio_path and os.path.exists(test_audio_path):
                os.unlink(test_audio_path)
    else:
        print("❌ Could not create test audio")
    
    # Test 4: Test format detection for different extensions
    print("\n4. Testing format detection for different extensions...")
    test_extensions = [".mp3", ".wav", ".webm", ".m4a", ".flac"]
    for ext in test_extensions:
        detected = detect_audio_format(b"fake_audio_data", f"test{ext}")
        print(f"  {ext} -> {detected}")
    
    print("\n" + "=" * 50)
    print("🎯 Audio Processing Test Complete!")
    print("\n💡 Next steps:")
    print("  - Test with real audio files")
    print("  - Test transcription with Google Cloud Speech")
    print("  - Install FFmpeg for better format support")

if __name__ == "__main__":
    test_audio_processing() 