from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY not found. "
        "Make sure you created a .env file with OPENAI_API_KEY=..."
    )

client = OpenAI(api_key=api_key)

messages = [
    {"role": "system", "content": "You are a helpful assistant."}
]

print("Secure ChatGPT Console Chat (type 'quit' to exit)")
print("-" * 50)

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    messages.append({"role": "user", "content": user_input})

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )

    assistant_message = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_message})

    print(f"AI: {assistant_message}\n")
