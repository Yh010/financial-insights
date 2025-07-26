# 🎤 Audio Features Documentation

This document describes the audio processing capabilities added to your financial insights application.

## Overview

The audio feature allows users to:
1. **Upload audio files** containing receipt information
2. **Convert audio to text** using Google Cloud Speech-to-Text
3. **Extract receipt data** from the transcribed text using Gemini AI
4. **Create wallet passes** directly from audio input

## 🚀 New Endpoints

### 1. Audio Transcription
**Endpoint:** `POST /audio/transcribe`

Converts audio to text using Google Cloud Speech-to-Text.

**Request:**
```bash
curl -X POST "http://localhost:8000/audio/transcribe" \
  -F "audio_file=@receipt_audio.mp3" \
  -F "language_code=en-US"
```

**Response:**
```json
{
  "status": "success",
  "transcript": "I bought groceries at Walmart for $45.67 on March 15th",
  "language_code": "en-US"
}
```

### 2. Audio Receipt Processing
**Endpoint:** `POST /audio/process-receipt`

Converts audio to text and extracts structured receipt data.

**Request:**
```bash
curl -X POST "http://localhost:8000/audio/process-receipt" \
  -F "audio_file=@receipt_audio.mp3" \
  -F "language_code=en-US"
```

**Response:**
```json
{
  "status": "success",
  "receipt_data": {
    "merchant_name": "Walmart",
    "purchase_date": "2024-03-15",
    "total_amount": 45.67,
    "tax_amount": 3.45,
    "items": [
      {
        "description": "Groceries",
        "quantity": 1,
        "price": 45.67
      }
    ]
  },
  "language_code": "en-US"
}
```

### 3. Complete Audio to Wallet Pass
**Endpoint:** `POST /audio/create-pass-from-audio`

Complete pipeline: Audio → Text → Receipt Data → Wallet Pass

**Request:**
```bash
curl -X POST "http://localhost:8000/audio/create-pass-from-audio" \
  -F "audio_file=@receipt_audio.mp3" \
  -F "language_code=en-US"
```

**Response:**
```json
{
  "status": "success",
  "wallet_save_url": "https://pay.google.com/gp/v/save/...",
  "receipt_data": {
    "merchant_name": "Walmart",
    "purchase_date": "2024-03-15",
    "total_amount": 45.67,
    "tax_amount": 3.45,
    "items": [...]
  },
  "transcript": "I bought groceries at Walmart for $45.67 on March 15th"
}
```

### 4. Enhanced Chat with Audio
**Endpoint:** `POST /api/chat`

The existing chat endpoint now supports audio files alongside text and images.

**Request:**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -F "query=Please process this receipt" \
  -F "audio_files=@receipt_audio.mp3" \
  -F "images=@receipt_image.jpg"
```

## 🛠️ Technical Implementation

### Audio Processing Pipeline

1. **Audio Format Conversion**
   - Supports multiple formats: MP3, WAV, M4A, etc.
   - Converts to 16-bit PCM WAV (required by Google Speech-to-Text)
   - Uses FFmpeg for conversion with pydub fallback

2. **Speech-to-Text**
   - Google Cloud Speech-to-Text API
   - Supports multiple languages
   - Automatic punctuation and confidence scoring

3. **Receipt Extraction**
   - Gemini AI processes transcribed text
   - Extracts structured receipt data
   - Returns JSON format for wallet pass creation

4. **Wallet Pass Creation**
   - Uses existing wallet service
   - Creates Google Wallet pass from extracted data

### Supported Audio Formats

- **MP3** (most common)
- **WAV**
- **M4A**
- **AAC**
- **OGG**
- **FLAC**

### Language Support

- **English (US)** - `en-US` (default)
- **English (UK)** - `en-GB`
- **Spanish** - `es-ES`
- **French** - `fr-FR`
- **German** - `de-DE`
- **And many more...**

## 📋 Setup Requirements

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Google Cloud Setup
Ensure you have:
- Google Cloud Speech-to-Text API enabled
- Proper authentication (service account or application default credentials)
- Sufficient quota for audio processing

### 3. FFmpeg Installation
For audio format conversion:

**Windows:**
```bash
# Download from https://ffmpeg.org/download.html
# Add to PATH environment variable
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

## 🧪 Testing

Use the provided test script:

```bash
cd backend
python test_audio.py
```

Make sure to:
1. Place a test audio file named `test_audio.mp3` in the backend directory
2. Start your FastAPI server: `uvicorn app.main:app --reload`

## 💡 Usage Examples

### Example 1: Simple Audio Transcription
```python
import requests

with open("receipt_audio.mp3", "rb") as audio_file:
    response = requests.post(
        "http://localhost:8000/audio/transcribe",
        files={"audio_file": audio_file},
        data={"language_code": "en-US"}
    )
    
    if response.status_code == 200:
        transcript = response.json()["transcript"]
        print(f"Transcript: {transcript}")
```

### Example 2: Complete Audio to Wallet Pass
```python
import requests

with open("receipt_audio.mp3", "rb") as audio_file:
    response = requests.post(
        "http://localhost:8000/audio/create-pass-from-audio",
        files={"audio_file": audio_file},
        data={"language_code": "en-US"}
    )
    
    if response.status_code == 200:
        result = response.json()
        wallet_url = result["wallet_save_url"]
        print(f"Wallet Pass URL: {wallet_url}")
```

## 🔧 Configuration

### Environment Variables
Add these to your `.env` file:

```env
# Google Cloud Speech-to-Text
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# Audio Processing
AUDIO_MAX_FILE_SIZE=10485760  # 10MB
AUDIO_SUPPORTED_FORMATS=mp3,wav,m4a,aac,ogg,flac
```

### Audio Processing Settings
You can customize audio processing in `app/functions/audio_processor.py`:

- **Sample Rate**: 16000 Hz (default)
- **Channels**: Mono (default)
- **Encoding**: 16-bit PCM
- **Model**: `latest_long` (for better accuracy)

## 🚨 Error Handling

The system handles various error scenarios:

- **Invalid audio format**: Returns 400 error
- **File too large**: Returns 413 error
- **Transcription failure**: Returns 500 error with details
- **Network issues**: Retries with exponential backoff

## 📊 Performance Considerations

- **Audio file size**: Keep under 10MB for optimal performance
- **Processing time**: ~2-5 seconds for typical receipts
- **Concurrent requests**: Limited by Google Cloud quotas
- **Caching**: Consider implementing transcript caching for repeated audio

## 🔮 Future Enhancements

Potential improvements:
- **Real-time streaming**: WebSocket support for live audio
- **Voice commands**: Natural language processing for commands
- **Multi-language receipts**: Automatic language detection
- **Audio quality enhancement**: Noise reduction and audio preprocessing
- **Batch processing**: Multiple audio files in one request

## 📞 Support

For issues or questions:
1. Check the logs for detailed error messages
2. Verify Google Cloud API quotas and billing
3. Test with different audio formats and qualities
4. Ensure proper authentication setup 