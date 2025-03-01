from config import supabase

def get_offers(product_ids):
    """Busca as ofertas no Supabase em vez de usar Selenium."""
    all_offers = []
    
    for product_id in product_ids:
        response = supabase.table("ofertas").select("*").eq("produto_id", product_id).execute()
        
        if response.data:
            all_offers.extend(response.data)  # Adiciona todas as ofertas encontradas
        
    return all_offers
