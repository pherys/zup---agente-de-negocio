import os
import streamlit as st
import requests

from flask import Flask, request, jsonify

# Se o seu agente precisa de outras bibliotecas, importe-as aqui
# Ex: from openai import OpenAI

app = Flask(__name__)

# Esta é a rota da sua API. O frontend vai chamar este endpoint.
@app.route('/api/agente', methods=['POST'])
def handle_agent_request():
    try:
        # 1. Recebe os dados enviados pelo frontend (o tipo de empresa)
        data = request.json
        business_idea = data.get('business_idea')

        if not business_idea:
            return jsonify({"error": "Nenhuma ideia de negócio foi fornecida"}), 400

        # --- SUA LÓGICA DO AGENTE ENTRA AQUI ---
        #
        # Substitua o código de exemplo abaixo pela lógica real do seu `agente.py`.
        # Você provavelmente tem uma função que recebe a `business_idea` como
        # entrada e retorna o plano de negócio como texto.
        #
        # Exemplo de como chamar sua função:
        # plano_de_negocio = sua_funcao_do_agente(business_idea)
        
        # Simplesmente para demonstração, vamos retornar um texto formatado.
        plano_de_negocio = (
            f"### Mini Plano para: {business_idea.title()} ###\n\n"
            "**Público-Alvo:**\n"
            "Jovens adultos entre 20-35 anos, interessados em produtos sustentáveis e artesanais.\n\n"
            "**Custos Estimados:**\n"
            "- Aluguel e Reforma: R$ 15.000\n"
            "- Equipamentos: R$ 8.000\n"
            "- Marketing Inicial: R$ 5.000\n\n"
            "**Estratégia de Marketing:**\n"
            "Foco em marketing de influência no Instagram e parcerias com comércios locais."
        )
        # --- FIM DA LÓGICA DO AGENTE ---

        # 2. Retorna a resposta em formato JSON para o frontend
        return jsonify({"business_plan": plano_de_negocio})

    except Exception as e:
        # Em caso de erro, retorna uma mensagem clara
        return jsonify({"error": str(e)}), 500

# O Vercel gerencia o servidor, então não precisamos de if __name__ == '__main__':
# Dados de autenticação (NUNCA coloque a chave diretamente no código)
REALM = "stackspot-freemium"
CLIENT_ID = os.getenv("CLIENT_ID")  # Defina no ambiente do Streamlit Cloud!
CLIENT_SECRET = os.getenv("STACKSPOT_API_KEY")  # Defina no ambiente do Streamlit Cloud!
AGENT_ID = os.getenv("AGENT_ID")  # Defina no ambiente do Streamlit Cloud!
API_URL = f"https://genai-inference-app.stackspot.com/v1/agent/{AGENT_ID}/chat"

def obter_jwt():
    if not CLIENT_SECRET:
        raise Exception("Chave secreta não definida. Defina a variável de ambiente STACKSPOT_API_KEY.")
    url = f"https://idm.stackspot.com/{REALM}/oidc/oauth/token"
    payload = f"grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post(url, data=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()["access_token"]

def gerar_mini_plano(pergunta):
    jwt = obter_jwt()
    payload = {
        "streaming": False,
        "user_prompt": pergunta,
        "stackspot_knowledge": False,
        "return_ks_in_response": True
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt}"
    }
    resp = requests.post(API_URL, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data.get("message") or str(data)

# --- Interface Streamlit ---
st.set_page_config(page_title="Mini Plano de Negócio", page_icon="💡", layout="centered")
st.markdown("""
<style>
body {background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);}
.stApp {background: #fff8f0;}
</style>
""", unsafe_allow_html=True)

st.title("Mini Plano de Negócio")
st.subheader("com StackSpot IA")
st.info("Escreva o tipo de empresa que você quer abrir e clique em **Gerar Mini Plano** para receber público-alvo, custos estimados e estratégia de marketing.")

empresa = st.text_input("O que você quer abrir?", placeholder="Ex: cafeteria temática, pet shop, loja de roupas fitness...")

if st.button("💡 Gerar Mini Plano"):
    if not empresa.strip():
        st.warning("Por favor, descreva o que você quer abrir!")
    else:
        with st.spinner("Gerando seu mini plano de negócio..."):
            try:
                resposta = gerar_mini_plano(empresa)
                st.success("Mini plano gerado!")
                st.markdown(f"<div style='background:#e0ffe0; border-radius:10px; padding:16px; color:#3b3b3b; font-size:1.08rem'>{resposta.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erro ao conectar com o agente: {e}")


st.markdown("<div style='text-align:center; color:#b2bec3; margin-top:24px;'>Powered by StackSpot IA &copy; 2024</div>", unsafe_allow_html=True)


