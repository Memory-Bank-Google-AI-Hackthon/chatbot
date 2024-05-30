import google.generativeai as genai


class ChatBot:
    def __init__(self, api_key):
        self.genai = genai
        self.genai.configure(api_key=api_key)
        self.model = self.genai.GenerativeModel("gemini-1.5-flash-latest")
        self.conversation = None
        self.init_conversation_history = []
        self.preload_conversation()

    def generation_config(self, temperature):
        return genai.types.GenerationConfig(temperature=temperature)

    def clear_conversation(self):
        self.conversation = self.model.start_chat(history=[])

    @property
    def history(self):
        conversation_history = [
            {"role": message.role, "text": message.parts[0].text}
            for message in self.conversation.history
        ]
        return conversation_history

    def start_conversation(self):
        self.conversation = self.model.start_chat(
            history=self.init_conversation_history
        )

    def construct_message(self, text, role="user"):
        return {"role": role, "parts": [text]}

    def preload_conversation(self, conversation_history=None):
        if isinstance(conversation_history, list):
            self.init_conversation_history = conversation_history
        else:
            self.init_conversation_history = [self.construct_message("使用繁體中文")]

    def send_message(self, message, temperature=0.5, stream=False):
        if temperature < 0 or temperature > 1:
            raise ValueError("temperature必須介於0~1之間")
        if not message:
            raise ValueError("訊息不得為空")

        try:
            response = self.conversation.send_message(
                content=message,
                generation_config=self.generation_config(temperature),
                stream=stream,
            )
            return response

        except Exception as e:
            print(f"對話機器人發生問題: {e}")

    def summarize_responses(self, responses):
        summary_prompt = "請總結以下回應：\n" + "\n\n".join(responses)
        summary_response = self.send_message(
            summary_prompt, temperature=0.3, stream=True
        )
        summary_text = []
        for chunk in summary_response:
            summary_text.append(chunk.text)
        return "".join(summary_text)
