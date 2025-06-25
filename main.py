import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("API")

# Global list to store the conversation history
messages = []

def configure_gemini():
    if key is None:
        raise ValueError("API key not found. Please set the 'API' environment variable.")
    genai.configure(api_key=key)

def gemini_flash_completion(message: str) -> None:
    global messages
    
    # Append the user's message to the history
    messages.append({"role": "user", "parts": [message]})

    # Initialize the model with the correct model ID for Gemini Flash
    # You can also use 'gemini-1.5-flash-latest' or other preview models as they become available.
    model = genai.GenerativeModel('gemini-1.5-flash-latest') 

    try:
        # Start a chat session, passing the entire conversation history.
        # The history needs to alternate between 'user' and 'model' roles.
        chat = model.start_chat(history=messages) 
        
        # Send the latest user message. The model will use the 'history'
        # provided during chat initialization to understand context.
        response = chat.send_message(message)
        
        # Extract the model's reply
        reply_content = response.text
        
        # Append the model's reply to the history
        messages.append({"role": "model", "parts": [reply_content]})
        
        print(f'Alfraid: {reply_content}\n')
        
    except Exception as e:
        print(f"An error occurred: {e}")
        # If an error occurs, you might want to remove the last user message
        # from history to avoid sending incomplete context in the next turn.
        if messages and messages[-1]["role"] == "user":
            messages.pop()

if __name__ == "__main__":
    configure_gemini()
    print("Alfraid: Hello, this is Alfred. How can I help you? (Type 'exit' to quit)\n")

    while True: # This is the loop that keeps the conversation going
        user_question = input("User: ")
        
        if user_question.lower() == 'exit':
            print("Alfraid: Goodbye! It was a pleasure assisting you.")
            break # Exit the loop if the user types 'exit'
        
        gemini_flash_completion(user_question)