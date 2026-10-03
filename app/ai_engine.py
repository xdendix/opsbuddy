# app/ai_engine.py
import ollama


def stream_ai_response(messages):
    """
    Sends the conversation history to the local Gemma model via Ollama
    and yields the response chunk by chunk (streaming).
    """
    stream = ollama.chat(model="gemma2:2b", messages=messages, stream=True)
    for chunk in stream:
        yield chunk["message"]["content"]
