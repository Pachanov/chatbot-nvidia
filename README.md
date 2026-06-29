# 🟢 NvidiaChat — Chatbot Open Source na Oracle Cloud

> *Disciplina: Produtos de GenAI · Pós-Graduação em IA Generativa Aplicada — UFPR 2026*

## 🚀 Implantei um Chatbot com LLM Open Source na Nuvem

Ao longo de três aulas da disciplina **Produtos de GenAI**, o desafio foi claro: sair do Jupyter Notebook e colocar um chatbot baseado em modelo open source **funcionando de verdade**, acessível para qualquer pessoa via navegador, rodando em infraestrutura de nuvem pública.

---

## 🎯 Objetivo da Atividade

- Um **modelo open source** via NVIDIA NIM API
- **Python + Streamlit** como stack de desenvolvimento
- **Oracle Cloud Infrastructure (OCI)** como plataforma de hospedagem
- Boas práticas de segurança e gerenciamento de credenciais

---

## 🖥️ Infraestrutura

| Recurso | Configuração |
|---|---|
| Shape | VM.Standard.E2.1.Micro (Always Free) |
| vCPUs | 1 OCPU (AMD) |
| RAM | 1 GB |
| SO | Ubuntu 22.04 LTS |
| IP Público | 163.176.192.253 |

---

## 🤖 Modelo: Meta Llama 3.1 8B Instruct

- Open source com pesos públicos
- 8B parâmetros — ótimo custo-benefício
- Bom desempenho em português
- Servido via NVIDIA NIM com otimizações TensorRT-LLM

---

## 🏗️ Desenvolvimento

**Arquitetura:**

**Bibliotecas:** streamlit, chatlas, openai, python-dotenv

**Credenciais:** NVIDIA_API_KEY carregada via python-dotenv, nunca commitada no repositório.

---

## ☁️ Implantação na Oracle Cloud

```bash
git clone https://github.com/Pachanov/chatbot-nvidia.git
cd chatbot_curso
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export NVIDIA_API_KEY="nvapi-..."
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
```

**Principais desafios:**
- Firewall duplo: Security List da OCI + ufw do Ubuntu
- Streamlit requer --server.address 0.0.0.0 para acesso externo
- Autenticação GitHub via SSH key

---

## 💡 Lições Aprendidas

- Infraestrutura tem camadas: VCN, subnet, security list e ufw precisam estar alinhados
- O SDK OpenAI é compatível com a NVIDIA NIM API
- Streamlit é poderoso para MVPs de IA
- Segurança de credenciais não é opcional mesmo em projetos acadêmicos

---

## 🔗 Links

- 🌐 **Aplicação**: http://163.176.192.253:8501
- 📦 **GitHub**: https://github.com/Pachanov/chatbot-nvidia
- 🤖 **NVIDIA NIM**: https://build.nvidia.com

---

*Desenvolvido por **Victor Hugo Pachano Maurera** — Junior MIS Data Analyst | Pós-Graduando em IA Generativa Aplicada (UFPR 2026–2027)*

*#GenAI #LLM #Python #Streamlit #OracleCloud #NVIDIA #OpenSource #Llama*
