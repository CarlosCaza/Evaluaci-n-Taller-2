import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# ==========================================
# 1. CLASE BASE (Plantilla)
# ==========================================
class ScraperBase:
    def __init__(self, fuente_nombre):
        self.fuente_nombre = fuente_nombre
        self.datos_extraidos = []

    def extraer(self):
        pass

# ==========================================
# 2. CLASE: BBC HEALTH (La fuente rigurosa)
# ==========================================
class ScraperBBC(ScraperBase):
    def __init__(self, lista_urls):
        super().__init__(fuente_nombre="BBC")
        self.lista_urls = lista_urls
        # Disfraz de navegador para evitar cualquier bloqueo preventivo
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def extraer(self):
        print(f"\n--- Iniciando extracción de {self.fuente_nombre} ---")
        try:
            for url in self.lista_urls:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                titulo_tag = soup.find('h1')
                titulo = titulo_tag.text.strip() if titulo_tag else "Sin título"

                parrafos = soup.find_all('p')
                texto_completo = " ".join([p.text.strip() for p in parrafos])

                if len(texto_completo) > 50:
                    post_estructurado = {
                        "Fuente": self.fuente_nombre,
                        "Fecha": datetime.now().strftime('%Y-%m-%d'),
                        "Título": titulo,
                        "Texto": texto_completo,
                        "Upvotes": 0, 
                        "URL": url
                    }
                    self.datos_extraidos.append(post_estructurado)
                    print(f"BBC Extraído: {titulo[:40]}...")
        except Exception as e:
            print(f"Error en BBC: {e}")

# ==========================================
# 3. CLASE: BLOGS KETO (El contraste)
# ==========================================
class ScraperBlogs(ScraperBase):
    def __init__(self, lista_urls):
        super().__init__(fuente_nombre="Keto Blogs")
        self.lista_urls = lista_urls
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
        }

    def extraer(self):
        print(f"\n--- Iniciando extracción de {self.fuente_nombre} ---")
        try:
            for url in self.lista_urls:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                titulo_tag = soup.find('h1')
                titulo = titulo_tag.text.strip() if titulo_tag else "Sin título"

                parrafos = soup.find_all('p')
                texto_completo = " ".join([p.text.strip() for p in parrafos])

                if len(texto_completo) > 50:
                    post_estructurado = {
                        "Fuente": self.fuente_nombre,
                        "Fecha": datetime.now().strftime('%Y-%m-%d'),
                        "Título": titulo,
                        "Texto": texto_completo,
                        "Upvotes": 0,
                        "URL": url
                    }
                    self.datos_extraidos.append(post_estructurado)
                    print(f"Blog Extraído: {titulo[:40]}...")
        except Exception as e:
            print(f"Error en Blogs: {e}")

# ==========================================
# 4. EJECUCIÓN E INTEGRACIÓN FINAL
# ==========================================
if __name__ == "__main__":
    
    # --- 1. PROCESAR BBC ---
    urls_bbc = ["https://www.bbc.co.uk/food/articles/keto_diet_weight_loss"]
    bot_bbc = ScraperBBC(lista_urls=urls_bbc)
    bot_bbc.extraer()
    
    df_bbc = pd.DataFrame(bot_bbc.datos_extraidos)
    if not df_bbc.empty:
        df_bbc.to_csv("datos_bbc.csv", index=False, encoding='utf-8')
        print("-> Archivo individual guardado: 'datos_bbc.csv'")

    # --- 2. PROCESAR BLOGS KETO ---
    # Aquí están los links que encontraste
    urls_blogs = [
        "https://perfectketo.com/keto-success-stories/",
        "https://beketo.uk/keto-questions-faq/"
    ]
    bot_blogs = ScraperBlogs(lista_urls=urls_blogs)
    bot_blogs.extraer()
    
    df_blogs = pd.DataFrame(bot_blogs.datos_extraidos)
    if not df_blogs.empty:
        df_blogs.to_csv("datos_blogs.csv", index=False, encoding='utf-8')
        print("-> Archivo individual guardado: 'datos_blogs.csv'")

    # --- 3. INTEGRACIÓN MAESTRA ---
    print("\n--- Integrando bases de datos ---")
    if not df_bbc.empty and not df_blogs.empty:
        df_consolidado = pd.concat([df_bbc, df_blogs], ignore_index=True)
        df_consolidado.to_csv("datos_maestros_keto.csv", index=False, encoding='utf-8')
        print(f"¡Éxito total! Se integraron {len(df_consolidado)} registros en 'datos_maestros_keto.csv'.")
    else:
        print("Faltan datos de alguna fuente para hacer la integración completa.")