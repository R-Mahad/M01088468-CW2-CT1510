from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="YOUR_API_KEY_HERE")

# Initialize converstion history
messages = [
    {"role": "system", "content": "You are a helpful assistant."}
]

print("ChatGPT Console Chat (type 'quit' to exit)")
print("-" * 50)

while True:
    # Get user input
    user_input = input("You: ")

    # Exit condition
    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    # Add user message to history
    messages.append({"role": "user", "content": user_input})

    # Get AI response
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )

    # Extract response
    assistant_message = completion.choices[0].message.content

    # Add assistant respone to history
    messages.append({"role": "assistant", "content": assistant_message})

    print(f"AI: {assistant_message}\n")
