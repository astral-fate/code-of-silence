"""OpenAI-compatible clients for OpenRouter, NVIDIA NIM, Groq and Experiential Labs. Keys come from the
environment or ./.env: OPENROUTER_API_KEY, NVIDIA_API_KEY, GROQ_API_KEY, XPL_API_KEY (only the providers you
use need a key). With USE_XPL=1, the models Experiential Labs serves are routed there (see XPL_ROUTE)."""
import os
import threading
import time

from dotenv import load_dotenv
from openai import OpenAI

PROVIDERS = {
    "openrouter": ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY"),
    "nim": ("https://integrate.api.nvidia.com/v1", "NVIDIA_API_KEY"),
    "groq": ("https://api.groq.com/openai/v1", "GROQ_API_KEY"),
    "xpl": ("https://api.experientiallabs.ai/v1", "XPL_API_KEY"),
}

# short name -> (provider, model id, reasoning model?). Mistral-7B-Instruct-v0.3 (the source paper's
# original fourth seat) is not served by any of these providers, so ministral-8b substitutes for it as
# in the sprint starter repo.
MODELS = {
    # the source paper's small roster
    "llama-3.1-8b": ("openrouter", "meta-llama/llama-3.1-8b-instruct", False),
    "qwen2.5-7b": ("openrouter", "qwen/qwen-2.5-7b-instruct", False),
    "llama-3.2-3b": ("openrouter", "meta-llama/llama-3.2-3b-instruct", False),
    "ministral-8b": ("openrouter", "mistralai/ministral-8b-2512", False),
    # other families and sizes
    "gpt-4.1-mini": ("openrouter", "openai/gpt-4.1-mini", False),
    "gemma-3-12b": ("openrouter", "google/gemma-3-12b-it", False),
    "gpt-oss-120b": ("openrouter", "openai/gpt-oss-120b", True),  # was Groq; its free tier rate-limits
    "gpt-oss-120b-or": ("openrouter", "openai/gpt-oss-120b", True),  # same model, OpenRouter route
    "qwen3.8-27b": ("openrouter", "qwen/qwen3.8-27b", True),       # Groq free tier rejects the request size
    "gpt-oss-20b": ("nim", "openai/gpt-oss-20b", True),
    "nemotron-3-ultra": ("nim", "nvidia/nemotron-3-ultra-550b-a55b", True),
    "nemotron-3.5-lightning": ("openrouter", "nvidia/nemotron-3.5-lightning", True),  # NIM free tier rate-limits
    "minimax-m3.1-flash": ("openrouter", "minimax/minimax-m3.1-flash", True),        # NIM free tier rate-limits
    "deepseek-v4.1-flash": ("nim", "deepseek-ai/deepseek-v4.1-flash", True),  # slow on the free tier
    "gemma-4-31b": ("nim", "google/gemma-4-31b-it", False),                    # slow on the free tier
}
# same weights on Experiential Labs; used instead of the routes above when USE_XPL=1. The other models
# (llama-3.1-8b, qwen2.5-7b, llama-3.2-3b, ministral-8b, minimax-m3.1-flash) are not served there.
XPL_ROUTE = {
    "gpt-4.1-mini": "gpt-4.1-mini", "gemma-3-12b": "gemma-3-12b-it", "gpt-oss-120b": "gpt-oss-120b",
    "gpt-oss-120b-or": "gpt-oss-120b", "qwen3.8-27b": "qwen3.8-27b", "gpt-oss-20b": "gpt-oss-20b",
    "nemotron-3.5-lightning": "nemotron-3.5-lightning", "deepseek-v4.1-flash": "deepseek-v4.1-flash",
    "gemma-4-31b": "gemma-4-31b-it",
}
DEFAULT_MODELS = ["llama-3.1-8b", "qwen2.5-7b", "llama-3.2-3b", "ministral-8b", "gpt-4.1-mini"]


def sampling(short: str) -> dict:
    """Per-family sampling used by the source harness."""
    if "llama" in short:
        return dict(temperature=0.8, top_p=0.95)
    if "qwen" in short:
        return dict(temperature=0.8, top_p=0.9)
    return dict(temperature=0.7, top_p=0.9)


_clients: dict = {}
# concurrent calls allowed per provider (free tiers rate-limit hard)
_LIMITS = {"openrouter": 24, "nim": 2, "groq": 2, "xpl": 16}
_sems: dict = {}


def client_for(provider: str) -> OpenAI:
    if provider not in _clients:
        load_dotenv(".env")
        base, env = PROVIDERS[provider]
        key = os.environ.get(env)
        if not key:
            raise SystemExit(f"{env} is not set (see .env.example).")
        _clients[provider] = OpenAI(base_url=base, api_key=key, timeout=180, max_retries=0)
    return _clients[provider]


def chat(short: str, messages: list[dict], max_tokens: int = 160, retries: int = 6, temperature: float | None = None):
    """Returns (text, usage_dict, model_id_served). Reasoning models get room to think before answering.
    Transient errors are retried; the last error is returned as text so it shows up in the results."""
    provider, model_id, reasoning = MODELS[short]
    load_dotenv(".env")
    if os.environ.get("USE_XPL") == "1" and short in XPL_ROUTE:
        provider, model_id = "xpl", XPL_ROUTE[short]
    client = client_for(provider)
    params = sampling(short) if temperature is None else {"temperature": temperature}   # judges use 0
    sem = _sems.setdefault(provider, threading.BoundedSemaphore(_LIMITS[provider]))
    err = None
    for attempt in range(retries):
        try:
            with sem:
                r = client.chat.completions.create(model=model_id, messages=messages,
                                                   max_tokens=1500 if reasoning else max_tokens, **params)
            return (r.choices[0].message.content or ""), (r.usage.model_dump() if r.usage else {}), r.model
        except Exception as e:  # noqa: BLE001
            err = e
            time.sleep(min(60, 5 * 2 ** attempt))   # exponential backoff for rate limits
    return f"<<error: {err}>>", {}, None
