#!/usr/bin/env python3
"""
Demo script to show how the web scrapper works without hitting the actual website.
This creates sample data to demonstrate the CSV output format and functionality.
"""

import pandas as pd
import os
from datetime import datetime
from scrapper import convert_fecha, clasificar_con_mapa

def create_demo_data():
    """Create sample event data to demonstrate the scrapper functionality"""
    
    # Sample events similar to what might be found on La Térmica Málaga
    sample_events = [
        {
            'nombre': 'Concierto de Flamenco Fusión',
            'categoria_original': 'Música',
            'ubicacion': 'Sala de Conciertos',
            'enlace': 'https://latermicamalaga.com/evento/flamenco-fusion',
            'fecha_hora': '21:00h',
            'fecha_resumen': '15/12/2024'
        },
        {
            'nombre': 'Obra de Teatro: La Casa de Bernarda Alba',
            'categoria_original': 'Teatro',
            'ubicacion': 'Teatro Principal',
            'enlace': 'https://latermicamalaga.com/evento/bernarda-alba',
            'fecha_hora': '20:30h',
            'fecha_resumen': '16/12/2024'
        },
        {
            'nombre': 'Exposición de Fotografía Contemporánea',
            'categoria_original': 'Arte',
            'ubicacion': 'Galería Norte',
            'enlace': 'https://latermicamalaga.com/evento/fotografia-contemporanea',
            'fecha_hora': '18:00h',
            'fecha_resumen': '17/12/2024'
        },
        {
            'nombre': 'Taller de Cerámica para Principiantes',
            'categoria_original': 'Talleres',
            'ubicacion': 'Aula de Arte',
            'enlace': 'https://latermicamalaga.com/evento/taller-ceramica',
            'fecha_hora': '10:00h',
            'fecha_resumen': '18/12/2024'
        },
        {
            'nombre': 'Conferencia: El Futuro del Arte Digital',
            'categoria_original': 'Conferencias',
            'ubicacion': 'Auditorio',
            'enlace': 'https://latermicamalaga.com/evento/arte-digital',
            'fecha_hora': '19:00h',
            'fecha_resumen': '19/12/2024'
        },
        {
            'nombre': 'Espectáculo de Danza Contemporánea',
            'categoria_original': 'Danza',
            'ubicacion': 'Sala de Danza',
            'enlace': 'https://latermicamalaga.com/evento/danza-contemporanea',
            'fecha_hora': '21:30h',
            'fecha_resumen': '20/12/2024'
        },
        {
            'nombre': 'Proyección: Documental sobre Málaga',
            'categoria_original': 'Cine',
            'ubicacion': 'Sala de Proyección',
            'enlace': 'https://latermicamalaga.com/evento/documental-malaga',
            'fecha_hora': '20:00h',
            'fecha_resumen': '21/12/2024'
        },
        {
            'nombre': 'Presentación de Libro: Poesía Malagueña',
            'categoria_original': 'Literatura',
            'ubicacion': 'Biblioteca',
            'enlace': 'https://latermicamalaga.com/evento/poesia-malaguena',
            'fecha_hora': '19:30h',
            'fecha_resumen': '22/12/2024'
        },
        {
            'nombre': 'Cuentacuentos Navideños para Niños',
            'categoria_original': 'Infantil',
            'ubicacion': 'Sala Infantil',
            'enlace': 'https://latermicamalaga.com/evento/cuentacuentos-navidad',
            'fecha_hora': '17:00h',
            'fecha_resumen': '23/12/2024'
        }
    ]
    
    return sample_events

def demo_scrapper_functionality():
    """Demonstrate the scrapper functionality with sample data"""
    
    print("🎭 Web Scrapper Térmica Málaga - DEMO")
    print("=" * 50)
    print("Este demo muestra cómo funciona el scrapper sin conectarse al sitio web real.\n")
    
    # Create sample data
    events = create_demo_data()
    print(f"📊 Procesando {len(events)} eventos de muestra...\n")
    
    # Process events like the real scrapper would
    nombres = []
    enlaces = []
    categorias = []
    etiquetas = []
    ubicaciones = []
    fechas_hora = []
    fechas_resumen = []
    fecha_modificado = []
    
    fecha_hoy = pd.Timestamp.today().normalize()
    
    print("🔄 Clasificando eventos automáticamente...")
    for i, evento in enumerate(events, 1):
        nombre = evento['nombre']
        categoria_automatica = clasificar_con_mapa(nombre)
        fecha_convertida = convert_fecha(evento['fecha_resumen'])
        
        nombres.append(nombre)
        enlaces.append(evento['enlace'])
        categorias.append(categoria_automatica)
        etiquetas.append(evento['categoria_original'])
        ubicaciones.append(evento['ubicacion'])
        fechas_hora.append(evento['fecha_hora'])
        fechas_resumen.append(fecha_convertida)
        fecha_modificado.append(fecha_hoy)
        
        print(f"   {i}. {nombre[:50]}{'...' if len(nombre) > 50 else ''}")
        print(f"      → Categoría: {categoria_automatica}")
    
    # Create DataFrame
    df_demo = pd.DataFrame({
        'nombre_evento': nombres,
        'categoria': categorias,
        'ubicacion': ubicaciones,
        'enlace_evento': enlaces,
        'fecha_hora': fechas_hora,
        'fecha_resumen': fechas_resumen,
        'fecha_modificado': fecha_modificado,
        'etiquetas': etiquetas
    })
    
    # Save to CSV
    demo_csv_path = 'demo_agenda_termica.csv'
    df_demo.to_csv(demo_csv_path, index=False)
    
    print(f"\n✅ Datos guardados en: {demo_csv_path}")
    print(f"📈 Total de eventos procesados: {len(df_demo)}")
    
    # Show statistics
    print("\n📊 Estadísticas por categoría:")
    categoria_stats = df_demo['categoria'].value_counts()
    for categoria, count in categoria_stats.items():
        print(f"   • {categoria.capitalize()}: {count} eventos")
    
    # Show sample of the data
    print(f"\n📋 Muestra de los datos (primeras 3 filas):")
    print("-" * 80)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 30)
    print(df_demo.head(3).to_string(index=False))
    
    print(f"\n💡 Para ver el archivo completo, abre: {demo_csv_path}")
    
    return demo_csv_path

def show_usage_instructions():
    """Show instructions for using the real scrapper"""
    
    print("\n" + "="*60)
    print("🚀 CÓMO USAR EL SCRAPPER REAL")
    print("="*60)
    print("""
Para usar el scrapper real con el sitio web de La Térmica Málaga:

1️⃣  Instalar dependencias:
   pip install -r requirements.txt

2️⃣  Ejecutar el scrapper:
   python scrapper.py

3️⃣  El scrapper creará 'agenda_termica.csv' con eventos reales

⚠️  NOTA: El scrapper real necesita conexión a internet y puede
   tardar unos minutos en completarse dependiendo de la cantidad
   de eventos disponibles en el sitio web.

🔧 PERSONALIZACIÓN:
   • Modificar base_url en scrapper.py para otros sitios
   • Cambiar csv_path para usar otro nombre de archivo
   • Ajustar las categorías en clasificar_con_mapa()

📖 Para más información, consulta el README.md
""")

if __name__ == "__main__":
    try:
        demo_file = demo_scrapper_functionality()
        show_usage_instructions()
        
        print(f"\n🎉 Demo completado exitosamente!")
        print(f"Archivo creado: {demo_file}")
        
    except Exception as e:
        print(f"❌ Error en el demo: {e}")
        print("Por favor, revisa que todas las dependencias estén instaladas.")