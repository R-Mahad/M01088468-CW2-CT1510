import streamlit as st
from openai import OpenAI

# Initialize OpenAI clinet
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🛡 Cybersecurity AI Assistant")

# Initialise session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a cybersecurity expert assistant.\n"
                "- Analyse incidents and threats\n"
                "- Provide technical guidance\n"
                "- Explain attack vectors and mitigations\n"
                "- Use standard terminology (MITRE ATT&CK, CVE)\n"
                "- Prioritise clear, actionable recommendations\n"
                "Tone: professional and technical."
            ),
        }
    ]

# Show all previous messages except the system one
for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
prompt = st.chat_input("Ask about cybersecurity...")

if prompt:
    # Show and save the user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # call OpenAI API
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=st.session_state.messages,
    )

    reply = completion.choices[0].message.content

    # display assistant response
    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
