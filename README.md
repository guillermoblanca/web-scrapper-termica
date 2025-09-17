# Web Scrapper Térmica Málaga

Un web scrapper desarrollado en Python usando Selenium para extraer información de eventos de [La Térmica Málaga](https://latermicamalaga.com/agenda) y guardar los datos en formato CSV.

## 📋 Descripción

Este proyecto automatiza la recolección de información sobre eventos culturales de La Térmica Málaga, incluyendo:
- Nombre del evento
- Categoría automática basada en palabras clave
- Ubicación
- Fecha y hora
- Enlaces a más información
- Clasificación inteligente por tipo de evento (música, teatro, danza, etc.)

## 🛠 Requisitos del Sistema

### Requisitos Previos
- **Python 3.8 o superior**
- **Google Chrome** (última versión recomendada)
- **Git** (para clonar el repositorio)
- **Conexión a Internet** (para descargar dependencias y realizar scraping)

### Sistemas Operativos Compatibles
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu 18.04+, Debian 9+, CentOS 7+)

## 📦 Instalación

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/guillermoblanca/web-scrapper-termica.git
cd web-scrapper-termica
```

### Paso 2: Crear un Entorno Virtual (Recomendado)
```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Verificar la Instalación de Chrome
Asegúrate de que Google Chrome esté instalado en tu sistema:
- **Windows**: Descarga desde [chrome.google.com](https://www.google.com/chrome/)
- **macOS**: Instala usando Homebrew: `brew install --cask google-chrome`
- **Linux**: 
  ```bash
  # Ubuntu/Debian
  wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
  sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
  sudo apt update
  sudo apt install google-chrome-stable
  ```

## 🚀 Uso

### Ejecución Básica
```bash
python scrapper.py
```

### Primera Ejecución
En la primera ejecución, el script:
1. Descargará automáticamente ChromeDriver
2. Accederá a la página de eventos de La Térmica Málaga
3. Extraerá toda la información disponible
4. Creará un archivo `agenda_termica.csv` con todos los eventos

### Ejecuciones Posteriores
En ejecuciones subsiguientes, el script:
- Solo añadirá eventos nuevos al CSV existente
- Evitará duplicados comparando nombre del evento y fecha
- Mostrará cuántos eventos nuevos se añadieron

### Ejemplo de Salida
```
Iniciando web scraping de eventos...
Encontrados 25 eventos
CSV creado con 25 eventos.
Datos guardados en: agenda_termica.csv
```

## 📊 Estructura del CSV de Salida

El archivo `agenda_termica.csv` contiene las siguientes columnas:

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| `nombre_evento` | Nombre completo del evento | "Concierto de Jazz Contemporáneo" |
| `categoria` | Categoría automática asignada | "música" |
| `ubicacion` | Lugar donde se celebra el evento | "Sala de Conciertos" |
| `enlace_evento` | URL con más información | "https://latermicamalaga.com/..." |
| `fecha_hora` | Fecha y hora del evento | "20:30h" |
| `fecha_resumen` | Fecha formateada | "15/12/2024" |
| `fecha_modificado` | Fecha de última actualización | "2024-12-10" |
| `etiquetas` | Categoría original del sitio web | "Música" |

### Categorías Automáticas
El script clasifica automáticamente los eventos en:
- **música**: conciertos, festivales, bandas
- **teatro**: obras, dramas, comedias
- **danza**: ballet, coreografías
- **exposición**: arte, pintura, fotografía
- **conferencia**: charlas, seminarios
- **taller**: workshops, cursos
- **cine**: películas, documentales
- **literatura**: presentaciones de libros, poesía
- **infantil**: eventos para niños y familias
- **otros**: eventos que no encajan en otras categorías

## ⚙️ Configuración Avanzada

### Modificar la URL de Destino
Para cambiar el sitio web objetivo, edita la variable `base_url` en `scrapper.py`:
```python
base_url = "https://tu-sitio-web.com/eventos"
```

### Cambiar el Nombre del Archivo CSV
Modifica la variable `csv_path`:
```python
csv_path = 'mi_archivo_eventos.csv'
```

### Opciones de Chrome
El script incluye opciones predefinidas de Chrome para mayor estabilidad:
- `--headless`: Ejecuta sin interfaz gráfica
- `--incognito`: Modo incógnito
- `--no-sandbox`: Para entornos de servidor
- `--disable-dev-shm-usage`: Optimización de memoria

## 🔧 Solución de Problemas

### Error: ChromeDriver no encontrado
**Problema**: `selenium.common.exceptions.WebDriverException`
**Solución**: 
1. Verifica que Chrome esté instalado
2. Ejecuta: `pip install --upgrade webdriver-manager`

### Error: Elemento no encontrado
**Problema**: `selenium.common.exceptions.NoSuchElementException`
**Solución**: 
1. La estructura del sitio web puede haber cambiado
2. Revisa los selectores CSS en el código
3. Verifica que el sitio web esté accesible

### Error: Permisos denegados
**Problema**: No se puede crear o escribir el archivo CSV
**Solución**:
1. Ejecuta el script como administrador
2. Verifica permisos de escritura en el directorio
3. Cambia la ubicación del archivo CSV

### Problemas de Memoria
**Problema**: El script consume mucha memoria
**Solución**:
1. Cierra otras aplicaciones
2. Usa la opción `--headless` (ya incluida)
3. Procesa eventos en lotes más pequeños

### Conexión Lenta o Timeout
**Problema**: El script se cuelga o es muy lento
**Solución**:
1. Verifica tu conexión a internet
2. Aumenta los tiempos de espera en el código
3. Ejecuta en horarios de menor tráfico

## 📁 Estructura del Proyecto

```
web-scrapper-termica/
├── scrapper.py           # Script principal
├── requirements.txt      # Dependencias de Python
├── README.md            # Esta documentación
├── LICENSE              # Licencia del proyecto
└── agenda_termica.csv   # Archivo de salida (se crea automáticamente)
```

## 🤝 Contribución

### Cómo Contribuir
1. Fork el repositorio
2. Crea una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit tus cambios: `git commit -am 'Añadir nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crea un Pull Request

### Reportar Bugs
1. Abre un Issue en GitHub
2. Incluye información del sistema operativo y versión de Python
3. Proporciona el error completo y pasos para reproducirlo

### Sugerir Mejoras
- Nuevas funcionalidades
- Optimizaciones de rendimiento
- Mejoras en la categorización automática
- Soporte para otros sitios web

## 📈 Roadmap

### Próximas Funcionalidades
- [ ] Filtros por fechas específicas
- [ ] Exportación a otros formatos (JSON, Excel)
- [ ] Interfaz gráfica de usuario
- [ ] Programación de ejecución automática
- [ ] Notificaciones por email de nuevos eventos
- [ ] API REST para consultas
- [ ] Dashboard web con visualizaciones

## 📄 Licencia

Este proyecto está bajo la Licencia Apache 2.0. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Guillermo Blanca**
- GitHub: [@guillermoblanca](https://github.com/guillermoblanca)

## 🙏 Agradecimientos

- [La Térmica Málaga](https://latermicamalaga.com/) por proporcionar la información cultural
- Comunidad de desarrolladores de Selenium y BeautifulSoup
- Contribuidores del proyecto

---

**¿Problemas o preguntas?** Abre un [Issue](https://github.com/guillermoblanca/web-scrapper-termica/issues) en GitHub.
