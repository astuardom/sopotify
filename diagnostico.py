import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 50)
print("DIAGNÓSTICO DE CONFIGURACIÓN")
print("=" * 50)

# Check environment variables
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

print(f"\n1. Variables de Entorno:")
print(f"   SPOTIPY_CLIENT_ID: {'✓ Configurado' if client_id else '✗ NO CONFIGURADO'}")
print(f"   SPOTIPY_CLIENT_SECRET: {'✓ Configurado' if client_secret else '✗ NO CONFIGURADO'}")

if client_id:
    print(f"   Client ID (primeros 10 caracteres): {client_id[:10]}...")

# Check FFmpeg
import subprocess
try:
    result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        version_line = result.stdout.split('\n')[0]
        print(f"\n2. FFmpeg: ✓ Instalado - {version_line}")
    else:
        print(f"\n2. FFmpeg: ✗ Error al ejecutar")
except FileNotFoundError:
    print(f"\n2. FFmpeg: ✗ NO INSTALADO")
except Exception as e:
    print(f"\n2. FFmpeg: ✗ Error - {e}")

# Check directories
downloads_dir = "downloads"
if os.path.exists(downloads_dir):
    files = os.listdir(downloads_dir)
    print(f"\n3. Directorio downloads/: ✓ Existe ({len(files)} archivos)")
else:
    print(f"\n3. Directorio downloads/: ✗ No existe")

# Test Spotify connection
print(f"\n4. Probando conexión con Spotify API...")
if client_id and client_secret:
    try:
        import spotipy
        from spotipy.oauth2 import SpotifyClientCredentials
        
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        ))
        
        # Try to get a test track
        result = sp.track('3n3Ppam7vgaVa1iaRUc9Lp')  # Mr. Brightside by The Killers
        print(f"   ✓ Conexión exitosa con Spotify API")
        print(f"   ✓ Track de prueba obtenido: {result['name']} - {result['artists'][0]['name']}")
    except Exception as e:
        print(f"   ✗ Error al conectar con Spotify: {e}")
else:
    print(f"   ✗ No se puede probar - faltan credenciales")

# Test yt-dlp
print(f"\n5. Probando yt-dlp...")
try:
    import yt_dlp
    print(f"   ✓ yt-dlp instalado correctamente")
except Exception as e:
    print(f"   ✗ Error con yt-dlp: {e}")

print("\n" + "=" * 50)
print("FIN DEL DIAGNÓSTICO")
print("=" * 50)
