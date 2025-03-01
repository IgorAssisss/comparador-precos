import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config import supabase

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_product_ids(query, brand):
    driver = setup_driver()
    search_url = f'https://www.google.com/search?tbm=shop&q={query}'
    driver.get(search_url)
    time.sleep(5)

    product_data = []
    
    while True:  # Loop para ir para a próxima página até não haver mais
        product_links = driver.find_elements(By.CSS_SELECTOR, 'a.Lq5OHe')
        product_titles = driver.find_elements(By.CSS_SELECTOR, 'h3.tAxDx')

        for link, title in zip(product_links, product_titles):
            href = link.get_attribute('href')
            match = re.search(r'product/(\d+)', href)
            if match:
                product_id = match.group(1)
                product_name = title.text.strip()

                # Verificar se o ID já existe no Supabase
                existing = supabase.table("produtos").select("*").eq("produto_id", product_id).execute()
                if not existing.data:  
                    print(f'Novo produto encontrado: {product_name} (ID: {product_id})')

                    # Inserir no Supabase
                    supabase.table("produtos").insert({
                        "produto_id": product_id,
                        "nome_produto": product_name,
                        "marca": brand
                    }).execute()
                
                product_data.append({'Produto ID': product_id, 'Nome do Produto': product_name})

        # Tentar clicar no botão "Próxima Página"
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'a#pnnext')
            next_button.click()
            time.sleep(5)  # Esperar o carregamento da nova página
        except:
            print("🚀 Todas as páginas foram processadas. Finalizando coleta.")
            break  # Sai do loop se não houver próxima página

    driver.quit()
    return product_data

if __name__ == "__main__":
    query = input("Digite o nome da marca para buscar no Google Shopping: ")
    get_product_ids(query, query)
