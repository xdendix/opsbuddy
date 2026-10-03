# app/main.py
import os
import sentry_sdk
from app.ui import console, ACCENT_COLOR, print_header
from app.ai_engine import stream_ai_response
from app.prompts import SYSADMIN_TUTOR_PROMPT

# SENTRY UPGRADE: Inisialisasi Sentry untuk memantau performa model lokal
# (Daftar akun Sentry gratis, lalu masukkan DSN lu di sini)
sentry_sdk.init(
    dsn="MASUKKAN_DSN_SENTRY_LU_DISINI",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


def read_local_file(filepath):
    """
    Agentic Feature: Reads a local log file securely.
    Limits to the last 500 lines to prevent Out-Of-Memory issues on local LLMs.
    """
    try:
        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                lines = file.readlines()[-500:]
                return "".join(lines)
        return None
    except Exception as e:
        return f"Error reading file: {str(e)}"


def chat_session():
    print_header()
    messages = [{"role": "system", "content": SYSADMIN_TUTOR_PROMPT}]

    while True:
        user_input = console.input(
            f"\n[{ACCENT_COLOR}]Andre (Trainee) > [/{ACCENT_COLOR}] "
        )

        if user_input.lower() in ["exit", "quit"]:
            console.print(
                f"[{ACCENT_COLOR}]Session terminated. Stay secure, stay local![/{ACCENT_COLOR}]"
            )
            break

        # AGENT UPGRADE: Command khusus untuk membaca file lokal
        if user_input.startswith("/analyze "):
            filepath = user_input.split(" ", 1)[1]
            console.print(
                f"[bold yellow]🔍 OpsBuddy is reading local file: {filepath}...[/bold yellow]"
            )

            file_content = read_local_file(filepath)

            if file_content:
                prompt_to_ai = f"Please analyze this error log and explain the root cause to Andre in simple terms:\n\n```text\n{file_content}\n```"
                messages.append({"role": "user", "content": prompt_to_ai})
            else:
                console.print(
                    f"[bold red]❌ File not found or unreadable. Check the path.[/bold red]"
                )
                continue
        else:
            messages.append({"role": "user", "content": user_input})

        console.print("\n[bold cyan]OpsBuddy:[/bold cyan]")

        full_reply = ""

        # SENTRY TRACING: Membungkus eksekusi Ollama untuk dikirim log performanya ke Sentry
        with sentry_sdk.start_span(
            op="ai.inference", description="Gemma 2B Local Generation"
        ):
            for chunk in stream_ai_response(messages):
                console.print(chunk, end="")
                full_reply += chunk

        print()
        console.print("-" * 50)
        messages.append({"role": "assistant", "content": full_reply})


if __name__ == "__main__":
    chat_session()
