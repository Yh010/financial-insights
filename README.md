# Financial Assistant with Server-Sent Events (SSE)

A modern financial assistant application built with Google's Agent Development Kit (ADK) and React, featuring real-time communication using Server-Sent Events (SSE).

## Features

- 🤖 **AI-Powered Financial Assistant**: Built with Google ADK agents
- 🔄 **Real-time Streaming**: Server-Sent Events for live response streaming
- 💬 **Interactive Chat Interface**: Modern React frontend with real-time updates
- 📊 **Financial Analysis**: Receipt analysis, document queries, and financial guidance
- 🧾 **Receipt Processing**: Upload and analyze receipts
- 📄 **Document Retrieval**: Query uploaded documents
- 💳 **Google Wallet Integration**: Generate wallet passes from receipts

## Architecture

### Backend (FastAPI + Google ADK)
- **FastAPI**: Modern Python web framework
- **Google ADK**: Agent Development Kit for AI agents
- **SSE Endpoints**: Real-time streaming communication
- **CORS Support**: Cross-origin resource sharing
- **Session Management**: In-memory session handling

### Frontend (React + Zustand)
- **React**: Modern UI framework
- **Zustand**: Lightweight state management
- **SSE Client**: Real-time event handling
- **Responsive Design**: Mobile-friendly interface

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- Google Cloud Project with ADK enabled
- Environment variables configured

### Backend Setup

1. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:
   Create a `.env` file in `backend/app/`:
   ```env
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_BUCKET=your-bucket-name
   WALLET_ISSUER_ID=your-wallet-issuer-id
   ```

3. **Start the backend server**:
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm run dev
   ```

3. **Open your browser**:
   Navigate to `http://localhost:5173`

## API Endpoints

### SSE Endpoints
- `GET /events/{user_id}`: Server-Sent Events stream for real-time agent responses
- `POST /send/{user_id}`: Send messages to the agent

### Legacy Endpoints (Backward Compatibility)
- `POST /invoke`: Single request endpoint for simple queries

### Utility Endpoints
- `POST /gemini`: Direct Gemini API calls
- `POST /extract`: Receipt extraction
- `POST /tools/create-receipt-pass`: Generate Google Wallet passes
- `POST /setup/create-wallet-class`: Create wallet pass class

## SSE Implementation Details

### Backend SSE Flow
1. **Session Creation**: Each user gets a unique session with ADK agent
2. **Event Streaming**: Agent responses streamed as SSE events
3. **Message Handling**: Client messages sent via HTTP POST
4. **Cleanup**: Automatic session cleanup on disconnect

### Frontend SSE Flow
1. **Connection**: Establish SSE connection on component mount
2. **Message Sending**: Send messages via HTTP POST
3. **Real-time Updates**: Handle streaming responses
4. **State Management**: Zustand store for global state
5. **Error Handling**: Graceful connection loss handling

### Message Types
```json
{
  "type": "content",
  "content": "Streaming text content",
  "partial": true
}
```

```json
{
  "type": "status",
  "turn_complete": true,
  "interrupted": false
}
```

## State Management

The application uses Zustand for global state management:

```javascript
const useAgentStore = create((set, get) => ({
  interactions: [],        // Chat history
  isProcessing: false,     // Loading state
  isConnected: false,      // SSE connection status
  currentResponse: '',     // Streaming response
  error: null,            // Error state
  
  // Actions for state updates
  sendMessage: async (message, adkClient) => { ... },
  handleSSEMessage: (data) => { ... },
  handleSSEError: (error) => { ... }
}))
```

## CORS Configuration

The backend is configured with CORS middleware:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Error Handling

### Backend Errors
- **Session not found**: Return error when SSE connection not established
- **Agent errors**: Graceful handling of agent failures
- **Connection cleanup**: Automatic resource cleanup

### Frontend Errors
- **Connection loss**: Automatic reconnection attempts
- **Message errors**: User-friendly error messages
- **SSE parsing errors**: Robust JSON parsing

## Development

### Adding New Agents
1. Create agent in `backend/app/sub_agents/`
2. Import in `backend/app/agent.py`
3. Add to tools list in root agent

### Extending SSE
1. Add new message types in backend
2. Handle new types in frontend store
3. Update UI components as needed

### Styling
- CSS modules for component styling
- Responsive design with mobile support
- Dark/light theme support (future)

## Production Deployment

### Backend
- Use production WSGI server (Gunicorn)
- Configure persistent session storage
- Set up proper CORS origins
- Enable HTTPS

### Frontend
- Build optimized production bundle
- Configure CDN for static assets
- Set up proper environment variables

## Troubleshooting

### Common Issues

1. **SSE Connection Fails**
   - Check CORS configuration
   - Verify backend is running
   - Check browser console for errors

2. **Agent Not Responding**
   - Verify Google Cloud credentials
   - Check ADK configuration
   - Review agent logs

3. **Frontend Not Updating**
   - Check Zustand store state
   - Verify SSE message parsing
   - Review React component updates

### Debug Mode
Enable debug logging by setting environment variables:
```env
DEBUG=true
LOG_LEVEL=DEBUG
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google ADK team for the Agent Development Kit
- FastAPI for the excellent web framework
- React team for the frontend framework
- Zustand for lightweight state management 