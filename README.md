# Gorcelx IA — Generador de Sitio Estático

> Radar semanal y publicación periódica sobre Inteligencia Artificial, Ingeniería de Agentes y Arquitectura de Sistemas de **Gorcelx**.

---

## 📋 Resumen del Proyecto

**Gorcelx IA** es un generador de sitios estáticos escrito en Python nativo (`build.py`) sin dependencias externas pesadas. Procesa automáticamente la edición semanal más reciente dentro de `repositorio/` y genera un sitio estático completo en `dist/index.html` con estética **Luminosa Editorial (Apple / Stripe Light Mode)** y **Glassmorphism**.

---

## 📁 Estructura del Repositorio

```text
gorcelx_ia/
├── build.py                                # Generador estático principal
├── dist/                                   # Sitio web compilado (listo para publicar)
│   ├── index.html                          # HTML + CSS Glassmorphism integrado
│   └── assets/
│       └── images/                         # Imágenes optimizadas de la edición
├── repositorio/
│   └── 2026_semana_36/                     # Edición semanal (detección automática)
│       ├── 01_noticias/                    # Artículos con formato Bento Grid
│       │   ├── *.txt                       # TITULO, RESUMEN, URL, TAG, FECHA
│       │   └── *.jpg                       # Imagen de portada vinculada
│       ├── 02_herramientas/                # Comparativas Premium vs Open Source
│       │   └── *.txt                       # CATEGORIA, LIDER_PREMIUM, EQUIVALENTE_GRATIS...
│       ├── 03_formacion/                   # Roadmap formativo con vídeos
│       │   └── *.txt                       # TITULO, PLATAFORMA, NIVEL, DURACION, URL...
│       ├── 04_skills/                      # Tarjetas de prompts con copiado rápido
│       │   └── *.txt                       # TITULO, CATEGORIA, PROMPT, EJEMPLO_USO...
│       └── 05_patrocinio/                  # Nota editorial de patrocinio
│           └── patrocinador.txt            # Si no existe, genera fallback automático
└── README.md                               # Este documento
```

---

## 🚀 Cómo Compilar el Sitio

Para compilar la versión más reciente del sitio:

```powershell
py build.py
```

El script:
1. Detecta automáticamente la subcarpeta más reciente dentro de `repositorio/` (orden cronológico por nombre).
2. Parsea todos los pares clave-valor de los archivos `.txt` (soportando campos multilínea).
3. Vincula y copia las imágenes asociadas `.jpg` a `dist/assets/images/`.
4. Si un recurso de formación incluye enlace a YouTube, inyecta automáticamente un reproductor nativo `<iframe>` responsive en relación 16:9.
5. Gestiona la lógica de patrocinio (nota de patrocinador o `<div id="carbonads-fallback"></div>`).
6. Genera el bundle estático completo en `dist/index.html`.

---

## 🌐 Cómo Previsualizar Localmente

Puedes abrir directamente el archivo `dist/index.html` en cualquier navegador o lanzar un servidor HTTP local en PowerShell:

```powershell
cd dist
py -m http.server 8000
```
Y acceder en tu navegador a: `http://localhost:8000`.

---

## 🎨 Características de Diseño Implementadas

* **Atmósfera Luminosa**: Fondo `#FBFBFD` enriquecido con gradientes radiales orgánicos difusos en naranja (`#F97316`) y coral cálido (`#FFEDD5`).
* **Glassmorphism**: Superficies de cristal translúcidas (`rgba(255, 255, 255, 0.72)`), desenfoque agresivo (`backdrop-filter: blur(24px)`), bordes hiper-finos y sombras suaves.
* **Regla de 16px**: Todos los contenedores, tarjetas, marcos de imagen, botones e iframes tienen `border-radius: 16px` para evitar el "efecto burbuja".
* **Logo Estático**: Logotipo oficial de Gorcelx sin etiquetas `<a>` envolventes.
* **Above the Fold Desaturado**: El bloque de patrocinio es una nota editorial compacta (`padding: 12px 24px`, fuente `0.9rem`).
* **Franja Panorámica Gorcelx.com**: Ubicada estratégicamente entre Noticias y Herramientas, con altura máxima de 300px y enlace exclusivo a `https://www.gorcelx.com`.
* **YouTube Nativo**: Detección e incrustación de reproductores de YouTube en la ruta de formación.

---

## 📌 Puntos de Continuación para Mañana

1. **Añadir Nuevas Ediciones**: Crear carpetas futuras como `repositorio/2026_semana_37/` para verificar la alternancia de ediciones.
2. **Automatización CI/CD**: Posible configuración de GitHub Actions para compilar y desplegar a GitHub Pages, Cloudflare Pages o Vercel.
3. **RSS / Newsletter Feed**: Generación opcional de un feed RSS/Atom (`feed.xml`) o newsletter markdown a partir de los `.txt` de la semana.
4. **Modo Oscuro Toggle** (Opcional): Si en el futuro se desea alternar entre el modo oscuro y este modo luminoso.
