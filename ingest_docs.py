from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv
import glob

# Load environment variables
load_dotenv()

def load_documents_from_directory(directory_path):
    """
    Manually load all .txt files from directory (Windows-compatible)
    """
    documents = []
    
    # Find all .txt files recursively
    txt_files = glob.glob(os.path.join(directory_path, "**/*.txt"), recursive=True)
    
    if not txt_files:
        print(f"⚠️  No .txt files found in {directory_path}")
        return documents
    
    print(f"Found {len(txt_files)} .txt file(s)")
    
    for file_path in txt_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Create LangChain Document object
            doc = Document(
                page_content=content,
                metadata={"source": file_path}
            )
            documents.append(doc)
            print(f"✅ Loaded: {os.path.basename(file_path)}")
            
        except Exception as e:
            print(f"❌ Error loading {file_path}: {str(e)}")
    
    return documents

def ingest_documents():
    """Load documents from docs/ folder and ingest into Pinecone"""
    
    print("="*70)
    print("JOSEPH MWANGI PORTFOLIO CHATBOT - DOCUMENT INGESTION")
    print("Using FREE Ollama (No API costs!)")
    print("="*70)
    
    print("\n📂 Loading documents from docs/ folder...")
    
    # Load documents manually (Windows-compatible)
    documents = load_documents_from_directory('docs')
    
    if len(documents) == 0:
        print("\n⚠️  No documents found in docs/ folder!")
        print("Please add .txt files to the docs/ folder and try again.")
        return
    
    print(f"\n✅ Successfully loaded {len(documents)} documents")
    
    # Split documents into chunks
    print("\n✂️  Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Created {len(chunks)} chunks")
    
    # Initialize Pinecone
    print("\n🔌 Initializing Pinecone...")
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = "joseph-portfolio-chatbot"
    
    # Create index if it doesn't exist
    existing_indexes = [index.name for index in pc.list_indexes()]
    
    if index_name not in existing_indexes:
        print(f"🆕 Creating new index: {index_name}")
        pc.create_index(
            name=index_name,
            dimension=768,  # Ollama embedding dimension (nomic-embed-text)
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
        print("✅ Index created successfully")
    else:
        print(f"✅ Index '{index_name}' already exists")
    
    # Create embeddings using FREE Ollama
    print("\n🧠 Creating embeddings using Ollama (FREE - runs locally)...")
    print("This may take a few minutes...")
    
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"  # Free embedding model
    )
    
    vectorstore = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=index_name
    )
    
    print("\n" + "="*70)
    print("✅ SUCCESS! Documents ingested successfully!")
    print("="*70)
    print(f"📊 Total chunks stored: {len(chunks)}")
    print(f"🗂️  Index name: {index_name}")
    print(f"📁 Documents processed:")
    for doc in documents:
        print(f"   • {os.path.basename(doc.metadata['source'])}")
    print("\n🚀 You can now run: python chatbot.py or streamlit run app.py")
    print("="*70 + "\n")
    
    return vectorstore

if __name__ == "__main__":
    try:
        print("\n⚠️  IMPORTANT: Make sure Ollama is running!")
        print("If you haven't installed Ollama, download it from: https://ollama.ai")
        print("Then run: ollama pull nomic-embed-text")
        print("="*70 + "\n")
        
        ingest_documents()
    except Exception as e:
        print("\n" + "="*70)
        print("❌ ERROR DURING INGESTION")
        print("="*70)
        print(f"Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure Ollama is installed and running")
        print("2. Run: ollama pull nomic-embed-text")
        print("3. Check that your .env file has valid PINECONE_API_KEY")
        print("4. Ensure you have .txt files in the docs/ folder")
        print("5. Verify your internet connection for Pinecone")
        print("="*70 + "\n")
        raise