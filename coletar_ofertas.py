import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config import supabase
import shutil
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Modo sem interface gráfica
    options.add_argument("--no-sandbox")  # Evita problemas de permissão
    options.add_argument("--disable-dev-shm-usage")  # Evita problemas de memória
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")

    # Caminho do Chrome no ambiente do Streamlit Cloud
    chrome_path = shutil.which("chromium-browser") or shutil.which("google-chrome")

    if chrome_path:
        options.binary_location = chrome_path

    return webdriver.Chrome(options=options)
def scrape_google_shopping_offers(driver, product_id, product_name, brand,):
    offer_url = f"https://www.google.com/shopping/product/{product_id}/offers"
    driver.get(offer_url)
    time.sleep(2)

    seller_data = []
    seller_rows = driver.find_elements(By.CLASS_NAME, 'sh-osd__offer-row')
    
    for row in seller_rows:
        try:
            seller_element = row.find_element(By.CSS_SELECTOR, 'a.b5ycib.shntl')
            seller = seller_element.text.strip()
            price = row.find_element(By.CLASS_NAME, 'drzWO').text.strip()
            link = seller_element.get_attribute("href")  # 🔹 Capturar o href do anúncio
            
            print(f'{brand} → Produto: {product_name}, Vendedor: {seller}, Preço: {price}, Link: {link}')

            seller_data.append({
                'Produto ID': product_id,
                'Produto': product_name,  # 🔹 Atualizamos aqui
                'Marca': brand,
                'Vendedor': seller,
                'Preço': price,
                'Link': link  # 🔹 Salvar o link do anúncio
            })
        except:
            pass

    return seller_data

def coletar_ofertas(brand):
    driver = setup_driver()
    
    # Buscar IDs, Produto e Marca dos produtos no Supabase
    products = supabase.table("produtos").select("produto_id, nome_produto, marca").eq("marca", brand).execute()
    
    all_sellers = []
    for product in products.data:
        product_id = product['produto_id']
        product_name = product['nome_produto']  # 🔹 Ajustar para `produto`
        product_brand = product['marca']
        
        sellers = scrape_google_shopping_offers(driver, product_id, product_name, product_brand)
        
        for offer in sellers:
            # Verificar se a oferta já existe no Supabase antes de inserir
            existing_offer = supabase.table("ofertas").select("*").eq("produto_id", offer["Produto ID"]).eq("vendedor", offer["Vendedor"]).execute()

            if not existing_offer.data:
                supabase.table("ofertas").insert({
                    "produto_id": offer["Produto ID"],
                    "produto": offer["Produto"],  # 🔹 Atualizado para `produto`
                    "marca": offer["Marca"],  # 🔹 Mantivemos `marca`
                    "vendedor": offer["Vendedor"],
                    "preco": offer["Preço"],
                    "link": offer["Link"]  # 🔹 Salvar o link no banco de dados
                }).execute()
        
        all_sellers.extend(sellers)

    driver.quit()
    print("✅ Ofertas coletadas e salvas no banco!")
    return all_sellers

if __name__ == "__main__":
    marca = input("Digite a marca para coletar ofertas: ")
    coletar_ofertas(marca)
