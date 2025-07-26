#!/usr/bin/env python3
"""
Simple test to verify audio processor imports work correctly.
"""

def test_imports():
    """Test that all audio processor imports work."""
    try:
        print("Testing audio processor imports...")
        
        # Test Google Cloud Speech import
        from google.cloud import speech
        print("✅ google.cloud.speech imported successfully")
        
        # Test audio processor import
        from app.functions.audio_processor import transcribe_audio, process_audio_receipt
        print("✅ audio_processor functions imported successfully")
        
        # Test other dependencies
        from pydub import AudioSegment
        print("✅ pydub imported successfully")
        
        import ffmpeg
        print("✅ ffmpeg-python imported successfully")
        
        print("\n🎉 All imports successful! Audio processor is ready to use.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_imports() 