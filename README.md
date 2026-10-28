# AI-Powered Web Research Assistant

An AI-powered web research assistant built with Python, LangChain, Groq, Tavily, and Streamlit. It helps users research topics by retrieving relevant web information and generating easy-to-understand answers with source links.

## 🚀 Features

- **AI-Powered Research:** Uses a Groq-hosted language model through LangChain.
- **Web Search Integration:** Retrieves relevant web results using the Tavily Search API.
- **Interactive UI:** Provides a clean chat interface built with Streamlit.
- **Human-in-the-Loop Approval:** Allows users to approve or cancel a research request before the agent executes it.
- **Source References:** Includes source titles and URLs in research responses.
- **Chat History:** Displays the conversation during the current session.
- **Suggested Queries:** Provides example topics to help users get started.

## 🛠️ Tech Stack

- **Programming Language:** Python
- **LLM Provider:** Groq
- **AI Agent Framework:** LangChain
- **Web Search API:** Tavily
- **Frontend:** Streamlit
- **Environment Management:** python-dotenv

## 📁 Project Structure

```text
WebResearchAgent/
├── app.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/WebResearchAgent.git
cd WebResearchAgent
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root directory:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Obtain API credentials from:

- Groq: https://console.groq.com/
- Tavily: https://tavily.com/

Keep your API keys private. Never upload the `.env` file to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

`http://localhost:8501`

## 🔄 How It Works

1. The user enters a research question in the Streamlit interface.
2. The application asks the user to approve or cancel the request.
3. After approval, the LangChain agent processes the question.
4. When needed, the agent calls the Tavily tool to retrieve relevant web results.
5. The Groq-hosted language model prepares a readable response from the available results.
6. The application displays the answer and source references in the chat interface.

## 💡 Example Queries

- What are the latest cybersecurity threats?
- Explain recent developments in artificial intelligence.
- What are the latest Python features?
- Research cloud security best practices.
- Explain recent developments in generative AI.

## 🔐 Security Notes

- Store API credentials in environment variables.
- Exclude `.env` and virtual environments from version control.
- Validate API errors and search results before relying on them.
- Review the source links to verify important information.

## 🎯 Learning Outcomes

This project demonstrates practical experience with:

- LLM integration and AI agent development
- LangChain tools and tool calling
- External API integration
- Web information retrieval
- Human-in-the-loop workflows
- Streamlit application development
- Python environment and dependency management

## ⚠️ Limitations

- Search quality depends on the available web results.
- The application requires valid API credentials and an internet connection.
- AI-generated responses can contain errors; verify important claims using the cited sources.
- The current chat history is maintained in the active Streamlit session.

## 👨‍💻 Author

**Siddhant Ghungarde**

GitHub: https://github.com/SiddhantGhungarde

## 📄 License

This project is available for learning and portfolio demonstration. Add a LICENSE file if you want to specify formal reuse and distribution terms.
