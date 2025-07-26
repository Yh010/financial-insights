# Financial Assistant Backend - Frontend Generation Prompt

## Project Overview
This is a **Financial Assistant Application** built with FastAPI that provides intelligent financial document processing, analysis, and Google Wallet integration. The application uses Google's Agent Development Kit (ADK) with Gemini 2.5 Pro to create a multi-agent system for handling various financial tasks.

## Core Functionality

### 1. Multi-Agent Architecture
The backend implements a sophisticated agent-based system with the following components:

- **Root Coordinator Agent**: Routes user queries to appropriate sub-agents based on intent
- **Greeter Agent**: Handles initial greetings and user onboarding
- **Calculator Agent**: Provides general financial information and answers queries using Google Search
- **Extractor Agent**: Processes receipt images and extracts structured data
- **Corpus Uploader Agent**: Manages document uploads to RAG (Retrieval-Augmented Generation) corpus
- **Retriever Agent**: Answers questions using uploaded documents via RAG

### 2. Key Features

#### Document Processing & Analysis
- **Receipt Image Processing**: Users can upload receipt images (JPG/PNG) for automatic data extraction
- **Structured Data Extraction**: Extracts merchant name, purchase date, total amount, tax amount, and itemized purchases
- **RAG Document Management**: Upload and query personal financial documents for intelligent retrieval

#### Google Wallet Integration
- **Digital Receipt Passes**: Automatically creates Google Wallet passes from extracted receipt data
- **Pass Management**: Generates signed JWTs for secure wallet pass creation
- **Visual Pass Design**: Customizable pass appearance with merchant logos and purchase details

#### AI-Powered Financial Assistance
- **General Financial Queries**: Answer questions about stocks, ETFs, inflation, etc.
- **Document-Based Q&A**: Query uploaded financial documents using RAG
- **Intelligent Routing**: Automatically directs users to the most appropriate agent

## API Endpoints

### Core Endpoints
- `POST /run` - Main agent interaction endpoint
- `POST /extract` - Extract data from receipt images
- `POST /gemini` - Direct Gemini AI interaction with image support
- `POST /rag/upload` - Upload documents to RAG corpus

### Google Wallet Endpoints
- `POST /setup/create-wallet-class` - Create wallet pass class (one-time setup)
- `POST /tools/create-receipt-pass` - Generate Google Wallet pass from receipt data

## Data Models

### Receipt Data Structure
```json
{
  "merchant_name": "string",
  "purchase_date": "YYYY-MM-DD",
  "total_amount": "float",
  "tax_amount": "float",
  "items": [
    {
      "description": "string",
      "quantity": "integer",
      "price": "float"
    }
  ]
}
```

### Agent Query Request
```json
{
  "query": "string"
}
```

## User Interaction Flow

### 1. Receipt Processing Flow
1. User uploads receipt image(s)
2. System extracts structured data using Gemini AI
3. Data is automatically uploaded to RAG corpus
4. User can optionally create Google Wallet pass
5. User can query extracted data later

### 2. Document Query Flow
1. User uploads financial documents to RAG corpus
2. User asks questions about uploaded documents
3. System retrieves relevant information using RAG
4. Provides answers with source citations

### 3. General Financial Q&A Flow
1. User asks general financial questions
2. System uses Google Search to find current information
3. Provides comprehensive, up-to-date answers

## Technical Requirements

### Backend Dependencies
- FastAPI 0.110.2
- Google ADK (Agent Development Kit)
- Vertex AI with Gemini 2.5 Pro
- Google Cloud Platform integration
- JWT handling for Google Wallet
- RAG (Retrieval-Augmented Generation) capabilities

### Environment Setup
- Google Cloud Project configuration
- Service account authentication
- Google Wallet API setup
- Vertex AI RAG corpus configuration

## Frontend Requirements

### Core UI Components Needed

#### 1. Chat Interface
- **Real-time messaging**: Support for text-based conversations with the AI agent
- **Message history**: Display conversation history with proper threading
- **Loading states**: Show when agents are processing requests
- **Error handling**: Graceful error display and retry mechanisms

#### 2. File Upload System
- **Image upload**: Drag-and-drop or file picker for receipt images
- **Document upload**: Support for various document formats (PDF, DOC, TXT)
- **Upload progress**: Visual feedback during file processing
- **File validation**: Check file types and sizes
- **Batch upload**: Support for multiple files

#### 3. Receipt Management
- **Receipt display**: Show extracted receipt data in structured format
- **Google Wallet integration**: "Save to Wallet" button with proper styling
- **Receipt history**: List of processed receipts with search/filter
- **Data editing**: Allow users to correct extracted data before wallet creation

#### 4. Document Library
- **Document list**: Display uploaded documents with metadata
- **Search functionality**: Search through uploaded documents
- **Document viewer**: Preview uploaded documents
- **RAG query interface**: Ask questions about uploaded documents

#### 5. Dashboard/Overview
- **Summary statistics**: Total receipts processed, documents uploaded
- **Recent activity**: Latest receipts and queries
- **Quick actions**: Common tasks accessible from main view

### Design Requirements

#### Visual Design
- **Modern, clean interface**: Professional financial application aesthetic
- **Responsive design**: Work on desktop, tablet, and mobile
- **Accessibility**: WCAG compliance for inclusive design
- **Dark/light mode**: Optional theme switching

#### User Experience
- **Intuitive navigation**: Clear information architecture
- **Progressive disclosure**: Show relevant information at appropriate times
- **Contextual help**: Tooltips and guidance for complex features
- **Keyboard shortcuts**: Power user features for efficiency

### Technical Frontend Requirements

#### Technology Stack Recommendations
- **React/Vue/Angular**: Modern JavaScript framework
- **TypeScript**: Type safety for better development experience
- **State management**: Redux, Zustand, or similar for complex state
- **HTTP client**: Axios or fetch for API communication
- **File handling**: Robust file upload with progress tracking
- **Real-time updates**: WebSocket or polling for live updates

#### API Integration
- **RESTful communication**: Proper error handling and loading states
- **File upload**: Multipart form data handling
- **Authentication**: JWT token management (if implemented)
- **CORS handling**: Proper cross-origin request configuration

#### Performance Considerations
- **Image optimization**: Compress and resize uploaded images
- **Lazy loading**: Load components and data as needed
- **Caching**: Cache frequently accessed data
- **Progressive loading**: Show skeleton screens during data fetch

### Security Considerations
- **File validation**: Client-side and server-side file type checking
- **Data privacy**: Secure handling of financial information
- **HTTPS**: Ensure all communications are encrypted
- **Input sanitization**: Prevent XSS and injection attacks

## User Personas & Use Cases

### Primary User: Individual Consumer
- **Use case**: Upload grocery receipts, track spending, create digital wallet passes
- **Pain points**: Manual receipt entry, lost receipts, no digital backup
- **Goals**: Automated expense tracking, digital receipt storage, easy wallet integration

### Secondary User: Small Business Owner
- **Use case**: Process business receipts, query financial documents, get financial advice
- **Pain points**: Time-consuming manual data entry, scattered financial information
- **Goals**: Automated document processing, centralized financial information, quick financial insights

## Success Metrics
- **User engagement**: Time spent in application, feature usage
- **Processing accuracy**: Receipt extraction success rate
- **User satisfaction**: Ease of use, feature completeness
- **Performance**: Upload speed, query response time

## Future Enhancement Opportunities
- **Expense categorization**: Automatic categorization of purchases
- **Budget tracking**: Set budgets and track spending against them
- **Financial insights**: AI-powered spending analysis and recommendations
- **Multi-currency support**: Handle international receipts and currencies
- **Integration**: Connect with banking APIs for automatic transaction import
- **Mobile app**: Native mobile application for on-the-go receipt capture

This comprehensive financial assistant backend provides a solid foundation for building a sophisticated frontend that can handle complex financial workflows while maintaining a user-friendly experience. 