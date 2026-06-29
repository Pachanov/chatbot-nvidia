# 🟢 NvidiaChat — Chatbot Open Source na Oracle Cloud

> *Disciplina: Produtos de GenAI · Pós-Graduação em IA Generativa Aplicada — UFPR 2026*

## 🚀 Implantei um Chatbot com LLM Open Source na Nuvem

Ao longo de três aulas da disciplina **Produtos de GenAI**, o desafio foi claro: sair do Jupyter Notebook e colocar um chatbot baseado em modelo open source **funcionando de verdade**, acessível para qualquer pessoa via navegador, rodando em infraestrutura de nuvem pública.

---

## 🎯 Objetivo da Atividade

Desenvolver e implantar um chatbot com IA Generativa utilizando:
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
