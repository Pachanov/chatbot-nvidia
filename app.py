import os
import streamlit as st
from dotenv import load_dotenv
from chatlas import ChatOpenAICompletions

load_dotenv()

st.set_page_config(
    page_title="Prompt Lab",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

  :root {
    --bg:      #0a0f1e;
    --surface: #111827;
    --border:  #1f2d3d;
    --accent:  #76b900;
    --accent2: #00d4aa;
    --text:    #e2e8f0;
    --muted:   #64748b;
    --user-bg: #1a2744;
  }

  html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Space Grotesk', sans-serif;
  }
  [data-testid="stHeader"]  { background: transparent !important; }
  [data-testid="stSidebar"] {
    background: #0d1424 !important;
    border-right: 1px solid var(--border) !important;
  }
  #MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }

  /* ── Título ── */
  .titulo {
    font-size: 1.9rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 24px 0 6px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 28px;
  }
  .titulo .dot {
    width: 13px; height: 13px;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 14px var(--accent);
    animation: pulse 2s infinite;
    flex-shrink: 0;
  }
  .titulo .badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: var(--accent);
    border: 1px solid var(--accent);
    padding: 3px 10px;
    border-radius: 999px;
    letter-spacing: .08em;
  }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.3} }

  /* ── Mensagens ── */
  .msg-wrap { display: flex; flex-direction: column; gap: 18px; padding-bottom: 100px; }
  .msg { display: flex; gap: 12px; align-items: flex-start; animation: fadeUp .2s ease; }
  .msg.user { flex-direction: row-reverse; }
  @keyframes fadeUp { from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:translateY(0)} }

  .avatar {
    width: 36px; height: 36px; border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem; font-weight: 700; flex-shrink: 0;
  }
  .avatar.bot  { background: var(--accent); color: #000; }
  .avatar.user { background: var(--user-bg); color: var(--accent2); border: 1px solid var(--border); }

  .bubble {
    max-width: 75%; padding: 13px 17px; border-radius: 14px;
    font-size: 0.92rem; line-height: 1.7;
    white-space: pre-wrap; word-break: break-word;
  }
  .bubble.bot {
    background: var(--surface); border: 1px solid var(--border);
    border-top-left-radius: 4px; color: var(--text);
  }
  .bubble.user {
    background: var(--user-bg); border: 1px solid #1e3a5f;
    border-top-right-radius: 4px; color: var(--text);
  }
  .bubble code {
    font-family: 'JetBrains Mono', monospace; font-size: 0.8rem;
    background: rgba(118,185,0,.12); color: var(--accent);
    padding: 1px 6px; border-radius: 4px;
  }

  /* ── Input ── */
  section[data-testid="stBottom"] {
    background: var(--bg) !important;
    border-top: 1px solid var(--border) !important;
    padding-top: 8px !important;
  }
  [data-testid="stChatInput"] {
    background: var(--bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
  }
  [data-testid="stChatInput"] textarea {
    background: var(--bg) !important;
    color: #ffffff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    caret-color: var(--accent) !important;
  }
  [data-testid="stChatInput"] textarea::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
  }
  [data-testid="stChatInput"]:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(118,185,0,.15) !important;
  }

  /* ── Sidebar cards ── */
  .model-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 16px; margin-bottom: 16px; font-size: 0.83rem;
  }
  .model-card .lbl {
    color: var(--muted); font-size: 0.68rem;
    text-transform: uppercase; letter-spacing: .07em; margin-bottom: 2px;
  }
  .model-card .val { color: var(--text); font-weight: 600; margin-bottom: 12px; }
  .model-card .val:last-child { margin-bottom: 0; }

  .tag {
    display: inline-block;
    background: rgba(118,185,0,.1); color: var(--accent);
    border: 1px solid rgba(118,185,0,.3); border-radius: 6px;
    padding: 2px 8px; font-size: 0.7rem;
    font-family: 'JetBrains Mono', monospace; margin: 2px;
  }

  .topic-item {
    padding: 7px 0; font-size: 0.84rem;
    color: #94a3b8; border-bottom: 1px solid var(--border);
  }

  /* ── Botão ── */
  .stButton button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.82rem !important;
    transition: all .2s !important;
    width: 100% !important;
  }
  .stButton button:hover { border-color: #e53e3e !important; color: #e53e3e !important; }

  ::-webkit-scrollbar { width: 5px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Cliente NVIDIA NIM ────────────────────────────────────────────────────────
chat = ChatOpenAICompletions(
    model="meta/llama-3.3-70b-instruct",
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)

SYSTEM_PROMPT = """
Você é um assistente especializado em engenharia de prompt.
Seu papel é ajudar o usuário a explorar diferentes estratégias
de construção de prompts para modelos de linguagem.
Sempre que possível:
- explique conceitos de forma objetiva;
- mostre exemplos práticos;
- compare abordagens quando solicitado;
- mantenha respostas técnicas e concisas.
"""

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:8px 0 20px;">
      <div style="font-size:1.1rem;font-weight:700;color:#e2e8f0;letter-spacing:-0.02em;">
        🟢 Prompt Lab
      </div>
      <div style="font-size:0.7rem;color:#64748b;font-family:'JetBrains Mono',monospace;margin-top:2px;">
        powered by NVIDIA NIM
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="model-card">
      <div class="lbl">Modelo</div>
      <div class="val">Llama 3.3 · 70B</div>
      <div class="lbl">Provedor</div>
      <div class="val">NVIDIA NIM API</div>
      <div class="lbl">Capacidades</div>
      <div style="margin-top:6px;">
        <span class="tag">Português 🇧🇷</span>
        <span class="tag">128K ctx</span>
        <span class="tag">Open Source</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin:20px 0 8px;font-size:0.68rem;color:#64748b;text-transform:uppercase;letter-spacing:.07em;">
      Tópicos
    </div>
    """, unsafe_allow_html=True)

    topics = ["Prompt Engineering","Chain of Thought","Few-Shot Learning",
              "RAG","Agentes","LLMs","Avaliação de Prompts"]
    for t in topics:
        st.markdown(f'<div class="topic-item">→ {t}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑 Limpar conversa"):
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Olá! Como posso ajudar você com Engenharia de Prompt?"}
        ]
        st.rerun()

    st.markdown("""
    <div style="margin-top:24px;padding-top:16px;border-top:1px solid #1f2d3d;
                font-size:0.7rem;color:#64748b;line-height:1.7;">
      Disciplina <strong style="color:#94a3b8;">Produtos de GenAI</strong><br>
      UFPR · Pós-Graduação IA Generativa<br>
      2026–2027
    </div>
    """, unsafe_allow_html=True)

# ── Cabeçalho ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="titulo">
  <div class="dot"></div>
  Engenharia de Prompt
  <span class="badge">LLAMA 3.3 · 70B</span>
</div>
""", unsafe_allow_html=True)

# ── Histórico ─────────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Olá! Como posso ajudar você com Engenharia de Prompt?"}
    ]

st.markdown('<div class="msg-wrap">', unsafe_allow_html=True)
for message in st.session_state.chat_history:
    role    = message["role"]
    content = message["content"]
    av_cls  = "bot" if role == "assistant" else "user"
    av_char = "AI"  if role == "assistant" else "V"
    align   = ""    if role == "assistant" else " user"
    st.markdown(f"""
    <div class="msg{align}">
      <div class="avatar {av_cls}">{av_char}</div>
      <div class="bubble {av_cls}">{content}</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Input e resposta ──────────────────────────────────────────────────────────
user_question = st.chat_input("Digite sua pergunta sobre Engenharia de Prompt...")

if user_question:
    st.session_state.chat_history.append({"role": "user", "content": user_question})

    conversation = SYSTEM_PROMPT + "\n\n"
    for msg in st.session_state.chat_history:
        conversation += f"{msg['role']}: {msg['content']}\n"

    with st.spinner(""):
        try:
            response = chat.chat(conversation, stream=False)
            answer   = str(response)
        except Exception as e:
            answer = f"⚠️ Erro ao chamar a API NVIDIA: `{e}`"

    st.session_state.chat_history.append({"role": "assistant", "content": answer})
    st.rerun()