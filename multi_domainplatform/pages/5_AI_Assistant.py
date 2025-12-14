import streamlit as st
from openai import OpenAI

# Use the API key stored in .streamlit/secrets.toml
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Multi-Domain AI Assistant")

st.write(
    "Ask questions related to cybersecurity, data science, or IT operations. "
    "The assistant will change behaviour based on the selected domain."
)

# --------------------- Domain selection ---------------------
domain = st.selectbox(
    "Choose a domain",
    ["Cybersecurity", "Data Science", "IT Operations"],
)

# Map domain -> system prompt text (from the lab document)
if domain == "Cybersecurity":
    system_prompt = """
You are a cybersecurity expert assistant.
Analyze incidents, threats, and provide technical guidance.
"""
elif domain == "Data Science":
    system_prompt = """
You are a data science expert assistant.
Help with analysis, visualization, and statistical insights.
"""
else:  # IT Operations
    system_prompt = """
You are an IT operations expert assistant.
Help troubleshoot issues, optimize systems, and manage tickets.
"""

# --------------------- Session state setup ---------------------
# We keep a separate chat history for this page.
if "ai_domain" not in st.session_state:
    st.session_state.ai_domain = domain

if "ai_messages" not in st.session_state:
    st.session_state.ai_messages = []

# If the user changes domain, reset the conversation
if st.session_state.ai_domain != domain:
    st.session_state.ai_domain = domain
    st.session_state.ai_messages = []

# Always start the conversation with a system message
# (not shown to the user, but sent to the API).
base_messages = [
    {"role": "system", "content": system_prompt.strip()}
]

# --------------------- Sidebar controls ---------------------
with st.sidebar:
    st.subheader("Chat settings")
    st.write(f"**Current domain:** {domain}")
    msg_count = len(st.session_state.ai_messages)
    st.metric("Messages", msg_count)

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.ai_messages = []
        st.success("Conversation cleared.")
        st.experimental_rerun()

# --------------------- Show chat history ---------------------
for message in st.session_state.ai_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------- Input box ---------------------
prompt = st.chat_input(f"Ask a question about {domain.lower()}...")

if prompt:
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message into history
    st.session_state.ai_messages.append(
        {"role": "user", "content": prompt}
    )

    # Build full message list: system prompt + chat history
    messages = base_messages + st.session_state.ai_messages

    # Call the ChatGPT API (non-streaming, like in the lab example)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )

    reply = completion.choices[0].message.content

    # Show assistant reply
    with st.chat_message("assistant"):
        st.markdown(reply)

    # Save assistant reply into history
    st.session_state.ai_messages.append(
        {"role": "assistant", "content": reply}
    )
