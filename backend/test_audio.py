"""
Test script for audio functionality.
This script helps test the audio processing endpoints.
"""

import requests
import json

# Test configuration
BASE_URL = "http://localhost:8000"
AUDIO_FILE_PATH = "test_audio.mp3"  # Replace with your test audio file

def test_audio_transcription():
    """Test the audio transcription endpoint."""
    print("Testing audio transcription...")
    
    try:
        with open(AUDIO_FILE_PATH, "rb") as audio_file:
            files = {"audio_file": audio_file}
            data = {"language_code": "en-US"}
            
            response = requests.post(
                f"{BASE_URL}/audio/transcribe",
                files=files,
                data=data
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Transcription successful!")
                print(f"Transcript: {result['transcript']}")
                return result['transcript']
            else:
                print(f"❌ Transcription failed: {response.text}")
                return None
                
    except FileNotFoundError:
        print(f"❌ Audio file not found: {AUDIO_FILE_PATH}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_audio_receipt_processing():
    """Test the audio receipt processing endpoint."""
    print("\nTesting audio receipt processing...")
    
    try:
        with open(AUDIO_FILE_PATH, "rb") as audio_file:
            files = {"audio_file": audio_file}
            data = {"language_code": "en-US"}
            
            response = requests.post(
                f"{BASE_URL}/audio/process-receipt",
                files=files,
                data=data
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Receipt processing successful!")
                print(f"Receipt data: {result['receipt_data']}")
                return result['receipt_data']
            else:
                print(f"❌ Receipt processing failed: {response.text}")
                return None
                
    except FileNotFoundError:
        print(f"❌ Audio file not found: {AUDIO_FILE_PATH}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_audio_pass_creation():
    """Test the complete audio to wallet pass pipeline."""
    print("\nTesting complete audio to wallet pass pipeline...")
    
    try:
        with open(AUDIO_FILE_PATH, "rb") as audio_file:
            files = {"audio_file": audio_file}
            data = {"language_code": "en-US"}
            
            response = requests.post(
                f"{BASE_URL}/audio/create-pass-from-audio",
                files=files,
                data=data
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Wallet pass creation successful!")
                print(f"Wallet URL: {result['wallet_save_url']}")
                print(f"Receipt data: {result['receipt_data']}")
                return result['wallet_save_url']
            else:
                print(f"❌ Wallet pass creation failed: {response.text}")
                return None
                
    except FileNotFoundError:
        print(f"❌ Audio file not found: {AUDIO_FILE_PATH}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_chat_with_audio():
    """Test the chat endpoint with audio."""
    print("\nTesting chat with audio...")
    
    try:
        with open(AUDIO_FILE_PATH, "rb") as audio_file:
            files = {"audio_files": audio_file}
            data = {"query": "Please process this audio and create a wallet pass"}
            
            response = requests.post(
                f"{BASE_URL}/api/chat",
                files=files,
                data=data
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Chat with audio successful!")
                print(f"Response: {result['response_text']}")
                return result['response_text']
            else:
                print(f"❌ Chat with audio failed: {response.text}")
                return None
                
    except FileNotFoundError:
        print(f"❌ Audio file not found: {AUDIO_FILE_PATH}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("🎤 Audio Functionality Test Suite")
    print("=" * 50)
    
    # Test individual endpoints
    test_audio_transcription()
    test_audio_receipt_processing()
    test_audio_pass_creation()
    test_chat_with_audio()
    
    print("\n" + "=" * 50)
    print("Test suite completed!") 