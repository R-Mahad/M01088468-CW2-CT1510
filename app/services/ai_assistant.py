from openai import OpenAI


class AIAssistant:
    """
    Handles AI chat logic for different domains.
    Keeps prompts in one place and provides a simple 'ask()' method.
    """

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.__client = OpenAI(api_key=api_key)
        self.__model = model
        self.__domain = "Cybersecurity"

    def set_domain(self, domain: str) -> None:
        """Set the current domain (Cybersecurity / Data Science / IT Operations)."""
        allowed = ["Cybersecurity", "Data Science", "IT Operations"]
        if domain not in allowed:
            raise ValueError(f"Invalid domain: {domain}. Must be one of {allowed}")
        self.__domain = domain

    def get_domain(self) -> str:
        return self.__domain

    def get_system_prompt(self) -> str:
        """Return the system prompt based on the currently selected domain."""
        if self.__domain == "Cybersecurity":
            return (
                "You are a cybersecurity expert assistant.\n"
                "Analyze incidents, threats, and provide technical guidance."
            )

        if self.__domain == "Data Science":
            return (
                "You are a data science expert assistant.\n"
                "Help with analysis, visualization, and statistical insights."
            )

        # IT Operations
        return (
            "You are an IT operations expert assistant.\n"
            "Help troubleshoot issues, optimize systems, and manage tickets."
        )

    def ask(self, chat_history: list[dict], user_prompt: str) -> str:
        """
        Send a message to the ChatGPT API using:
        - a domain-specific system prompt
        - the existing chat history
        - the new user prompt

        chat_history should be a list of dicts like:
        [{"role":"user","content":"..."}, {"role":"assistant","content":"..."}]
        """
        messages = [{"role": "system", "content": self.get_system_prompt()}]

        # Add existing conversation messages
        for m in chat_history:
            messages.append({"role": m["role"], "content": m["content"]})

        # Add the new user prompt
        messages.append({"role": "user", "content": user_prompt})

        completion = self.__client.chat.completions.create(
            model=self.__model,
            messages=messages,
        )

        return completion.choices[0].message.content
