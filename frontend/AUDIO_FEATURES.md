# 🎤 Frontend Audio Features

This document describes the audio functionality added to the frontend React application.

## 🚀 Features Added

### 1. Enhanced Chat Interface (`App.tsx`)

The main chat interface now supports:

- **Audio file upload** - Upload existing audio files
- **Voice recording** - Record audio directly in the browser
- **Combined inputs** - Send text, images, and audio together
- **Audio preview** - Play uploaded/recorded audio before sending

### 2. Audio Testing Interface (`TestPage.tsx`)

A dedicated testing interface for audio features:

- **Comprehensive testing** - Test all audio endpoints
- **Real-time recording** - Record audio for testing
- **Result visualization** - See transcripts, receipt data, and wallet URLs
- **Error handling** - Clear error messages and debugging info

## 🎯 How to Use

### Chat Interface

1. **Navigate to the main app**: Go to `/app`
2. **Upload audio**: Click the microphone icon to upload an audio file
3. **Record audio**: Click the microphone button to start/stop recording
4. **Send message**: Combine with text and images, then send

### Audio Testing Interface

1. **Navigate to test page**: Go to `/test` or click "🎤 Test Audio" in the header
2. **Select audio input method**:
   - Upload an existing audio file
   - Record audio directly in the browser
3. **Run tests**: Click "Run All Audio Tests" to test all endpoints
4. **View results**: See transcripts, receipt data, and wallet URLs

## 🛠️ Technical Implementation

### Audio Recording

Uses the Web Audio API and MediaRecorder:

```typescript
const startRecording = async () => {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const mediaRecorder = new MediaRecorder(stream, {
    mimeType: 'audio/webm;codecs=opus'
  });
  // ... recording logic
};
```

### File Upload

Supports multiple audio formats:
- MP3, WAV, M4A, AAC, OGG, FLAC
- WebM (for recorded audio)

### API Integration

Sends audio files to backend endpoints:
- `/api/chat` - Combined chat with audio
- `/audio/transcribe` - Audio to text
- `/audio/process-receipt` - Audio to receipt data
- `/audio/create-pass-from-audio` - Complete pipeline

## 📱 UI Components

### Chat Interface Controls

- **📎 Paperclip** - Upload images
- **🎤 Mic** - Upload audio files
- **🎤 Mic (recording)** - Start/stop voice recording
- **📤 Send** - Send message with all attachments

### Audio Tester Interface

- **Upload Audio** - Select existing audio files
- **Start/Stop Recording** - Record audio directly
- **Run All Tests** - Test all audio endpoints
- **Results Display** - Show transcripts, data, and wallet URLs

## 🎨 Styling

Uses Tailwind CSS with custom styling:

- **Green theme** for audio-related elements
- **Blue theme** for image uploads
- **Red theme** for recording state
- **Responsive design** for mobile and desktop

## 🔧 Configuration

### Environment Variables

Add to your `.env` file:

```env
VITE_BACKEND_URL=http://localhost:8000
```

### Browser Permissions

The app requires microphone access for recording:

```javascript
// Request microphone permission
navigator.mediaDevices.getUserMedia({ audio: true })
```

## 🧪 Testing

### Manual Testing

1. **Start the backend**: `cd backend && uvicorn app.main:app --reload`
2. **Start the frontend**: `cd frontend && npm run dev`
3. **Navigate to test page**: Go to `http://localhost:5173/test`
4. **Test audio features**: Upload or record audio and run tests

### Test Scenarios

- **Audio upload**: Upload various audio formats
- **Voice recording**: Record audio in different browsers
- **Combined inputs**: Send text + image + audio together
- **Error handling**: Test with invalid files and network errors

## 🚨 Browser Compatibility

### Supported Browsers

- **Chrome** - Full support (recommended)
- **Firefox** - Full support
- **Safari** - Limited support (may need polyfills)
- **Edge** - Full support

### MediaRecorder Support

```javascript
// Check if MediaRecorder is supported
if (typeof MediaRecorder !== 'undefined') {
  // Recording is supported
} else {
  // Fallback to file upload only
}
```

## 🔮 Future Enhancements

### Planned Features

- **Real-time transcription** - Live audio to text
- **Voice commands** - Natural language processing
- **Audio quality settings** - Adjust recording quality
- **Batch processing** - Multiple audio files
- **Audio editing** - Trim and enhance audio

### Performance Optimizations

- **Audio compression** - Reduce file sizes
- **Streaming uploads** - Large file support
- **Caching** - Cache transcripts and results
- **Progressive loading** - Better UX for large files

## 📞 Troubleshooting

### Common Issues

1. **Microphone not working**
   - Check browser permissions
   - Ensure HTTPS in production
   - Try different browser

2. **Audio upload fails**
   - Check file format support
   - Verify file size limits
   - Check network connection

3. **Recording quality issues**
   - Use better microphone
   - Reduce background noise
   - Check browser settings

### Debug Mode

Enable debug logging:

```javascript
// In browser console
localStorage.setItem('debug', 'true');
```

## 📚 Resources

- [Web Audio API Documentation](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
- [MediaRecorder API](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder)
- [React Audio Components](https://reactjs.org/docs/hooks-reference.html)
- [Tailwind CSS Audio Components](https://tailwindcss.com/components) 