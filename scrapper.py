from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import os

options = Options()
options.add_argument('--incognito')

base_url = "https://latermicamalaga.com/agenda"
csv_path = 'agenda_termica.csv'

df = pd.read_csv(csv_path)

def obtener_eventos_desde_web():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(base_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    contenedor = soup.find('div', class_='col-md-12 agendaev todos')
    eventos = contenedor.find_all('div', class_='col-md-12 filaagenda')

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
        nombre = evento.select_one('div.eventotop a').text.strip()
        enlace = evento.select_one('div.eventotop a')['href']
        categoria = evento.select_one('p.eventocat').text.strip()
        ubicacion_tag = evento.select_one('span.lugar')
        ubicacion = ubicacion_tag.text.strip() if ubicacion_tag else 'Sin ubicación'
        fecha_hora_tag = evento.select_one('span.fech')
        fecha_hora = fecha_hora_tag.text.strip() if fecha_hora_tag else 'Sin fecha/hora'
        fecha_resumen_tag = evento.select_one('p.fechaagenda')
        fecha_resumen = fecha_resumen_tag.text.strip() if fecha_resumen_tag else 'Sin fecha resumen'

        # Usas tu función para la categoría
        categoria_nueva = clasificar_con_mapa(nombre)

        nombres.append(nombre)
        enlaces.append(enlace)
        etiquetas.append(categoria)
        categorias.append(categoria_nueva)
        ubicaciones.append(ubicacion)
        fechas_hora.append(fecha_hora)
        fechas_resumen.append(convert_fecha(fecha_resumen))
        fecha_modificado.append(fecha_hoy)

    df_web = pd.DataFrame({
        'nombre_evento': nombres,
        'categoria': categorias,
        'ubicacion': ubicaciones,
        'enlace_evento': enlaces,
        'fecha_hora': fechas_hora,
        'fecha_resumen': fechas_resumen,
        'fecha_modificado' : fecha_modificado,
        'etiquetas' : etiquetas
    })
    return df_web

def main():
    df_web = obtener_eventos_desde_web()

    df_web['fecha_resumen'] = df_web['fecha_resumen'].apply(convert_fecha)

    if os.path.exists(csv_path):
        df_guardado = pd.read_csv(csv_path)
        df_guardado['fecha_resumen'] = df['fecha_resumen'].apply(convert_fecha)
        # Filtrar eventos nuevos (nombre_evento + fecha_resumen)
        df_nuevos = df_web[
            ~df_web.set_index(['nombre_evento', 'fecha_resumen']).index.isin(
                df_guardado.set_index(['nombre_evento', 'fecha_resumen']).index
            )
        ]

        if not df_nuevos.empty:
            df_actualizado = pd.concat([df_guardado, df_nuevos], ignore_index=True)
            df_actualizado.to_csv(csv_path, index=False)
            print(f"Se añadieron {len(df_nuevos)} eventos nuevos.")
        else:
            print("No hay eventos nuevos para añadir.")
    else:
        df_web.to_csv(csv_path, index=False)
        print("CSV creado con todos los eventos.")

if __name__ == "__main__":
    main()
