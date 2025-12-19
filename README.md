# 🎵 Jarama Music

> **Tu plataforma personal de música** - Descarga y reproduce música desde Spotify con una interfaz moderna y elegante.

---

## ✨ Características

### 🎧 Funcionalidades Principales

- **Descarga desde Spotify** - Tracks, álbumes y playlists completas
- **Reproductor Completo** - Control total de reproducción con visualizador de ondas
- **Organización Automática** - Música organizada por artista, álbum o playlist
- **PWA Instalable** - Instala como app nativa en móvil y desktop
- **Diseño Moderno** - Interfaz glassmorphism con gradientes vibrantes
- **Offline Ready** - Service Worker para caché inteligente

### 🎮 Controles del Reproductor

- ▶️ Play/Pause
- ⏭️ Next/Previous Track
- 🔀 Shuffle (reproducción aleatoria)
- 🔁 Repeat (repetir canción)
- 🔊 Control de volumen interactivo
- 📊 Barra de progreso clickeable
- 🎨 Visualizador de ondas circular

---

## 🚀 Instalación

### Requisitos Previos

- Python 3.9+
- FFmpeg (para conversión de audio)
- Credenciales de Spotify API

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/sopotify.git
cd sopotify
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
SPOTIPY_CLIENT_ID=tu_client_id_aqui
SPOTIPY_CLIENT_SECRET=tu_client_secret_aqui
```

> **¿Cómo obtener credenciales de Spotify?**
> 1. Ve a [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
> 2. Crea una nueva aplicación
> 3. Copia el Client ID y Client Secret

### 4. Instalar FFmpeg

#### Windows (con Chocolatey):
```bash
choco install ffmpeg
```

#### macOS (con Homebrew):
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install ffmpeg
```

### 5. Ejecutar la Aplicación

```bash
python app.py
```

Abre tu navegador en: **http://localhost:5000**

---

## 🐳 Docker

### Construir la Imagen

```bash
docker build -t jarama-music .
```

### Ejecutar el Contenedor

```bash
docker run -p 5000:5000 --env-file .env jarama-music
```

---

## 📱 Instalar como PWA

### En Desktop (Chrome/Edge)

1. Abre la aplicación en el navegador
2. Busca el ícono **"Instalar"** en la barra de direcciones
3. O ve a **Menú → Instalar Jarama Music**

### En Android

1. Abre en Chrome
2. Toca **Menú (⋮) → Agregar a pantalla de inicio**

### En iOS

1. Abre en Safari
2. Toca el botón **Compartir**
3. Selecciona **Agregar a pantalla de inicio**

---

## 🎯 Uso

### Descargar Música

1. Copia el enlace de Spotify (track, álbum o playlist)
2. Pégalo en la barra de búsqueda superior
3. Haz clic en **Download**
4. Espera a que se complete la descarga
5. La música aparecerá automáticamente en tu biblioteca

### Reproducir Música

- Haz clic en cualquier canción de la lista o sidebar
- Usa los controles del reproductor en la parte inferior
- Ajusta el volumen con la barra de la derecha
- Haz clic en la barra de progreso para saltar a cualquier parte

---

## 🛠️ Tecnologías

### Backend

| Tecnología | Uso |
|------------|-----|
| **Flask** | Framework web |
| **Spotipy** | Cliente Spotify API |
| **yt-dlp** | Descarga de YouTube |
| **Mutagen** | Metadatos MP3 |
| **Gunicorn** | Servidor WSGI |

### Frontend

| Tecnología | Uso |
|------------|-----|
| **HTML5** | Estructura |
| **CSS3** | Glassmorphism, animaciones |
| **JavaScript** | Lógica del reproductor |
| **Font Awesome** | Iconos |
| **Google Fonts (Inter)** | Tipografía |

### PWA

| Tecnología | Uso |
|------------|-----|
| **Service Worker** | Caché offline |
| **Web App Manifest** | Instalación |
| **Cache API** | Almacenamiento |

---

## 📁 Estructura del Proyecto

```
sopotify/
├── app.py                    # Backend Flask principal
├── spotify_service.py        # Integración Spotify API
├── downloader.py            # Descarga desde YouTube
├── requirements.txt         # Dependencias Python
├── Dockerfile              # Configuración Docker
├── .env                    # Variables de entorno
├── templates/
│   └── index.html          # Interfaz principal
├── static/
│   ├── style.css           # Estilos
│   ├── manifest.json       # PWA manifest
│   ├── sw.js              # Service Worker
│   └── icons/             # Iconos PWA
└── downloads/             # Música descargada
```

---

## 🎨 Diseño

### Paleta de Colores

```css
--primary: #8b5cf6;        /* Violeta */
--accent: #ec4899;         /* Rosa */
--bg-main: #0f172a;        /* Azul oscuro */
--text-main: #f8fafc;      /* Blanco */
```

### Tipografía

- **Font Family:** Inter (Google Fonts)
- **Weights:** 400, 500, 600, 700, 800, 900

---

## 🚢 Despliegue

### Render

1. Crea una nueva Web Service en [Render](https://render.com)
2. Conecta tu repositorio de GitHub
3. Configura las variables de entorno:
   - `SPOTIPY_CLIENT_ID`
   - `SPOTIPY_CLIENT_SECRET`
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn --bind 0.0.0.0:$PORT app:app`

### Heroku

```bash
heroku create jarama-music
heroku config:set SPOTIPY_CLIENT_ID=tu_client_id
heroku config:set SPOTIPY_CLIENT_SECRET=tu_client_secret
git push heroku main
```

---

## 🐛 Troubleshooting

### El Service Worker no se registra

- Verifica que `static/sw.js` existe
- Asegúrate de usar HTTPS (o localhost)
- Revisa la consola del navegador

### Error al descargar música

- Verifica que FFmpeg está instalado: `ffmpeg -version`
- Comprueba las credenciales de Spotify en `.env`
- Revisa los logs en `app.log`

### La aplicación no se puede instalar como PWA

- Verifica que `manifest.json` es válido
- Asegúrate de tener iconos de 192x192 y 512x512
- El Service Worker debe estar activo

---

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 👨‍💻 Autor

**Astuardo**

---

## 🙏 Agradecimientos

- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Flask](https://flask.palletsprojects.com/)
- [Font Awesome](https://fontawesome.com/)

---

## 📞 Soporte

Si tienes problemas o preguntas:

1. Revisa la sección de [Troubleshooting](#-troubleshooting)
2. Consulta la [documentación de PWA](PWA_SETUP_GUIDE.md)
3. Abre un issue en GitHub

---

<div align="center">

**Hecho con ❤️ y mucha música 🎵**

[⬆ Volver arriba](#-jarama-music)

</div>
