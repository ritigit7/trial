# Chat with Ollama - Local AI Chat Application

![Chat with Ollama Logo](https://via.placeholder.com/150x50?text=Chat+with+Ollama) *(Replace with your actual logo image)*

## 📝 Description

Chat with Ollama is a Streamlit-based application that allows you to interact with various local AI models through Ollama. The application supports multiple data sources including direct chat, Wikipedia queries, SQL databases, PDF/Word documents, and website content using Retrieval-Augmented Generation (RAG) techniques.

## ✨ Features

- **Multiple Model Support**: Choose from various Ollama models (Qwen, Llama 3, Mistral, etc.)
- **Multiple Data Sources**:
  - Direct chat with the AI model
  - Wikipedia knowledge queries
  - SQL database interaction
  - PDF and Word document processing
  - Website content analysis
- **RAG Implementation**: For document and website content
- **Real-time Streaming**: Responses streamed as they're generated
- **Conversation Memory**: Maintains chat history
- **Logging**: Detailed logging of all interactions

## 🛠️ Installation

1. **Prerequisites**:
   - Python 3.8+
   - Ollama installed and running locally ([Installation Guide](https://ollama.ai/))
   - Required models pulled (e.g., `ollama pull qwen2.5:1.5b`)

2. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/chat-with-ollama.git
   cd chat-with-ollama
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

1. **Run the application**:
   ```bash
   streamlit run app.py
   ```

2. **Configure the app**:
   - Select your preferred Ollama model
   - Choose a data source type
   - Provide necessary inputs (file paths, URLs, etc.)

3. **Start chatting**!

## 📂 Project Structure

```
chat-with-ollama/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── vector_store/          # Directory for vector stores (auto-created)
├── logs/                  # Conversation logs (auto-created)
├── README.md              # This file
└── assets/                # For images/logo (optional)
```

## 🌟 Available Models

The application supports these Ollama models (and more can be added):

- `qwen2.5:1.5b`
- `nomic-embed-text`
- `gemma3:1b`
- `codellama`
- *(Add your own favorites!)*

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📧 Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/chat-with-ollama](https://github.com/yourusername/chat-with-ollama)

---

*(Remember to replace placeholder information with your actual details and add a proper logo image)*
