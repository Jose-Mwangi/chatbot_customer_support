from chatbot import PortfolioChatbot
import time

# Test questions specific to Joseph's portfolio
TEST_QUESTIONS = [
    "What services does Joseph offer?",
    "What's your experience with AI/ML?",
    "How do I start a project with you?",
    "What technologies do you use?",
    "How can I contact Joseph?",
]

def quick_test():
    """Quick test with sample questions"""
    
    print("="*80)
    print(" "*20 + "JOSEPH MWANGI PORTFOLIO CHATBOT")
    print(" "*25 + "🆓 FREE Ollama Version")
    print(" "*28 + "QUICK TEST")
    print("="*80 + "\n")
    
    try:
        bot = PortfolioChatbot()
        
        print(f"Testing with {len(TEST_QUESTIONS)} questions...\n")
        
        for i, question in enumerate(TEST_QUESTIONS, 1):
            print(f"{'='*80}")
            print(f"Question {i}/{len(TEST_QUESTIONS)}")
            print(f"{'='*80}")
            print(f"\n❓ Q: {question}")
            
            start_time = time.time()
            response = bot.chat(question)
            response_time = time.time() - start_time
            
            print(f"\n✅ A: {response['answer']}")
            print(f"\n⏱️  Response time: {response_time:.2f}s")
            print(f"📚 Sources: {len(response['sources'])}")
            print(f"\n{'='*80}\n")
            
            time.sleep(0.5)
        
        print("\n✅ Quick test complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure:")
        print("1. Ollama is installed and running")
        print("2. You've run: ollama pull llama3.2")
        print("3. You've run: python ingest_docs.py")

if __name__ == "__main__":
    try:
        quick_test()
    except KeyboardInterrupt:
        print("\n\n👋 Test stopped by user")
