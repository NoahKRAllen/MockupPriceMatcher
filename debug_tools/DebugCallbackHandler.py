from langchain.callbacks.base import BaseCallbackHandler

class DebugCallbackHandler(BaseCallbackHandler):
    def on_tool_start(self, serialized, input_str, **kwargs):
        print(f"\n🛠 Tool Start: {serialized['name']}")
        print(f"🔢 Input: {input_str}")

    def on_tool_end(self, output, **kwargs):
        print(f"✅ Tool Output: {output}\n")

    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"\n🧠 LLM Prompt: {prompts[0]}\n")

    def on_llm_end(self, response, **kwargs):
        print(f"📤 LLM Response: {response.generations[0][0].text.strip()}\n")
