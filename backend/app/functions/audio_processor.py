"""
Audio processing functionality for converting audio to text.
Uses Google Cloud Speech-to-Text API for transcription.
"""

import os
import io
import tempfile
import mimetypes
import subprocess
from typing import Optional
from google.cloud import speech
from pydub import AudioSegment
import ffmpeg

def check_ffmpeg_available() -> bool:
    """
    Check if FFmpeg is available on the system.
    
    Returns:
        bool: True if FFmpeg is available, False otherwise
    """
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        return False

def detect_audio_format(audio_bytes: bytes, filename: str = "") -> str:
    """
    Detect audio format from file extension or content.
    
    Args:
        audio_bytes: Raw audio bytes
        filename: Optional filename for extension detection
    
    Returns:
        str: Detected audio format
    """
    # Try to detect from filename first
    if filename:
        ext = os.path.splitext(filename)[1].lower()
        if ext in ['.mp3', '.wav', '.m4a', '.aac', '.ogg', '.flac', '.webm']:
            return ext[1:]  # Remove the dot
    
    # Try to detect from content using mimetypes
    try:
        mime_type, _ = mimetypes.guess_type(filename or "audio.mp3")
        if mime_type:
            if 'mp3' in mime_type:
                return 'mp3'
            elif 'wav' in mime_type:
                return 'wav'
            elif 'm4a' in mime_type or 'aac' in mime_type:
                return 'm4a'
            elif 'ogg' in mime_type:
                return 'ogg'
            elif 'flac' in mime_type:
                return 'flac'
            elif 'webm' in mime_type:
                return 'webm'
    except:
        pass
    
    # Default to mp3 if detection fails
    return "mp3"

def detect_audio_encoding(audio_bytes: bytes, filename: str = "") -> str:
    """
    Detect the audio encoding from the file content or extension.
    
    Args:
        audio_bytes: Raw audio bytes
        filename: Optional filename for extension detection
    
    Returns:
        str: Detected encoding (LINEAR16, FLAC, MULAW, etc.)
    """
    # Try to detect from filename first
    if filename:
        ext = os.path.splitext(filename)[1].lower()
        if ext == '.wav':
            return 'LINEAR16'
        elif ext == '.flac':
            return 'FLAC'
        elif ext == '.mp3':
            return 'MP3'
        elif ext == '.webm':
            return 'WEBM_OPUS'
        elif ext == '.m4a':
            return 'MP3'  # M4A is typically AAC but we'll treat as MP3
    
    # Default to LINEAR16 for unknown formats
    return 'LINEAR16'

def convert_audio_format(audio_bytes: bytes, input_format: str = "mp3") -> bytes:
    """
    Convert audio to the format required by Google Speech-to-Text (16-bit PCM WAV).
    
    Args:
        audio_bytes: Raw audio bytes
        input_format: Input audio format (mp3, wav, m4a, etc.)
    
    Returns:
        bytes: Converted audio in WAV format
    """
    # First try using pydub (doesn't require external FFmpeg)
    try:
        print(f"Attempting pydub conversion for {input_format}...")
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=input_format)
        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        
        output = io.BytesIO()
        audio.export(output, format="wav")
        print("✅ Pydub conversion successful")
        return output.getvalue()
        
    except Exception as e:
        print(f"Pydub conversion failed: {e}")
        
        # Fallback: try using ffmpeg if available
        if check_ffmpeg_available():
            try:
                print("Attempting ffmpeg conversion...")
                # Create temporary files for conversion
                with tempfile.NamedTemporaryFile(suffix=f".{input_format}", delete=False) as temp_input:
                    temp_input.write(audio_bytes)
                    temp_input_path = temp_input.name
                
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_output:
                    temp_output_path = temp_output.name
                
                # Convert using ffmpeg
                (
                    ffmpeg
                    .input(temp_input_path)
                    .output(temp_output_path, 
                           acodec='pcm_s16le',  # 16-bit PCM
                           ac=1,                # Mono channel
                           ar=16000)            # 16kHz sample rate
                    .overwrite_output()
                    .run(capture_stdout=True, capture_stderr=True)
                )
                
                # Read the converted audio
                with open(temp_output_path, 'rb') as f:
                    converted_audio = f.read()
                
                # Clean up temporary files
                os.unlink(temp_input_path)
                os.unlink(temp_output_path)
                
                print("✅ FFmpeg conversion successful")
                return converted_audio
                
            except Exception as e2:
                print(f"FFmpeg conversion also failed: {e2}")
        else:
            print("FFmpeg not available, skipping ffmpeg conversion")
        
        # Last resort: try to use the original audio if it's already WAV
        if input_format.lower() == "wav":
            print("Using original WAV audio as fallback")
            return audio_bytes
        elif input_format.lower() == "webm":
            # For WebM files, try to convert to a simpler format
            try:
                print("Attempting WebM to WAV conversion with pydub...")
                # Try to load as WebM and export as WAV
                audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="webm")
                audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
                
                output = io.BytesIO()
                audio.export(output, format="wav")
                print("✅ WebM to WAV conversion successful")
                return output.getvalue()
            except Exception as webm_error:
                print(f"WebM conversion failed: {webm_error}")
                # If all else fails, try to use the original audio
                print("Using original WebM audio as last resort")
                return audio_bytes
        else:
            raise Exception(f"Audio conversion failed for format {input_format}. Please install FFmpeg or ensure audio is in a supported format.")

def transcribe_audio(audio_bytes: bytes, language_code: str = "en-US", filename: str = "") -> str:
    """
    Transcribe audio to text using Google Cloud Speech-to-Text.
    
    Args:
        audio_bytes: Audio file bytes
        language_code: Language code for transcription (default: en-US)
        filename: Optional filename for format detection
    
    Returns:
        str: Transcribed text
    """
    try:
        # Initialize the Speech client
        client = speech.SpeechClient()
        
        # Detect audio format and convert to proper format
        detected_format = detect_audio_format(audio_bytes, filename)
        print(f"Detected audio format: {detected_format}")
        
        try:
            converted_audio = convert_audio_format(audio_bytes, detected_format)
        except Exception as e:
            print(f"Failed to convert {detected_format}, trying fallback formats...")
            # Try fallback formats
            for fallback_format in ["wav", "mp3", "webm"]:
                if fallback_format != detected_format:
                    try:
                        converted_audio = convert_audio_format(audio_bytes, fallback_format)
                        print(f"Successfully converted using {fallback_format}")
                        break
                    except:
                        continue
            else:
                raise e
        
        # Create the audio object
        audio = speech.RecognitionAudio(content=converted_audio)
        
        # Detect encoding and configure recognition accordingly
        detected_encoding = detect_audio_encoding(audio_bytes, filename)
        print(f"Using encoding: {detected_encoding}")
        
        # Configure the recognition based on detected encoding
        if detected_encoding == 'WEBM_OPUS':
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
                language_code=language_code,
                enable_automatic_punctuation=True,
                enable_word_time_offsets=False,
                enable_word_confidence=True,
                model="latest_long",
            )
        elif detected_encoding == 'FLAC':
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
                language_code=language_code,
                enable_automatic_punctuation=True,
                enable_word_time_offsets=False,
                enable_word_confidence=True,
                model="latest_long",
            )
        elif detected_encoding == 'MP3':
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.MP3,
                language_code=language_code,
                enable_automatic_punctuation=True,
                enable_word_time_offsets=False,
                enable_word_confidence=True,
                model="latest_long",
            )
        else:
            # Default to LINEAR16
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                language_code=language_code,
                enable_automatic_punctuation=True,
                enable_word_time_offsets=False,
                enable_word_confidence=True,
                model="latest_long",
            )
        
        # Perform the transcription
        response = client.recognize(config=config, audio=audio)
        
        # Extract the transcribed text
        transcript = ""
        for result in response.results:
            if result.alternatives:
                transcript += result.alternatives[0].transcript + " "
        
        return transcript.strip()
        
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        raise e

def process_audio_receipt(audio_bytes: bytes, language_code: str = "en-US", filename: str = "") -> str:
    """
    Process audio receipt and extract receipt information.
    
    Args:
        audio_bytes: Audio file bytes containing receipt information
        language_code: Language code for transcription
        filename: Optional filename for format detection
    
    Returns:
        str: Extracted receipt information in text format
    """
    try:
        # Step 1: Convert audio to text
        print("Converting audio to text...")
        transcript = transcribe_audio(audio_bytes, language_code, filename)
        print(f"Transcription: {transcript}")
        
        # Step 2: Process the transcript through Gemini for receipt extraction
        from .gemini import generate
        
        prompt = f"""
        You are an expert financial assistant. The user has provided audio describing a receipt.
        Please extract the receipt information from the following transcript and format it as JSON:
        
        Transcript: {transcript}
        
        Please extract and return the following information in JSON format:
        {{
            "merchant_name": "store name",
            "purchase_date": "YYYY-MM-DD",
            "total_amount": 0.00,
            "tax_amount": 0.00,
            "items": [
                {{
                    "description": "item name",
                    "quantity": 1,
                    "price": 0.00
                }}
            ]
        }}
        
        If any information is not available, use null for that field.
        """
        
        # Generate structured receipt data
        response = generate(prompt)
        return response
        
    except Exception as e:
        print(f"Error processing audio receipt: {e}")
        raise e 