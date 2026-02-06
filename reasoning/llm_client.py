# reasoning/llm_client.py

import subprocess


def call_ollama(prompt: str, model: str = "phi3:mini") -> str:
    """
    Windows-safe, CPU-safe Ollama call.
    Explicitly encodes stdin and decodes stdout.
    """

    process = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode("utf-8"),   # 🔑 FIX: encode stdin
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    return process.stdout.decode("utf-8", errors="ignore").strip()
