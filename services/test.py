from langchain_deepseek import ChatDeepSeek
from langchain_groq import ChatGroq
import os
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage

def test_deepseek_api(api_key):
    try:
        # Initialize the DeepSeek chat model
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            #model="llama-3.1-405b-reasoning",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=api_key
            # other params...
        )
        
        # Test with a simple message
        response = llm.invoke([HumanMessage(content="What is the capital of France?")])
        
        print("API test successful!")
        print("Response:", response)
        return True
    except Exception as e:
        print("API test failed!")
        print("Error:", str(e))
        return False

if __name__ == "__main__":
    # Get API key from environment variable
    api_key = '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'
    print(api_key) 
    
    if not api_key:
        print("Error: GROQ_API_KEY environment variable not set")
    else:
        print("Testing DeepSeek API...")
        print(api_key)
        success = test_deepseek_api(api_key)
        
        if not success:
            print("\nPossible issues:")
            print("1. Your API key might be invalid")
            print("2. Your account might have insufficient balance")
            print("3. There might be network connectivity issues")
            print("4. The DeepSeek API might be temporarily unavailable")