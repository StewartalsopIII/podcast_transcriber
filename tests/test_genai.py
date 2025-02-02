import os
from dotenv import load_dotenv
import google.generativeai as genai

def test_genai_connection():
    """Test basic connection to Google's Generative AI"""
    try:
        # Load the .env file
        load_dotenv()  # Add this line
        
        # Configure the library with your API key
        API_KEY = os.getenv('GOOGLE_API_KEY')
        if not API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in .env file")
            
        genai.configure(api_key=API_KEY)
        
        # Initialize the model (using Gemini-Pro)
        model = genai.GenerativeModel('gemini-pro')
        
        # Simple test prompt
        response = model.generate_content("Reply with 'Test successful' if you can read this.")
        
        # Print the response
        print("\nAPI Test Results:")
        print("----------------")
        print(f"Response: {response.text}")
        
        return True
    except Exception as e:
        print(f"\nError: {str(e)}")
        return False

if __name__ == "__main__":
    print("\nTesting Google Generative AI Connection...")
    success = test_genai_connection()
    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed!")