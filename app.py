import streamlit as st
import time
import pandas as pd
import io
from config import supabase
from coletar_ofertas import scrape_google_shopping_offers, setup_driver

def get_brands():
    """Obtém a lista de marcas disponíveis no Supabase."""
    response = supabase.table("produtos").select("marca").execute()
    brands = list(set([item["marca"] for item in response.data]))
    return brands

def get_products_by_brand(brand):
    """Obtém os produtos de uma marca específica."""
    response = supabase.table("produtos").select("produto_id, nome_produto").eq("marca", brand).execute()
    return response.data

def get_offers(product_ids, product_names, brand):
    """Coleta e exibe ofertas para os produtos selecionados."""
    driver = setup_driver()
    all_offers = []
    for product_id, product_name in zip(product_ids, product_names):
        offers = scrape_google_shopping_offers(driver, product_id, product_name, brand)
        for offer in offers:
            offer["Produto"] = product_name
            all_offers.append(offer)
    driver.quit()
    return all_offers

# Lista de usuários autorizados
USERS = {
    "Jonas Lubas": "pricing2025",
    "Adriene Fonseca": "pricing2025",
    "Rafaella Tesch": "pricing2025",
    "Larissa Pio": "pricing2025",
    "Luã Genaro": "pricing2025",
    "Igor Assis": "pricing2025",
    "Thayssa Nascimento": "pricing2025",
    "Gabrieli Tays": "pricing2025"
}

# Interface Streamlit
st.set_page_config(page_title="Comparador de Preços", page_icon="🔎", layout="wide")

# Inicializa a variável de autenticação na sessão de forma garantida
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""

if not st.session_state["authenticated"]:
    st.markdown("<h1 class='title'>🔑 Login</h1>", unsafe_allow_html=True)
    username = st.text_input("Nome de Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if username in USERS and USERS[username] == password:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.rerun()
        else:
            st.error("⚠️ Nome de usuário ou senha incorretos. Tente novamente.")
    st.stop()

if st.button("🚪 Logout"):
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""
    st.rerun()

st.markdown(f"<h1 class='title'>🔎 Comparador de Preços - Google Shopping</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>Bem-vindo, {st.session_state['username']}! Encontre as melhores ofertas de produtos rapidamente.</p>", unsafe_allow_html=True)

# Aba de busca
col1, col2 = st.columns([1, 2])

with col1:
    brands = get_brands()
    selected_brand = st.selectbox("Selecione uma marca:", brands)

if selected_brand:
    with st.expander("📌 Escolha os produtos", expanded=True):
        products = get_products_by_brand(selected_brand)
        product_options = {prod["nome_produto"]: prod["produto_id"] for prod in products}
        selected_products = st.multiselect("Selecione os produtos:", ["Todos"] + list(product_options.keys()))
    
    if "Todos" in selected_products:
        selected_products = list(product_options.keys())
    
    if selected_products:
        product_ids = [product_options[name] for name in selected_products]
        buscar = st.button("🔍 Buscar Ofertas")
    
        if buscar:
            with st.spinner("🔍 Buscando as melhores ofertas... Aguarde um momento!"):
                time.sleep(2)
                offers = get_offers(product_ids, selected_products, selected_brand)
            
            if offers:
                st.success("✅ Ofertas encontradas!")
                df = pd.DataFrame(offers)
                df["Preço"] = df["Preço"].apply(lambda x: f"{x}")
                df["Link"] = df["Link"].apply(lambda x: f"{x}")
                st.dataframe(df)
            else:
                st.warning("⚠️ Nenhuma oferta encontrada para os produtos selecionados.")
