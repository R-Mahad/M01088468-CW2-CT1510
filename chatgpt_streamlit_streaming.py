import streamlit as st
from openai import OpenAI

# Create OpenAI client from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Basic page config
st.set_page_config(
    page_title="ChatGPT Assistant",
    page_icon="💬",
    layout="wide",
)

st.title("💬 ChatGPT - OpenAI API")
st.caption("Streaming demo using GPT-4o")

# Persistent chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----- Sidebar controls -----
with st.sidebar:
    st.subheader("Chat Controls")

    # Number of non-system messages
    message_count = len(
        [m for m in st.session_state.messages if m["role"] != "system"]
    )
    st.metric("Messages", message_count)

    # Clear chat
    if st.button("🗑 Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # Choose model
    model = st.selectbox(
        "Model",
        ["gpt-4o", "gpt-4o-mini"],
        index=0,
    )

    # Temperature slider
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=1.0,
        step=0.1,
        help="Higher = more creative / random answers.",
    )

# ----- Display existing messages -----
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----- Get new user input -----
prompt = st.chat_input("Say something...")

if prompt:
    # Show + store user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # Call ChatGPT with streaming enabled
    completion = client.chat.completions.create(
        model=model,
        messages=st.session_state.messages,
        temperature=temperature,
        stream=True,  # important for streaming
    )

    # Stream the response chunk by chunk
    full_reply = ""

    with st.chat_message("assistant"):
        container = st.empty()  # this will be updated repeatedly

        for chunk in completion:
            delta = chunk.choices[0].delta
            if delta.content:
                full_reply += delta.content
                container.markdown(full_reply)

    # Store final reply in history
    st.session_state.messages.append(
        {"role": "assistant", 
         "content": full_reply}
    )
