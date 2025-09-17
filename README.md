# 🎭 Scraper Agenda La Térmica Málaga

Un **web scraper en Python** que obtiene automáticamente los eventos publicados en la agenda de [La Térmica Málaga](https://latermicamalaga.com/agenda) y los guarda en un archivo **CSV** para su consulta y análisis.

---

## 🚀 Características

* 📅 Extrae **nombre, categoría, etiquetas, ubicación, fecha y enlace** de cada evento.
* 🗂️ Guarda y actualiza los resultados en `agenda_termica.csv`.
* 🔄 Detecta **eventos nuevos** y los añade al CSV sin duplicar datos.
* 🕵️ Usa **Selenium + BeautifulSoup** para scrapear de manera fiable.
* ⚡ Gestión automática de drivers con `webdriver-manager`.

---

## 🛠️ Requisitos

* Python **3.8+**
* Google Chrome instalado

---

## 📦 Instalación

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/tu-usuario/mi-scraper-termica.git
   cd mi-scraper-termica
   ```

2. Crear un entorno virtual (opcional pero recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / Mac
   venv\Scripts\activate    # Windows
   ```

3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Uso

Ejecuta el script principal:

```bash
python scraper.py
```

* Si no existe `agenda_termica.csv`, se creará con todos los eventos actuales.
* Si ya existe, solo se añadirán los **eventos nuevos** encontrados.

📂 El archivo resultante se guarda en:

```
agenda_termica.csv
```

---

## 📊 Ejemplo de salida (CSV)

```csv
nombre_evento,categoria,ubicacion,enlace_evento,fecha_hora,fecha_resumen,etiquetas
Concierto de Jazz,Música,La Térmica,https://...,20:00 h,2025-09-23,Música
Taller de Fotografía,Talleres,Sala 2,https://...,17:30 h,2025-09-25,Arte
```

---

## 📚 Tecnologías usadas

* 🐍 Python
* 🌐 Selenium
* 🍲 BeautifulSoup
* 📊 pandas
* ⚙️ webdriver-manager
