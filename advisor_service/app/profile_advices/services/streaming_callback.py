from langchain.callbacks.base import BaseCallbackHandler

class StreamTokensHandler(BaseCallbackHandler):
    def __init__(self):
        self.tokens = []

    def on_llm_new_token(self, token: str, **kwargs):
        self.tokens.append(token)

    def get_tokens(self):
        return self.tokens
