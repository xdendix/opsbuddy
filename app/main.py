# app/main.py
import os
import sentry_sdk
from app.ui import console, ACCENT_COLOR, print_header
from app.ai_engine import stream_ai_response
from app.prompts import SYSADMIN_TUTOR_PROMPT

# Inisialisasi Sentry untuk memantau latensi AI lokal
sentry_sdk.init(
    dsn="https://ad84b5eb7da94d2a0d8ce8d7e4d40952@o4512189504356352.ingest.us.sentry.io/4512189682745344",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    enable_logs=True,
)


def read_local_file(filepath):
    """
    Membaca isi file log lokal dengan aman.
    Dibatasi maksimal 500 baris terakhir agar AI tidak kehabisan memori.
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

    try:
        while True:
            user_input = console.input(
                f"\n[{ACCENT_COLOR}]Andre (Trainee) > [/{ACCENT_COLOR}] "
            )

            if user_input.lower() in ["exit", "quit"]:
                console.print(
                    f"[{ACCENT_COLOR}]Session terminated. Stay secure, stay local![/{ACCENT_COLOR}]"
                )
                break

            # Fitur Local File Analyzer (Membaca file log)
            if user_input.startswith("/analyze "):
                filepath = user_input.split(" ", 1)[1]
                console.print(
                    f"[bold yellow]🔍 OpsBuddy is reading local file: {filepath}...[/bold yellow]"
                )

                file_content = read_local_file(filepath)

                if file_content:
                    prompt_to_ai = f"Please analyze this error log and explain the root cause concisely:\n\n```text\n{file_content}\n```"
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

            # Membungkus proses Ollama dengan Sentry Tracing menggunakan start_span yang dimodifikasi
            with sentry_sdk.start_transaction(
                name="Gemma Local Generation"
            ) as transaction:
                with transaction.start_child(
                    op="ai.inference", name="Stream Response dari Ollama"
                ):
                    for chunk in stream_ai_response(messages):
                        console.print(chunk, end="")
                        full_reply += chunk
            print()
            console.print("-" * 50)
            messages.append({"role": "assistant", "content": full_reply})

            # Memaksa Sentry mengirim data latensi ke server secara real-time
            sentry_sdk.flush()

    # Menangani penutupan aplikasi via Ctrl+C secara bersih tanpa error panjang
    except KeyboardInterrupt:
        console.print(
            f"\n\n[{ACCENT_COLOR}]Program dihentikan paksa (Ctrl+C). Stay secure, stay local![/{ACCENT_COLOR}]"
        )
        sentry_sdk.flush()


if __name__ == "__main__":
    try:
        chat_session()
    except KeyboardInterrupt:
        pass
