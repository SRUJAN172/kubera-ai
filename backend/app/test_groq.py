import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Import the generate_explanation function from our service
try:
    from llm_service import generate_explanation
except ImportError:
    print("Error: Could not import llm_service. Make sure you are in the backend/app directory.")
    exit(1)

def main():
    api_key = os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        print("[ERROR] GROQ_API_KEY is not set in your .env file!")
        print("Please add GROQ_API_KEY=your_key_here to backend/app/.env")
        return

    print("[SUCCESS] GROQ_API_KEY found. Testing connection to Groq API...\n")
    
    prompt = "Explain why an emergency fund is important in 2 sentences."
    print(f"Prompt: {prompt}")
    print("-" * 40)
    
    try:
        response = generate_explanation(prompt)
        print("Groq Response:\n")
        print(response)
        print("\n" + "-" * 40)
        print("[SUCCESS] Groq test successful!")
    except Exception as e:
        print(f"\n[ERROR] Error calling Groq: {e}")

if __name__ == "__main__":
    main()
