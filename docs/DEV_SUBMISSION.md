title: "OpsBuddy: Mentoring an IT Student with a Secure, Local AI Agent 🐧"
published: false
tags: devchallenge, python, ai, opensource, sentry

The Problem: Learning Ops Without Breaking Production

Meet Andre, a good friend of mine and a passionate IT student. He understands the theoretical side of networking and operating systems, but when it comes to navigating a Linux terminal or diagnosing real server logs, he freezes up.

I wanted to mentor him and let him learn by doing, but giving him SSH access to my production servers was completely out of the question. One wrong command, and my side projects could vanish.

Furthermore, Andre had a dangerous habit: whenever he encountered a confusing log file during his local practice, his first instinct was to copy and paste the entire block into a cloud-based AI to ask, "What does this error mean?" In the real Ops world, doing this with production logs—which often contain API tokens, database connection strings, and sensitive user data (PII)—is a massive security violation.

I needed to build him a safe sandbox where he could practice CLI commands and analyze real logs without compromising data privacy.

What I Built: OpsBuddy

I built OpsBuddy, a fully local, CLI-based AI agent designed specifically for Andre. It acts as his personal, patient Senior SysAdmin mentor.

Under the hood, OpsBuddy runs on Python using the Rich library for a clean, distraction-free terminal UI. The core intelligence is powered by Gemma 2B, a lightweight open-weight model running 100% locally on his machine via Ollama.

OpsBuddy provides two main features:

Interactive Mentorship: It answers his questions about Linux concepts and commands directly in the terminal.

Secure Agentic Log Analysis (/analyze): Andre can use the custom command /analyze /path/to/logfile.log. Python securely reads the local file, passes the last 500 lines to the local Gemma model, and explains the root cause. Not a single byte of data leaves his laptop.

Why Open Innovation Matters Here

For this project, using open-source AI is not just a preference; it is a strict operational requirement.

I am using this tool to instill a security-first mindset in Andre from day one. By using an open-weight model like Gemma, I can guarantee absolute data privacy. Andre can dissect real, messy server logs with embedded credentials without violating any Non-Disclosure Agreements (NDAs) or leaking sensitive information to third-party cloud APIs. Open innovation proves that we don't have to trade security for the convenience of AI.

Tracking AI Performance with Sentry

Running an LLM locally on a CPU can be resource-intensive. To ensure OpsBuddy remains responsive, I integrated the Sentry Python SDK to trace the performance of the AI agent.

By wrapping the Ollama streaming function in a Sentry transaction, I can monitor the exact inference latency (LLM Calls) directly from the Sentry dashboard. This helps me understand if the context window is getting too large or if the system is slowing down.

Here is a snippet of how I implemented the agent tracing:

# Wrapping the Ollama process with Sentry Tracing
with sentry_sdk.start_transaction(name="Gemma Local Generation") as transaction:
    with transaction.start_child(op="ai.inference", name="Stream Response dari Ollama"):
        
        # Stream the response token-by-token for a zero-latency feel
        for chunk in stream_ai_response(messages):
            console.print(chunk, end="")
            full_reply += chunk
            
# Force Sentry to flush the latency data immediately after the reply
sentry_sdk.flush()


(You can check out the full repository and setup instructions on my GitHub: [github](https://github.com/xdendix/opsbuddy))

Handing It Over

I sent the script over to Andre, helped him install Ollama, and let him run OpsBuddy for the first time. I told him to point the /analyze command at a dummy Nginx crash log I provided.

Here is what he said after his first session:

"Bro, this is actually insane. I thought it was going to ping an external server and take forever, but it’s completely offline and types out the answers instantly. I finally understand how to read a stack trace without being terrified of leaking data." — Andre

Building OpsBuddy didn't just solve a technical problem; it gave my friend the confidence to step into the Ops world safely. Happy coding! 🐧