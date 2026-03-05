import datetime
import json
import requests
import streamlit as st
import uuid
import os

st.set_page_config(
    page_title="TechSupport_AI",
    page_icon="🤖",
    layout="wide",
)

# Après st.set_page_config, ajoutez :
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ─── Config ─────────────────────────────────────────────────────────────────────
OLLAMA_HOST = "http://localhost:11434"

def clear_chat_history():
    st.session_state["chat_messages"] = []

default_ollama_models = {
    "phi3:mini":     "Phi-3 Mini 3.8B",
    "llama3.2:3b":   "Llama 3.2 3B",
    "llama3.2:1b":   "Llama 3.2 1B",
    "llama3.2":      "Llama 3.2 8B",
    "mistral:7b":    "Mistral 7B",
    "gemma2:2b":     "Gemma 2B",
    "codellama:7b":  "Code Llama 7B",
}

openai_models = {
    "gpt-4o":       "GPT-4o",
    "gpt-4o-mini":  "GPT-4o Mini",
    "gpt-4-turbo":  "GPT-4 Turbo",
    "gpt-4":        "GPT-4",
    "gpt-3.5-turbo":"GPT-3.5 Turbo",
    "o1":           "o1",
    "o1-mini":      "o1 Mini",
}

package_data = {"version": "1.0.0", "release_date": datetime.date(2026, 2, 15)}
st.session_state["use_cutoff_date"] = False

def get_cutoff_string():
    if "date_cutoff" not in st.session_state:
        st.session_state["date_cutoff"] = datetime.date(2021, 9, 1)
    if "date_cutoff_today" not in st.session_state:
        st.session_state["date_cutoff_today"] = datetime.date.today()
    if st.session_state["use_cutoff_date"]:
        d1 = st.session_state["date_cutoff"].strftime("%B %d, %Y")
        d2 = st.session_state["date_cutoff_today"].strftime("%B %d, %Y")
        return f"Your knowledge cutoff date is {d1}. Today's date is {d2}."
    return ""


# ─── API helpers ─────────────────────────────────────────────────────────────────

def stream_openai(messages_payload):
    api_key = st.session_state.get("openai_api_key", "")
    if not api_key:
        raise ValueError("No OpenAI API key provided.")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    body = {
        "model": st.session_state["openai_model"],
        "messages": messages_payload,
        "stream": True,
        "max_tokens": st.session_state["max_tokens"],
        "temperature": st.session_state["temperature"],
        "top_p": st.session_state["top_p"],
        "presence_penalty": st.session_state.get("presence_penalty", 0.0),
        "frequency_penalty": st.session_state.get("frequency_penalty", 0.0),
    }
    response = requests.post("https://api.openai.com/v1/chat/completions",
                             headers=headers, json=body, stream=True, timeout=120)
    if response.status_code != 200:
        raise RuntimeError(f"OpenAI error {response.status_code}: {response.text}")
    for line in response.iter_lines():
        if line:
            line_text = line.decode("utf-8")
            if line_text.startswith("data: "):
                data_str = line_text[6:]
                if data_str.strip() == "[DONE]":
                    break
                try:
                    data = json.loads(data_str)
                    delta = data["choices"][0]["delta"]
                    if "content" in delta and delta["content"]:
                        yield delta["content"]
                except Exception:
                    continue

def get_openai(messages_payload):
    api_key = st.session_state.get("openai_api_key", "")
    if not api_key:
        raise ValueError("No OpenAI API key provided.")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    body = {
        "model": st.session_state["openai_model"],
        "messages": messages_payload,
        "stream": False,
        "max_tokens": st.session_state["max_tokens"],
        "temperature": st.session_state["temperature"],
        "top_p": st.session_state["top_p"],
    }
    response = requests.post("https://api.openai.com/v1/chat/completions",
                             headers=headers, json=body, timeout=120)
    if response.status_code != 200:
        raise RuntimeError(f"OpenAI error {response.status_code}: {response.text}")
    return response.json()["choices"][0]["message"]["content"]

def stream_ollama(messages_payload):
    payload = {
        "model": st.session_state["openai_model"],
        "messages": messages_payload,
        "stream": True,
        "options": {
            "temperature": st.session_state["temperature"],
            "top_p": st.session_state["top_p"],
            "num_predict": st.session_state["max_tokens"],
        },
    }
    host = st.session_state.get("ollama_host", OLLAMA_HOST)
    response = requests.post(f"{host}/api/chat", json=payload, stream=True, timeout=60)
    if response.status_code != 200:
        raise RuntimeError(f"Ollama error {response.status_code}: {response.text}")
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line.decode("utf-8"))
                if "message" in data and "content" in data["message"]:
                    yield data["message"]["content"]
            except Exception:
                continue

def get_ollama(messages_payload):
    payload = {
        "model": st.session_state["openai_model"],
        "messages": messages_payload,
        "stream": False,
        "options": {
            "temperature": st.session_state["temperature"],
            "top_p": st.session_state["top_p"],
            "num_predict": st.session_state["max_tokens"],
        },
    }
    host = st.session_state.get("ollama_host", OLLAMA_HOST)
    response = requests.post(f"{host}/api/chat", json=payload, timeout=120)
    if response.status_code != 200:
        raise RuntimeError(f"Ollama error {response.status_code}: {response.text}")
    return response.json()["message"]["content"]


# ─── Sidebar ──────────────────────────────────────────────────────────────────────

with st.sidebar:

    with st.expander("PROVIDER", expanded=True):
        provider = st.radio(
            "Backend",
            ["Ollama (local)", "OpenAI API"],
            label_visibility="collapsed",
        )
        st.session_state["provider"] = provider

        if provider == "OpenAI API":
            api_key = st.text_input(
                "API Key",
                value=st.session_state.get("openai_api_key", ""),
                type="password",
                placeholder="sk-...",
            )
            st.session_state["openai_api_key"] = api_key
            if api_key:
                st.success("Key set")
            else:
                st.warning("Enter your API key")

    with st.expander("MODEL"):
        if provider == "OpenAI API":
            available_models = openai_models
        else:
            available_models = dict(default_ollama_models)
            try:
                host = st.session_state.get("ollama_host", OLLAMA_HOST)
                resp = requests.get(f"{host}/api/tags", timeout=5)
                if resp.status_code == 200:
                    raw = resp.json().get("models", [])
                    if raw:
                        available_models = {m["name"]: m["name"] for m in raw}
            except Exception:
                pass

        st.session_state["openai_model"] = st.selectbox(
            "Model",
            list(available_models.keys()),
            format_func=lambda x: available_models.get(x, x),
            label_visibility="collapsed",
        )

        with open("data/setup_prompts.json", "r") as f:
            setup_prompts = json.load(f)

        # Add custom option
        setup_prompts["custom"] = {
            "label": "Custom",
            "value": "You are a helpful AI assistant.",
        }

        selected_key = st.selectbox(
            "Role",
            list(setup_prompts.keys()),
            format_func=lambda x: setup_prompts[x]["label"],
        )

        if selected_key == "custom":
            custom_val = st.text_input("Custom prompt", value="You are a helpful AI assistant.")
            selected_setup_prompt = {"label": "Custom", "value": custom_val or "You are a helpful AI assistant."}
        else:
            selected_setup_prompt = {
                "label": setup_prompts[selected_key]["label"],
                "value": setup_prompts[selected_key]["value"],
            }

        st.session_state["setup_prompt"] = selected_setup_prompt["value"]

        st.session_state["use_cutoff_date"] = st.checkbox("Knowledge cutoff", value=False)
        if st.session_state["use_cutoff_date"]:
            max_d = datetime.date(2021, 9, 1)
            st.session_state["date_cutoff"] = st.date_input("Cutoff date", value=max_d, max_value=max_d)
            st.session_state["date_cutoff_today"] = st.date_input("Today", value=datetime.date.today())
            st.session_state["setup_prompt"] += f" {get_cutoff_string()}"

    with st.expander("CHAT"):
        st.session_state["streaming_output"] = st.checkbox("Streaming output", value=True)
        st.button("Clear history", use_container_width=True, on_click=clear_chat_history)

    with st.expander("FINE-TUNING"):
        st.session_state["max_tokens"]        = st.slider("Max tokens",   512,  8192, 2048, 16)
        st.session_state["temperature"]       = st.slider("Temperature",  0.0,  2.0,  1.0,  0.01)
        st.session_state["top_p"]             = st.slider("Top P",        0.0,  1.0,  1.0,  0.01)
        st.session_state["presence_penalty"]  = st.slider("Presence",    -2.0,  2.0,  0.0,  0.01)
        st.session_state["frequency_penalty"] = st.slider("Frequency",   -2.0,  2.0,  0.0,  0.01)

    if provider == "Ollama (local)":
        with st.expander("OLLAMA"):
            st.session_state["ollama_host"] = st.text_input("Host", value=OLLAMA_HOST)
            if st.button("Test connection", use_container_width=True):
                try:
                    r = requests.get(f"{st.session_state['ollama_host']}/api/tags", timeout=5)
                    if r.status_code == 200:
                        st.success(f"Connected — {len(r.json().get('models', []))} models found")
                    else:
                        st.error(f"HTTP {r.status_code}")
                except Exception as e:
                    st.error(str(e))

    with st.expander("SESSION"):
        st.session_state.setdefault("session_identifier", str(uuid.uuid4()))
        st.text_input("ID", value=st.session_state["session_identifier"],
                      type="password", disabled=True)
        if st.button("Regenerate", use_container_width=True):
            st.session_state["session_identifier"] = str(uuid.uuid4())


# ─── Header ───────────────────────────────────────────────────────────────────────

model_display = st.session_state.get("openai_model", "—")
prov_short    = "OAI" if st.session_state.get("provider") == "OpenAI API" else "OLLAMA"

st.markdown(f"""
<div class="ts-header">
  <div class="ts-header-logo">TECH<span>SUPPORT_AI</span></div>
  <div class="ts-header-badge">{prov_short} &nbsp;·&nbsp; {model_display}</div>
</div>
""", unsafe_allow_html=True)


# ─── Hero ─────────────────────────────────────────────────────────────────────────

st.markdown(f"""
<div class="hero-section">
  <div class="hero-label">AI Chat Interface</div>
  <div class="hero-title"><span>Your</span> intelligent<br>assistant.</div>
  <div class="hero-sub">{selected_setup_prompt['label']} mode active &nbsp;·&nbsp; Ask anything.</div>
</div>
""", unsafe_allow_html=True)


# ─── Status bar ───────────────────────────────────────────────────────────────────

stream_label = "STREAMING ON" if st.session_state.get("streaming_output", True) else "STREAMING OFF"
st.markdown(f"""
<div class="status-bar">
  <div class="status-dot"></div>
  <div class="status-text">MODEL &nbsp;<strong>{model_display}</strong></div>
  <div class="status-text">TEMP &nbsp;<strong>{st.session_state.get('temperature', 1.0):.2f}</strong></div>
  <div class="status-text">MAX TOKENS &nbsp;<strong>{st.session_state.get('max_tokens', 2048)}</strong></div>
  <div class="status-text"><strong>{stream_label}</strong></div>
</div>
""", unsafe_allow_html=True)


# ─── Chat ─────────────────────────────────────────────────────────────────────────

def messages():
    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = []
    return [{"role": "system", "content": st.session_state["setup_prompt"]}] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state["chat_messages"]
    ]

for message in messages():
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask anything..."):
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    use_openai = st.session_state["provider"] == "OpenAI API"
    current_messages = messages()

    if st.session_state.get("streaming_output", True):
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            try:
                streamer = stream_openai(current_messages) if use_openai else stream_ollama(current_messages)
                for chunk in streamer:
                    full_response += chunk
                    placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)
                st.session_state.chat_messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                placeholder.markdown(f"**Error:** {e}")
                st.error(str(e))
    else:
        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("···")
            try:
                response_text = get_openai(current_messages) if use_openai else get_ollama(current_messages)
                placeholder.markdown(response_text)
                st.session_state.chat_messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                placeholder.markdown(f"**Error:** {e}")
                st.error(str(e))


# ─── Footer ───────────────────────────────────────────────────────────────────────

st.markdown(f"""
<div class="ts-footer">
  TechSupport_AI {package_data['version']} &nbsp;·&nbsp;
  Released {package_data['release_date'].strftime('%B %d, %Y')} &nbsp;·&nbsp;
  AI may produce inaccurate information.
</div>
""", unsafe_allow_html=True)
