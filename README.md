# AI Chat Assistant

A modern web-based chat application that integrates with Google's Gemini AI to provide intelligent conversational responses. Built with Flask backend and a responsive HTML/CSS/JavaScript frontend.

## Features

- **AI-Powered Conversations**: Chat with Google Gemini 2.5 Flash or Gemini 2.0 Flash models
- **Chat History**: Persistent storage of conversations with automatic history management
- **Dark Mode**: Toggle between light and dark themes with persistent preference
- **Responsive Design**: Mobile-friendly interface that works on all devices
- **Rich Text Support**: Markdown rendering for formatted AI responses including headers, lists, code blocks, and tables
- **Real-time Updates**: Messages are sent and received in real-time with visual feedback
- **Dual API Integration**: Support for both Google Generative AI SDK and direct HTTP API

## Project Structure

```
ai_py/
├── app.py              # Flask application with API endpoints
├── main.py             # AI integration and text generation logic
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Frontend UI with JavaScript
└── chat_history/       # Chat conversation storage (auto-created)
    ├── *.json          # Individual chat files
```

## Installation

### Prerequisites

- Python 3.7 or higher
- Google Generative AI API key

### Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd c:\Users\Admin\Documents\flask_py\ai_py
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```
   
   Or set the environment variable directly in your system.

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Dependencies

- **Flask 2.3.3**: Web framework for Python
- **google-generativeai 0.3.1**: Google Generative AI SDK
- **python-dotenv 1.0.0**: Environment variable management
- **requests 2.32.5**: HTTP client for API calls

Install all dependencies with:
```bash
pip install -r requirements.txt
```

## Configuration

### API Key

The application requires a Google Generative AI API key. Set it via the `GOOGLE_API_KEY` environment variable in a `.env` file at the project root.

### Default Model

The application uses `models/gemini-2.5-flash` by default (SDK integration). For HTTP API calls, it defaults to `gemini-2.0-flash`.

## API Endpoints

### Chat Management

- **GET `/api/chats`** - Retrieve all chat conversations with metadata
- **GET `/api/chats/latest`** - Retrieve the 5 most recent chats
- **GET `/api/chat/<chat_id>`** - Retrieve a specific chat conversation
- **POST `/api/chat`** - Create a new chat conversation
- **PUT `/api/chat/<chat_id>`** - Update an existing chat conversation

### Text Generation

- **POST `/generate`** - Generate text using the Google Generative AI SDK
  ```json
  {
    "prompt": "Your message here"
  }
  ```

- **POST `/generate-http`** - Generate text using direct HTTP API
  ```json
  {
    "prompt": "Your message here",
    "model": "gemini-2.0-flash"
  }
  ```

### Frontend

- **GET `/`** - Serve the main application UI

## Chat History Storage

Chat conversations are automatically stored as JSON files in the `chat_history/` directory. Each file contains:

```json
{
  "id": "unique-chat-id",
  "title": "Chat title (auto-generated from first message)",
  "timestamp": "2024-11-18T10:30:00.000000",
  "messages": [
    {
      "role": "user",
      "content": "User message"
    },
    {
      "role": "ai",
      "content": "AI response"
    }
  ]
}
```

## Frontend Features

### User Interface

- **Sidebar**: Navigation with chat history and theme toggle
- **Chat Area**: Message display with rich formatting
- **Input Field**: Auto-expanding textarea for message composition
- **Empty State**: Welcoming message for new chats

### Markdown Support

AI responses support the following markdown formatting:

- **Headers**: `# H1`, `## H2`, `### H3`
- **Bold**: `**bold text**`
- **Italic**: `*italic text*`
- **Code**: `` `inline code` ``
- **Lists**: 
  - Unordered: `- item` or `* item`
  - Ordered: `1. item`, `2. item`
- **Code Blocks**: Triple backticks (rendered as `<pre>`)
- **Horizontal Rules**: `---`
- **Blockquotes**: `> quote`
- **Tables**: Standard markdown table syntax

### Theme Persistence

Dark mode preference is saved in browser's `localStorage` and persists across sessions.

## Usage

1. **Start a New Chat**: Click the "+ New Chat" button in the sidebar
2. **Send a Message**: Type in the message field and press Enter (or Shift+Enter for new lines)
3. **View History**: Select any chat from the sidebar to load it
4. **Toggle Theme**: Use the sun/moon icon toggle in the sidebar footer
5. **Auto-save**: Chats are automatically saved when you receive a response

## Development

### Running with Debug Mode

The application runs with Flask debug mode enabled by default:

```bash
python app.py
```

### Project Files Breakdown

- **app.py**: 
  - Flask application setup
  - Chat CRUD operations (Create, Read, Update)
  - Text generation endpoints
  - Chat history management

- **main.py**:
  - Google Generative AI SDK configuration
  - `generate_text()`: SDK-based text generation
  - `generate_text_http()`: Direct HTTP API calls

- **templates/index.html**:
  - Complete UI implementation
  - JavaScript for chat management and API calls
  - CSS for styling and responsiveness
  - Markdown to HTML conversion
  - Theme management

## Troubleshooting

### API Key Not Found

If you see "GOOGLE_API_KEY not found in environment variables":
- Ensure `.env` file exists in the project root with `GOOGLE_API_KEY=your_key`
- Or set the environment variable: `set GOOGLE_API_KEY=your_key` (Windows)

### Port Already in Use

If port 5000 is in use:
- Modify the port in `app.py`: `app.run(host="0.0.0.0", port=5001, debug=True)`

### Chat History Not Loading

- Check that the `chat_history/` directory exists and has proper permissions
- Verify JSON files in `chat_history/` are properly formatted

## Browser Compatibility

- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support
- Mobile browsers: Responsive design optimized for touch devices

## Future Enhancements

- User authentication and accounts
- Chat export functionality (PDF, JSON)
- Conversation search
- Message editing and deletion
- System prompt customization
- Multiple AI model selection
- Voice input/output

## License

This project is provided as-is for educational and personal use.

## Support

For issues or questions, refer to the code comments in `app.py` and `templates/index.html` for detailed implementation notes.
