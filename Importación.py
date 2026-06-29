import logging
from datetime import datetime
import os
import csv
from pathlib import Path

# ==========================================
# IMPORTACIÓN DEL MÓDULO
# ==========================================
# Importamos la clase ScraperBBC

import ScraperBBC
import ScraperReddit

# Configuración básica de registros (Logs)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')

# ==========================================
# CLASE DE ALMACENAMIENTO
# ==========================================
class StorageManager:
    def __init__(self, output_dir="data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True) 

    def save_to_csv(self, data: list[dict], filename: str):
        if not data:
            logging.warning("No hay datos para guardar.")
            return

        filepath = self.output_dir / f"{filename}.csv"
        # Obtener los encabezados del primer diccionario
        headers = data[0].keys()

        with open(filepath, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        return filepath

# ==========================================
# CLASE PIPELINE
# ==========================================
class HealthNewsPipeline:
    def __init__(self, storage_format="csv"):
        self.storage_format = storage_format
        self.execution_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.storage = StorageManager(output_dir="data")

    def run(self):
        logging.info(f"=== Iniciando Pipeline de Desinformación en Salud [ID: {self.execution_id}] ===")

        # --- PASO 1: EXTRACCIÓN ---
        logging.info("Fase 1/3: Extrayendo datos...")
        raw_data = self._extract()

        if not raw_data:
            logging.warning("No se obtuvieron datos. Cancelando pipeline.")
            return

        # --- PASO 2: TRANSFORMACIÓN ---
        logging.info(f"Fase 2/3: Procesando y limpiando {len(raw_data)} artículos...")
        cleaned_data = self._transform(raw_data)

        # --- PASO 3: CARGA (Almacenamiento) ---
        logging.info("Fase 3/3: Guardando datos integrados...")
        self._load(cleaned_data)
        
        logging.info("=== Pipeline finalizado con éxito ===")

    def _extract(self):
        """
        AQUÍ OCURRE LA CONEXIÓN: Llamamos a las clases de Persona 2
        """
        datos_totales = []

        # Ejecutamos el Scraper de la BBC
        urls_bbc = ["https://www.bbc.co.uk/food/articles/keto_diet_weight_loss"]
        bot_bbc = ScraperBBC(lista_urls=urls_bbc)
        bot_bbc.extraer()
        
        # Sumamos los datos reales extraídos a nuestra lista total
        datos_totales.extend(bot_bbc.datos_extraidos)

        bot_reddit = ScraperReddit(limite_posts=100)
        bot_reddit.extraer()
        datos_totales.extend(bot_reddit.datos_extraidos)

        return datos_totales

    def _transform(self, data):
        return data

    def _load(self, data):
        nombre_archivo = f"datos_maestros_{self.execution_id}"
        ruta_guardada = self.storage.save_to_csv(data, nombre_archivo)
        logging.info(f"--> [OK] Registros guardados en {ruta_guardada}")


if __name__ == "__main__":
    sistema = HealthNewsPipeline(storage_format="csv")
    sistema.run()