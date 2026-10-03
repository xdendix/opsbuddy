# app/ai_engine.py
import ollama


def stream_ai_response(messages):
    """
    Mengirim riwayat percakapan ke model Gemma lokal via Ollama
    dan menampilkan respon kata-per-kata (streaming).
    """
    stream = ollama.chat(model="gemma2:2b", messages=messages, stream=True)
    for chunk in stream:
        yield chunk["message"]["content"]
