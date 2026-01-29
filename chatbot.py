from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os
from dotenv import load_dotenv

load_dotenv()

class PortfolioChatbot:
    """AI-powered portfolio assistant for Joseph Mwangi - FREE Ollama Version"""
    
    def __init__(self, index_name="joseph-portfolio-chatbot"):
        """Initialize the chatbot with vector store and LLM"""
        
        print("="*70)
        print("JOSEPH MWANGI PORTFOLIO CHATBOT")
        print("🆓 Using FREE Ollama (No API costs!)")
        print("="*70)
        print("\n🚀 Initializing chatbot...\n")
        
        # Initialize embeddings (FREE - runs locally)
        self.embeddings = OllamaEmbeddings(
            model="nomic-embed-text"
        )
        
        # Connect to Pinecone vectorstore
        self.vectorstore = PineconeVectorStore(
            index_name=index_name,
            embedding=self.embeddings
        )
        print(f"✅ Connected to Pinecone index: {index_name}")
        
        # Initialize LLM (FREE - runs locally)
        self.llm = OllamaLLM(
            model="llama3.2",
            temperature=0.7,
        )
        print("✅ Initialized Llama 3.2 (FREE)")
        
        # Create retriever
        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 3}
        )
        
        # Custom prompt template
        self.prompt = PromptTemplate.from_template("""You are an AI assistant representing Joseph Mwangi, a multidisciplinary technology professional specializing in data science, analytics, cloud engineering, AI/ML, and backend development.

Use the following information from Joseph's portfolio and documentation to answer questions about his:
- Services and expertise
- Technical skills and experience
- Project approach and methodology
- Contact information and how to work with him

Be professional, helpful, and enthusiastic about Joseph's capabilities. If asked about something not in the documentation, politely say you don't have that specific information and suggest contacting Joseph directly.

Portfolio Information:
{context}

Question: {question}

Your Answer (as Joseph's AI assistant):""")
        
        # Create chain
        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        
        # Conversation history (simple list)
        self.conversation_history = []
        
        print("✅ Chatbot ready!")
        print("\n" + "="*70 + "\n")
    
    def chat(self, question):
        """
        Process a user question and return answer with sources
        
        Args:
            question (str): User's question
            
        Returns:
            dict: Contains 'answer' and 'sources'
        """
        try:
            # Get relevant documents
            docs = self.retriever.get_relevant_documents(question)
            
            # Get answer from chain
            answer = self.chain.invoke(question)
            
            # Add to conversation history
            self.conversation_history.append({
                "question": question,
                "answer": answer
            })
            
            return {
                "answer": answer,
                "sources": docs
            }
        except Exception as e:
            return {
                "answer": f"I apologize, but I encountered an error: {str(e)}. Please make sure Ollama is running and try again, or contact Joseph directly at josephkamenya289@gmail.com",
                "sources": []
            }
    
    def reset_memory(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("✅ Conversation memory cleared\n")

# CLI Testing Interface
if __name__ == "__main__":
    print("\n💬 CLI Mode - Commands: 'quit'/'exit' to stop, 'reset' to clear memory\n")
    
    try:
        bot = PortfolioChatbot()
        
        # Welcome message
        print("Hi! I'm Joseph's AI assistant (powered by FREE Ollama).")
        print("Ask me about his services, skills, experience, or how to work with him.\n")
        
        while True:
            user_input = input("🧑 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for your interest in Joseph's services!")
                print("📧 Contact: josephkamenya289@gmail.com")
                print("📱 Phone: +254 719 432 446 / +254 734 772 818\n")
                break
            
            if user_input.lower() == 'reset':
                bot.reset_memory()
                continue
            
            # Get response
            print("\n🤖 Assistant: ", end="", flush=True)
            response = bot.chat(user_input)
            
            # Display answer
            print(response['answer'])
            
            # Display sources
            if response['sources']:
                print(f"\n📚 [Based on {len(response['sources'])} source document(s)]")
            
            print()
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure Ollama is installed and running")
        print("2. Run: ollama pull llama3.2")
        print("3. Run 'python ingest_docs.py' first")
        print("4. Check your .env file has valid PINECONE_API_KEY\n")