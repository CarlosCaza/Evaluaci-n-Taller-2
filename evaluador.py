import pandas as pd
import random


print("Cargando la base de datos de BBC y Blogs...")
df = pd.read_csv("datos_keto.csv")

# Muestreo Aleatorio Simple (MAS) para extraer 30 filas representativas
n_muestra = min(30, len(df))
df_muestra = df.sample(n=n_muestra, random_state=42).copy()
print(f"Muestra de {n_muestra} textos seleccionada con éxito.")


# Palabras típicas de la desinformación comercial (Red flags)
banderas_rojas = ["miracle", "secret", "burn fat", "fat burning", "fast", "quick", "guaranteed", "cure", "easy", "magic", "transformation"]

# Palabras típicas de fuentes rigurosas (Green flags)
banderas_verdes = ["study", "research", "medical", "science", "evidence", "risk", "side effects", "patients", "doctor"]

def evaluar_texto(texto):
    texto_min = str(texto).lower()
    
    # Contamos cuántas banderas rojas y verdes hay en el texto
    puntos_rojos = sum(1 for palabra in banderas_rojas if palabra in texto_min)
    puntos_verdes = sum(1 for palabra in banderas_verdes if palabra in texto_min)
    
    # Lógica de clasificación
    if puntos_rojos > 0 and puntos_rojos > puntos_verdes:
        return "ALERTA"
    elif puntos_verdes > 0:
        return "CONFIABLE"
    else:
        return "NEUTRAL"


print("Iniciando análisis de palabras clave...")

df_muestra['Veredicto_Final'] = df_muestra['Texto'].apply(evaluar_texto)

archivo_final = "resultados_analisis_keto.csv"
df_muestra.to_csv(archivo_final, index=False, encoding='utf-8')

print(f"\n¡Análisis completado! Revisa el archivo '{archivo_final}'.")
print("\nResumen de resultados:")
print(df_muestra['Veredicto_Final'].value_counts())