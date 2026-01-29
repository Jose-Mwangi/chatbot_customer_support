import streamlit as st
from chatbot import PortfolioChatbot
import time

# Page configuration
st.set_page_config(
    page_title="Joseph Mwangi - AI Portfolio Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        max-width: 1400px;
        margin: 0 auto;
    }
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>💼 Joseph Mwangi - Portfolio Assistant</h1>
    <p>🆓 Powered by FREE Ollama (No API costs!)</p>
    <p>Ask me about Joseph's services, skills, experience, and how to work with him!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("👨‍💻 Joseph Mwangi")
    st.markdown("""
    **Data Scientist | Cloud Engineer | AI/ML Specialist | Backend Developer**
    
    Transforming complex data into actionable insights and building intelligent, scalable systems.
    """)
    
    st.divider()
    
    st.header("📞 Contact")
    st.markdown("""
    📧 **Email:**  
    josephkamenya289@gmail.com
    
    📱 **Phone:**  
    +254 719 432 446  
    +254 734 772 818
    
    🌐 **Portfolio:**  
    [portfolio-jose-mwas.vercel.app](https://portfolio-jose-mwas.vercel.app/)
    """)
    
    st.divider()
    
    st.header("🎯 Quick Questions")
    quick_questions = [
        "What services do you offer?",
        "What's your experience with AI/ML?",
        "Can you help with cloud migration?",
        "How do I start a project with you?",
        "What technologies do you use?"
    ]
    
    for q in quick_questions:
        if st.button(q, key=f"quick_{q}"):
            st.session_state.quick_question = q
    
    st.divider()
    
    if st.button("🔄 New Conversation", type="primary"):
        st.session_state.messages = []
        if 'chatbot' in st.session_state:
            st.session_state.chatbot.reset_memory()
        st.rerun()
    
    st.divider()
    
    st.header("⚙️ Settings")
    show_sources = st.checkbox("Show source documents", value=True)
    
    st.divider()
    st.info("🆓 This chatbot runs 100% FREE using Ollama locally. No API costs!")

# Initialize chatbot
@st.cache_resource
def load_chatbot():
    """Load chatbot once and cache it"""
    return PortfolioChatbot()

try:
    if 'chatbot' not in st.session_state:
        with st.spinner("🔧 Loading AI assistant..."):
            st.session_state.chatbot = load_chatbot()
        st.success("✅ AI assistant ready! (FREE Ollama)", icon="🤖")
        time.sleep(1)
        st.rerun()
except Exception as e:
    st.error(f"❌ Error loading chatbot: {str(e)}")
    st.warning("""
    **Troubleshooting Steps:**
    1. Make sure Ollama is installed: https://ollama.ai
    2. Run: `ollama pull llama3.2` and `ollama pull nomic-embed-text`
    3. Ensure you've run `python ingest_docs.py` first
    4. Check your `.env` file has valid `PINECONE_API_KEY`
    5. Make sure Ollama is running in the background
    """)
    st.stop()

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "👋 Hello! I'm Joseph's AI assistant (powered by FREE Ollama). I can help you learn about his services, technical expertise, project experience, and how to work with him. What would you like to know?",
        "sources": [],
        "timestamp": time.time()
    })

# Handle quick questions
if 'quick_question' in st.session_state:
    prompt = st.session_state.quick_question
    del st.session_state.quick_question
    
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": time.time()
    })
    
    with st.spinner("🤔 Thinking..."):
        response = st.session_state.chatbot.chat(prompt)
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": response["answer"],
        "sources": response["sources"],
        "timestamp": time.time()
    })
    
    st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        if message["role"] == "assistant" and "sources" in message and show_sources:
            if message["sources"]:
                with st.expander(f"📚 View {len(message['sources'])} source document(s)"):
                    for i, doc in enumerate(message["sources"], 1):
                        st.markdown(f"**Source {i}:**")
                        st.text_area(
                            f"source_{i}",
                            doc.page_content,
                            height=120,
                            key=f"source_{message['timestamp']}_{i}",
                            label_visibility="collapsed"
                        )

# Chat input
if prompt := st.chat_input("💬 Ask me anything about Joseph's services and expertise..."):
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": time.time()
    })
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            response = st.session_state.chatbot.chat(prompt)
        
        st.markdown(response["answer"])
        
        if show_sources and response["sources"]:
            with st.expander(f"📚 View {len(response['sources'])} source document(s)"):
                for i, doc in enumerate(response["sources"], 1):
                    st.markdown(f"**Source {i}:**")
                    st.text_area(
                        f"source_{i}",
                        doc.page_content,
                        height=120,
                        key=f"source_{time.time()}_{i}",
                        label_visibility="collapsed"
                    )
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": response["answer"],
        "sources": response["sources"],
        "timestamp": time.time()
    })

# Footer
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**📧 Email:**")
    st.markdown("josephkamenya289@gmail.com")

with col2:
    st.markdown("**📱 Phone:**")
    st.markdown("+254 719 432 446")

with col3:
    st.markdown("**🌐 Portfolio:**")
    st.markdown("[Visit Website](https://portfolio-jose-mwas.vercel.app/)")

st.caption("🤖 Powered by LangChain and FREE Ollama (Llama 3.2) | 🔒 Runs 100% Locally")