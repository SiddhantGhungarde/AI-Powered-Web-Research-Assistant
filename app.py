
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.tools import tool
from tavily import TavilyClient

load_dotenv()

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="WebResearch AI",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0b1020 0%, #10172a 55%, #111827 100%);
    color: #f1f5f9;
}

[data-testid="stSidebar"] {
    background: #0a0f1c;
    border-right: 1px solid #263148;
}

.hero {
    padding: 28px 30px;
    border: 1px solid #293753;
    border-radius: 22px;
    background: linear-gradient(120deg, #172442, #111827 75%);
    margin-bottom: 26px;
}

.hero h1 {
    font-size: 36px;
    font-weight: 800;
    margin: 5px 0 10px 0;
    color: #f8fafc;
}

.hero p {
    color: #aab8d0;
    font-size: 15px;
    margin-bottom: 0;
    line-height: 1.7;
}

.eyebrow {
    color: #8bafff;
    font-weight: 700;
    letter-spacing: 2px;
    font-size: 11px;
}

.status-card {
    padding: 15px;
    background: #141d30;
    border: 1px solid #293753;
    border-radius: 14px;
    margin: 10px 0;
}

.status-title {
    color: #dce6f7;
    font-weight: 600;
    font-size: 14px;
}

.status-subtitle {
    color: #8c9bb5;
    font-size: 12px;
    margin-top: 5px;
}

.section-label {
    color: #91a4c4;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 700;
    margin: 20px 0 10px;
}

div[data-testid="stChatMessage"] {
    border: 1px solid #27344c;
    border-radius: 16px;
    padding: 12px;
    background: rgba(20, 29, 48, 0.72);
    margin-bottom: 12px;
}

.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    min-height: 42px;
}

.stChatInput textarea {
    border-radius: 14px !important;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("## 🔎 WebResearch AI")
    st.caption("Your personal web research assistant")

    st.markdown("---")

    st.markdown("### ⚡ Capabilities")

    st.markdown("""
    <div class="status-card">
        <div class="status-title">🌐 Web Research</div>
        <div class="status-subtitle">Search the web using Tavily</div>
    </div>
    <div class="status-card">
        <div class="status-title">🧠 AI Intelligence</div>
        <div class="status-subtitle">Powered by Groq and LangChain</div>
    </div>
    <div class="status-card">
        <div class="status-title">🛡️ Human Approval</div>
        <div class="status-subtitle">Approve research before execution</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 💡 Try asking")

    examples = [
        "Latest cybersecurity threats",
        "Recent developments in AI",
        "Latest Python updates",
        "Cloud security best practices"
    ]

    for example in examples:
        if st.button(example, key=f"example_{example}", use_container_width=True):
            st.session_state.pending_query = example
            st.rerun()

    st.markdown("---")

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_query = None
        st.rerun()

    st.caption("Built with Python · Streamlit · LangChain")


# ---------------- INITIALIZE STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None


# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <div class="eyebrow">INTELLIGENT WEB RESEARCH</div>
    <h1>Research anything. 🔍</h1>
    <p>
        Explore the latest information from the web with AI-powered research.
        Ask a question, approve the search, and get a clear answer.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="status-card">
        <div class="status-title">🌐 Live web search</div>
        <div class="status-subtitle">Discover relevant web sources</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="status-card">
        <div class="status-title">🤖 AI-powered answers</div>
        <div class="status-subtitle">Understand research results</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="status-card">
        <div class="status-title">🛡️ You stay in control</div>
        <div class="status-subtitle">Approve before researching</div>
    </div>
    """, unsafe_allow_html=True)


# ---------------- TAVILY TOOL ----------------

@st.cache_resource
def get_tavily_client():
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY is missing from your .env file.")
    return TavilyClient(api_key=api_key)


@tool
def web_research(query: str) -> str:
    """Search the web for relevant and recent information about a topic."""
    response = get_tavily_client().search(
        query=f"latest information on {query}",
        search_depth="basic",
        max_results=3
    )

    results = response.get("results", [])

    if not results:
        return f"No web results found for: {query}"

    research_list = []

    for item in results:
        title = item.get("title", "No title")
        url = item.get("url", "")
        content = item.get("content", "")

        research_list.append(
            f"Title: {title}\n"
            f"URL: {url}\n"
            f"Content: {content}"
        )

    return f"Web research results for {query}:\n\n" + "\n\n".join(
        research_list
    )


# ---------------- AGENT ----------------

@st.cache_resource
def get_agent():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing from your .env file.")

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        api_key=api_key
    )

    return create_agent(
        llm,
        tools=[web_research],
        system_prompt="""
        You are WebResearch AI, a helpful web information assistant.

        When the user asks for current information, use the web_research tool.
        Summarize the findings clearly and accurately.
        Include the source titles and their URLs in your answer.
        Distinguish sourced information from your own explanation.
        If the search results are insufficient, say so honestly.
        Never invent sources or URLs.
        """
    )


# ---------------- CHAT HISTORY ----------------

st.markdown('<div class="section-label">YOUR RESEARCH SESSION</div>',
            unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------- CHAT INPUT ----------------

prompt = st.chat_input("Ask about cybersecurity, AI, technology, or anything...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    st.session_state.pending_query = prompt
    st.rerun()


# ---------------- HUMAN APPROVAL ----------------

if st.session_state.pending_query:
    query = st.session_state.pending_query

    st.markdown("### 🛡️ Research approval")

    st.info(
        f"Your agent is ready to process this request:\n\n**{query}**\n\n"
        "Approve to let the agent run. If it needs web research, "
        "it can call Tavily to retrieve up to 3 results."
    )

    approve_col, cancel_col = st.columns([1, 1])

    with approve_col:
        approved = st.button(
            "✅ Approve & Research",
            type="primary",
            use_container_width=True
        )

    with cancel_col:
        cancelled = st.button(
            "✖ Cancel",
            use_container_width=True
        )

    if cancelled:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Research cancelled. No agent request was executed."
        })
        st.session_state.pending_query = None
        st.rerun()

    if approved:
        st.session_state.pending_query = None

        try:
            with st.spinner("🔎 Researching and preparing your answer..."):
                agent = get_agent()

                result = agent.invoke({
                    "messages": [
                        {"role": "user", "content": query}
                    ]
                })

                answer = result["messages"][-1].content

                if not isinstance(answer, str):
                    answer = str(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant",
                "content": (
                    "Something went wrong while researching. "
                    "Check your API keys, network connection, and terminal "
                    f"for details.\n\nError: `{e}`"
                )
            })

        st.rerun()


# ---------------- EMPTY STATE ----------------

if not st.session_state.messages and not st.session_state.pending_query:
    st.markdown("### ✨ Start exploring")

    st.write("Choose a topic or type your own question in the chat box.")

    demo1, demo2 = st.columns(2)

    with demo1:
        st.markdown("""
        <div class="status-card">
            <div class="status-title">🔐 Cybersecurity</div>
            <div class="status-subtitle">
                Threat intelligence, vulnerabilities, and security trends
            </div>
        </div>
        """, unsafe_allow_html=True)

    with demo2:
        st.markdown("""
        <div class="status-card">
            <div class="status-title">🧠 Artificial Intelligence</div>
            <div class="status-subtitle">
                AI news, LLMs, agents, and emerging technologies
            </div>
        </div>
        """, unsafe_allow_html=True)
