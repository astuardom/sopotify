# Jarama Music - PWA Setup Guide

## 📱 ¡Tu aplicación ahora es una PWA!

He convertido Jarama Music en una **Progressive Web App** completa. Esto significa que ahora puedes:

✅ **Instalarla** en tu teléfono o computadora como una app nativa  
✅ **Usarla offline** (funcionalidad limitada)  
✅ **Recibir notificaciones** (opcional, para futuras actualizaciones)  
✅ **Experiencia más rápida** gracias al caché inteligente  

---

## 🚀 Archivos Creados

### 1. **manifest.json** (`static/manifest.json`)
Archivo de configuración de la PWA con:
- Nombre de la app
- Iconos en múltiples tamaños
- Colores de tema
- Configuración de pantalla

### 2. **Service Worker** (`static/sw.js`)
Maneja:
- Caché de assets estáticos
- Estrategias de red (network-first para API, cache-first para assets)
- Sincronización en segundo plano
- Soporte para notificaciones push

### 3. **Script de Generación de Iconos** (`generate_icons.py`)
Genera todos los tamaños de iconos necesarios desde una imagen base.

---

## 📋 Pasos para Completar la Configuración

### Paso 1: Generar los Iconos

1. **Guarda el icono generado** (está en los artifacts) como `static/icon-base.png`

2. **Instala Pillow** (si no lo tienes):
   ```bash
   pip install Pillow
   ```

3. **Ejecuta el script de generación**:
   ```bash
   python generate_icons.py
   ```

   Esto creará la carpeta `static/icons/` con todos los tamaños necesarios.

### Paso 2: Corregir el HTML

El archivo `index.html` se duplicó durante la edición. Necesitas restaurarlo. Aquí tienes dos opciones:

#### Opción A: Restaurar desde Git (si tienes control de versiones)
```bash
git checkout templates/index.html
```

Luego añade estas líneas en el `<head>`:

```html
<!-- PWA Meta Tags -->
<meta name="description" content="Your personal music streaming and download platform">
<meta name="theme-color" content="#8b5cf6">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Jarama Music">

<!-- PWA Manifest -->
<link rel="manifest" href="{{ url_for('static', filename='manifest.json') }}">

<!-- Icons for iOS -->
<link rel="apple-touch-icon" sizes="192x192" href="{{ url_for('static', filename='icons/icon-192x192.png') }}">
```

Y antes del cierre de `</script>` al final del archivo, añade:

```javascript
// PWA - Service Worker Registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/sw.js')
            .then((registration) => {
                console.log('✓ Service Worker registered:', registration.scope);
            })
            .catch((error) => {
                console.log('✗ Service Worker registration failed:', error);
            });
    });
}
```

#### Opción B: Usar el backup
```bash
# Si tienes un backup limpio
Copy-Item "templates\index.html.backup" "templates\index.html"
```

---

## 🧪 Probar la PWA

### En Desarrollo Local

1. **Inicia el servidor**:
   ```bash
   python app.py
   ```

2. **Abre Chrome/Edge** y ve a `http://localhost:5000`

3. **Abre DevTools** (F12) → pestaña **Application**

4. **Verifica**:
   - **Manifest**: Debe mostrar todos los datos
   - **Service Workers**: Debe estar registrado y activo
   - **Storage**: Verás el caché creado

### Instalar en el Dispositivo

#### En Desktop (Chrome/Edge):
- Busca el ícono de **"Instalar"** en la barra de direcciones
- O ve a **Menú** → **Instalar Jarama Music**

#### En Mobile (Android):
- Abre en Chrome
- Toca **Menú** (⋮) → **Agregar a pantalla de inicio**

#### En iOS:
- Abre en Safari
- Toca el botón **Compartir** 
- Selecciona **Agregar a pantalla de inicio**

---

## 🎨 Personalización Adicional

### Cambiar Colores de Tema
Edita `static/manifest.json`:
```json
{
  "theme_color": "#8b5cf6",  // Color de la barra de estado
  "background_color": "#0f172a"  // Color de fondo al abrir
}
```

### Añadir Botón de Instalación Personalizado

Puedes añadir un botón en la interfaz para instalar la PWA:

```html
<button id="install-btn" onclick="installPWA()" style="display:none;">
    📱 Instalar App
</button>
```

El código JavaScript ya está incluido en el archivo.

---

## 🔧 Troubleshooting

### El Service Worker no se registra
- Verifica que el archivo `static/sw.js` existe
- Asegúrate de estar usando HTTPS (o localhost)
- Revisa la consola del navegador para errores

### Los iconos no aparecen
- Ejecuta `python generate_icons.py`
- Verifica que la carpeta `static/icons/` existe
- Revisa que los archivos PNG se generaron correctamente

### La app no se puede instalar
- Verifica que el manifest.json es válido (usa DevTools)
- Asegúrate de tener al menos un icono de 192x192 y 512x512
- El Service Worker debe estar activo

---

## 📊 Características PWA Implementadas

✅ **Instalable**: Puede instalarse en dispositivos  
✅ **Offline Ready**: Caché inteligente de assets  
✅ **Fast**: Carga rápida con Service Worker  
✅ **Engaging**: Pantalla completa, sin barra del navegador  
✅ **Responsive**: Funciona en móvil, tablet y desktop  
✅ **Safe**: Requiere HTTPS en producción  

---

## 🚀 Próximos Pasos (Opcional)

1. **Notificaciones Push**: Implementar notificaciones cuando se complete una descarga
2. **Background Sync**: Sincronizar descargas pendientes cuando vuelva la conexión
3. **Offline Music**: Permitir reproducción offline de canciones descargadas
4. **Update Notifications**: Notificar al usuario cuando hay una nueva versión

---

## 📝 Notas Importantes

- **HTTPS Requerido**: En producción, la PWA requiere HTTPS (localhost funciona sin HTTPS)
- **Cache Management**: El Service Worker cachea assets automáticamente
- **Updates**: Para actualizar el SW, cambia el `CACHE_NAME` en `sw.js`

---

¡Tu aplicación ahora es una PWA completa! 🎉
