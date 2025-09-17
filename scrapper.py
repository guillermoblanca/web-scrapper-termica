from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
from datetime import datetime

options = Options()
options.add_argument('--incognito')
options.add_argument('--headless')  # Run in background
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

base_url = "https://latermicamalaga.com/agenda"
csv_path = 'agenda_termica.csv'

def convert_fecha(fecha_str):
    """Convert various date formats to a standardized format"""
    if not fecha_str or fecha_str == 'Sin fecha resumen':
        return 'Sin fecha'
    
    # Clean the string
    fecha_str = fecha_str.strip()
    
    # Try to extract date patterns
    date_patterns = [
        r'(\d{1,2})/(\d{1,2})/(\d{4})',  # DD/MM/YYYY
        r'(\d{1,2})-(\d{1,2})-(\d{4})',  # DD-MM-YYYY
        r'(\d{4})-(\d{1,2})-(\d{1,2})',  # YYYY-MM-DD
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, fecha_str)
        if match:
            if pattern == r'(\d{4})-(\d{1,2})-(\d{1,2})':  # YYYY-MM-DD
                return f"{match.group(3)}/{match.group(2)}/{match.group(1)}"
            else:  # DD/MM/YYYY or DD-MM-YYYY
                return f"{match.group(1)}/{match.group(2)}/{match.group(3)}"
    
    return fecha_str

def clasificar_con_mapa(nombre_evento):
    """Classify events into categories based on keywords in the event name"""
    nombre_lower = nombre_evento.lower()
    
    # Category mapping - Order matters! More specific categories first
    categorias = {
        'conferencia': ['conferencia', 'charla', 'mesa redonda', 'debate', 'seminario', 'coloquio'],
        'taller': ['taller', 'workshop', 'curso', 'masterclass', 'clase'],
        'danza': ['danza', 'baile', 'ballet', 'coreografía', 'dance'],
        'cine': ['cine', 'película', 'film', 'documental', 'cortometraje', 'proyección'],
        'literatura': ['libro', 'lectura', 'poesía', 'escritor', 'literatura', 'novela', 'presentación de libro'],
        'infantil': ['infantil', 'niños', 'familia', 'cuentacuentos'],
        'música': ['música', 'concierto', 'festival', 'banda', 'cantante', 'orquesta', 'coral', 'jazz', 'rock', 'pop', 'flamenco'],
        'teatro': ['teatro', 'obra', 'drama', 'comedia', 'representación'],
        'exposición': ['exposición', 'muestra', 'galería', 'arte', 'pintura', 'escultura', 'fotografía'],
        'otros': []
    }
    
    # Check for specific combinations first
    if 'espectáculo' in nombre_lower and 'danza' in nombre_lower:
        return 'danza'
    if 'taller' in nombre_lower and ('pintura' in nombre_lower or 'cerámica' in nombre_lower):
        return 'taller'
    if 'conferencia' in nombre_lower:
        return 'conferencia'
    
    for categoria, palabras_clave in categorias.items():
        for palabra in palabras_clave:
            if palabra in nombre_lower:
                return categoria
    
    return 'otros'

def obtener_eventos_desde_web():
    """Scrape events from La Térmica Málaga website"""
    print("Iniciando web scraping de eventos...")
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(base_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    contenedor = soup.find('div', class_='col-md-12 agendaev todos')
    if not contenedor:
        print("No se encontró el contenedor de eventos")
        return pd.DataFrame()
    
    eventos = contenedor.find_all('div', class_='col-md-12 filaagenda')
    print(f"Encontrados {len(eventos)} eventos")

    nombres = []
    enlaces = []
    categorias = []
    etiquetas = []
    ubicaciones = []
    fechas_hora = []
    fechas_resumen = []
    fecha_modificado = []

    fecha_hoy = pd.Timestamp.today().normalize()

    for evento in eventos:
        try:
            nombre_element = evento.select_one('div.eventotop a')
            nombre = nombre_element.text.strip() if nombre_element else 'Sin nombre'
            enlace = nombre_element['href'] if nombre_element else 'Sin enlace'
            
            categoria_element = evento.select_one('p.eventocat')
            categoria = categoria_element.text.strip() if categoria_element else 'Sin categoría'
            
            ubicacion_tag = evento.select_one('span.lugar')
            ubicacion = ubicacion_tag.text.strip() if ubicacion_tag else 'Sin ubicación'
            
            fecha_hora_tag = evento.select_one('span.fech')
            fecha_hora = fecha_hora_tag.text.strip() if fecha_hora_tag else 'Sin fecha/hora'
            
            fecha_resumen_tag = evento.select_one('p.fechaagenda')
            fecha_resumen = fecha_resumen_tag.text.strip() if fecha_resumen_tag else 'Sin fecha resumen'

            # Use classification function for category
            categoria_nueva = clasificar_con_mapa(nombre)

            nombres.append(nombre)
            enlaces.append(enlace)
            etiquetas.append(categoria)
            categorias.append(categoria_nueva)
            ubicaciones.append(ubicacion)
            fechas_hora.append(fecha_hora)
            fechas_resumen.append(convert_fecha(fecha_resumen))
            fecha_modificado.append(fecha_hoy)
            
        except Exception as e:
            print(f"Error procesando evento: {e}")
            continue

    df_web = pd.DataFrame({
        'nombre_evento': nombres,
        'categoria': categorias,
        'ubicacion': ubicaciones,
        'enlace_evento': enlaces,
        'fecha_hora': fechas_hora,
        'fecha_resumen': fechas_resumen,
        'fecha_modificado': fecha_modificado,
        'etiquetas': etiquetas
    })
    return df_web

def main():
    """Main function to run the scraper and save data to CSV"""
    try:
        df_web = obtener_eventos_desde_web()
        
        if df_web.empty:
            print("No se obtuvieron eventos del sitio web")
            return

        df_web['fecha_resumen'] = df_web['fecha_resumen'].apply(convert_fecha)

        if os.path.exists(csv_path):
            print(f"Archivo CSV existente encontrado: {csv_path}")
            df_guardado = pd.read_csv(csv_path)
            df_guardado['fecha_resumen'] = df_guardado['fecha_resumen'].apply(convert_fecha)
            
            # Filter new events (nombre_evento + fecha_resumen)
            df_nuevos = df_web[
                ~df_web.set_index(['nombre_evento', 'fecha_resumen']).index.isin(
                    df_guardado.set_index(['nombre_evento', 'fecha_resumen']).index
                )
            ]

            if not df_nuevos.empty:
                df_actualizado = pd.concat([df_guardado, df_nuevos], ignore_index=True)
                df_actualizado.to_csv(csv_path, index=False)
                print(f"Se añadieron {len(df_nuevos)} eventos nuevos.")
                print(f"Total de eventos en el archivo: {len(df_actualizado)}")
            else:
                print("No hay eventos nuevos para añadir.")
        else:
            df_web.to_csv(csv_path, index=False)
            print(f"CSV creado con {len(df_web)} eventos.")
            
        print(f"Datos guardados en: {csv_path}")
        
    except Exception as e:
        print(f"Error en la ejecución principal: {e}")

if __name__ == "__main__":
    main()