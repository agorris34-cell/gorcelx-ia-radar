#!/usr/bin/env python3
"""
GORCELX IA - Generador de Sitio Estático
Estética 'Luminosa Editorial' (Apple/Stripe Light Mode) con Glassmorphism Refinado
Auditoría UX/UI: Retención Above the Fold, Reproductores de YouTube Nativos y Franja Gorcelx.com
"""

import os
import sys
import re
import html
import shutil
from pathlib import Path

# Asegurar compatibilidad UTF-8 en consola de Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ==============================================================================
# CONFIGURACIÓN DE MARCA Y ASSETS EXTERNOS
# ==============================================================================
# Logotipo oficial extraído de gorcelx.com (estático en navbar, sin enlaces)
GORCELX_LOGO_URL = "https://gorcelx.com/brand/gorcelx-logo-mark.png"

# Imagen de fondo en alta resolución para la franja promocional de Gorcelx.com
GORCELX_BANNER_IMG_URL = "https://gorcelx.com/tour/etapa-1-registro.jpg"

# Enlace de destino exclusivo para Gorcelx.com
GORCELX_PROMO_URL = "https://www.gorcelx.com"

ROOT_DIR = Path(__file__).resolve().parent
REPO_DIR = ROOT_DIR / "repositorio"
DIST_DIR = ROOT_DIR / "dist"
ASSETS_DIR = DIST_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"


def find_latest_week_dir(repo_dir: Path) -> Path:
    """Encuentra la carpeta de semana más reciente dentro de repositorio/"""
    if not repo_dir.exists():
        raise FileNotFoundError(f"No se encontró el directorio del repositorio: {repo_dir}")

    subdirs = [p for p in repo_dir.iterdir() if p.is_dir() and not p.name.startswith(".")]
    if not subdirs:
        raise ValueError(f"No se encontraron ediciones semanales en: {repo_dir}")

    subdirs.sort(key=lambda p: p.name)
    return subdirs[-1]


def parse_txt_file(filepath: Path) -> dict:
    """Extrae las variables clave-valor de un archivo .txt con soporte multilínea."""
    data = {"_filename": filepath.name, "_stem": filepath.stem}
    current_key = None
    current_val_lines = []

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            match = re.match(r"^([A-Za-z0-9_]+)\s*:\s*(.*)$", line)
            if match:
                if current_key:
                    data[current_key] = "\n".join(current_val_lines).strip()
                current_key = match.group(1).upper()
                current_val_lines = [match.group(2)]
            elif current_key:
                current_val_lines.append(line.rstrip("\r\n"))

    if current_key:
        data[current_key] = "\n".join(current_val_lines).strip()

    for k, v in list(data.items()):
        if isinstance(v, str) and "\\n" in v:
            data[k] = v.replace("\\n", "\n")

    return data


def find_associated_image(txt_path: Path) -> Path | None:
    """Busca una imagen .jpg/.jpeg/.png con el mismo nombre base que el archivo .txt"""
    parent = txt_path.parent
    stem = txt_path.stem
    for ext in [".jpg", ".jpeg", ".png", ".webp"]:
        candidate = parent / f"{stem}{ext}"
        if candidate.exists():
            return candidate
    return None


def copy_image_to_dist(src_path: Path | None, prefix: str = "") -> str | None:
    """Copia la imagen a dist/assets/images/ y retorna su ruta relativa web."""
    if not src_path or not src_path.exists():
        return None
    dest_filename = f"{prefix}_{src_path.name}" if prefix else src_path.name
    dest_path = IMAGES_DIR / dest_filename
    shutil.copy2(src_path, dest_path)
    return f"assets/images/{dest_filename}"


def escape(text: str | None) -> str:
    """Escapa texto HTML de forma segura."""
    return html.escape(str(text or ""))


def extract_youtube_id(url: str | None) -> str | None:
    """
    Detecta si la URL corresponde a YouTube y extrae su ID de vídeo.
    Soporta formatos estándar: youtube.com/watch?v=..., youtu.be/..., embed/...
    """
    if not url:
        return None
    if "youtube.com" not in url and "youtu.be" not in url:
        return None

    patterns = [
        r"(?:v=|vi=|\/v\/|\/vi\/|\/embed\/|\/shorts\/)([a-zA-Z0-9_-]{11})",
        r"youtu\.be\/([a-zA-Z0-9_-]{11})",
        r"[?&]v=([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        m = re.search(pattern, url)
        if m:
            return m.group(1)
    return None


def get_css() -> str:
    """
    CSS 'Luminosa Editorial' con Glassmorphism Refinado:
    - Border-radius unificado a 16px en todas las tarjetas, botones, marcos e iframes (adiós efecto burbuja)
    - Padding interno reducido en Bento Grid para máximo protagonismo de las imágenes
    - Banner de Patrocinador desaturado y compacto (nota del editor Above the Fold)
    - Franja horizontal panorámica para Gorcelx.com (máx. 300px)
    - Reproductor responsive de YouTube (16:9 con border-radius 16px)
    """
    return """
        :root {
            /* Atmósfera Luminosa Base (Apple/Stripe Light Mode) */
            --bg-luminosa: #FBFBFD;
            --bg-glass: rgba(255, 255, 255, 0.65);
            --bg-glass-card: rgba(255, 255, 255, 0.72);
            --bg-glass-hover: rgba(255, 255, 255, 0.90);
            --bg-glass-nav: rgba(251, 251, 253, 0.82);
            --bg-code-terminal: #0f172a;

            /* Bordes de Cristal y Separadores */
            --border-glass: rgba(255, 255, 255, 0.85);
            --border-glass-subtle: rgba(226, 232, 240, 0.75);
            --border-orange-glow: rgba(249, 115, 22, 0.35);

            /* Tipografía Táctil (Negro Asfalto & Gris Marengo) */
            --text-asphalt: #0f172a;
            --text-charcoal: #1e293b;
            --text-secondary: #475569;
            --text-muted: #64748b;
            --text-faint: #94a3b8;

            /* Colores Corporativos Gorcelx */
            --gorcelx-orange: #f97316;
            --gorcelx-coral: #ea580c;
            --gorcelx-warm-light: #ffedd5;
            --gradient-fire: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
            --gradient-fire-text: linear-gradient(135deg, #ea580c 0%, #f97316 60%, #c2410c 100%);

            /* Acentos */
            --accent-emerald: #059669;
            --accent-emerald-bg: rgba(16, 185, 129, 0.10);
            --accent-rose: #e11d48;
            --accent-rose-bg: rgba(244, 63, 94, 0.08);

            /* Tipografía */
            --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

            /* Sombras Amplias de Cristal */
            --shadow-glass: 0 24px 48px rgba(0, 0, 0, 0.04), 0 4px 16px rgba(0, 0, 0, 0.02);
            --shadow-glass-hover: 0 32px 64px rgba(0, 0, 0, 0.07), 0 6px 20px rgba(249, 115, 22, 0.08);
            --shadow-strip: 0 20px 50px rgba(15, 23, 42, 0.10);
            --shadow-button: 0 4px 14px rgba(249, 115, 22, 0.35);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            background-color: var(--bg-luminosa);
            color: var(--text-asphalt);
            font-family: var(--font-sans);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 12% 8%, rgba(249, 115, 22, 0.14) 0%, transparent 48%),
                radial-gradient(circle at 88% 16%, rgba(255, 237, 213, 0.65) 0%, transparent 45%),
                radial-gradient(circle at 50% 45%, rgba(249, 115, 22, 0.06) 0%, transparent 55%),
                radial-gradient(circle at 18% 75%, rgba(255, 237, 213, 0.50) 0%, transparent 42%),
                radial-gradient(circle at 82% 88%, rgba(249, 115, 22, 0.10) 0%, transparent 45%);
            background-attachment: fixed;
        }

        a {
            color: var(--gorcelx-coral);
            text-decoration: none;
            transition: all 0.2s ease;
        }

        a:hover {
            color: var(--gorcelx-orange);
        }

        .container {
            max-width: 1240px;
            margin: 0 auto;
            padding: 0 1.75rem;
        }

        /* ==========================================================================
           HEADER / NAVBAR (EL LOGO NO CONTIENE ENLACE <a>)
           ========================================================================== */
        header.site-header {
            padding: 1.1rem 0;
            border-bottom: 1px solid var(--border-glass);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            position: sticky;
            top: 0;
            z-index: 100;
            background: var(--bg-glass-nav);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.025);
        }

        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1.5rem;
        }

        /* Contenedor estático del logo: sin enlaces <a> */
        .brand-identity {
            display: inline-flex;
            align-items: center;
            gap: 0.85rem;
            user-select: none;
            cursor: default;
        }

        .brand-logo-img {
            height: 34px;
            width: 34px;
            object-fit: contain;
            filter: drop-shadow(0 2px 8px rgba(249, 115, 22, 0.35));
            pointer-events: none;
        }

        .brand-text {
            font-size: 1.22rem;
            font-weight: 900;
            letter-spacing: -0.03em;
            color: var(--text-asphalt);
            display: flex;
            align-items: center;
            gap: 0.45rem;
        }

        .brand-ia-badge {
            background: var(--gradient-fire);
            color: #ffffff;
            font-size: 0.65rem;
            font-weight: 900;
            padding: 0.15rem 0.5rem;
            border-radius: 6px;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            box-shadow: 0 2px 6px rgba(249, 115, 22, 0.3);
        }

        .edition-badge {
            background: rgba(249, 115, 22, 0.08);
            color: var(--gorcelx-coral);
            border: 1px solid rgba(249, 115, 22, 0.22);
            font-size: 0.72rem;
            font-family: var(--font-mono);
            font-weight: 700;
            padding: 0.25rem 0.75rem;
            border-radius: 16px;
            letter-spacing: 0.04em;
        }

        nav.nav-links {
            display: flex;
            align-items: center;
            gap: 1.75rem;
        }

        nav.nav-links a {
            color: var(--text-secondary);
            font-size: 0.88rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }

        nav.nav-links a:hover {
            color: var(--gorcelx-coral);
        }

        /* ==========================================================================
           HERO SECTION
           ========================================================================== */
        .hero-section {
            padding: 4rem 0 1.75rem 0;
            text-align: center;
            position: relative;
        }

        .hero-pill-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.55rem;
            background: rgba(255, 255, 255, 0.85);
            border: 1px solid var(--border-glass-subtle);
            padding: 0.35rem 0.95rem;
            border-radius: 16px;
            margin-bottom: 1.35rem;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03);
            backdrop-filter: blur(12px);
        }

        .hero-pill-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--gorcelx-orange);
            box-shadow: 0 0 10px var(--gorcelx-orange);
        }

        .hero-pill-text {
            font-size: 0.78rem;
            color: var(--text-secondary);
            font-weight: 600;
            letter-spacing: 0.02em;
        }

        .hero-title {
            font-size: clamp(2.2rem, 5vw, 3.8rem);
            font-weight: 900;
            letter-spacing: -0.045em;
            line-height: 1.1;
            margin-bottom: 1rem;
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
            color: var(--text-asphalt);
        }

        .hero-title .fire-gradient-text {
            background: var(--gradient-fire-text);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
        }

        .hero-desc {
            color: var(--text-secondary);
            font-size: 1.12rem;
            max-width: 650px;
            margin: 0 auto;
            line-height: 1.6;
            font-weight: 400;
        }

        /* ==========================================================================
           DESATURACIÓN ABOVE THE FOLD: PATROCINADOR COMPACTO (NOTA DEL EDITOR)
           Padding: 12px 24px, font-size: 0.9rem, botón pequeño
           ========================================================================== */
        .sponsor-box {
            background: rgba(255, 255, 255, 0.75);
            border: 1px solid var(--border-glass-subtle);
            border-left: 3px solid var(--gorcelx-orange);
            border-radius: 16px;
            padding: 12px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1.25rem;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.02);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            margin: 1.5rem auto 2.5rem auto;
            max-width: 1000px;
            font-size: 0.9rem;
            transition: all 0.2s ease;
        }

        .sponsor-box:hover {
            background: rgba(255, 255, 255, 0.92);
            border-color: rgba(249, 115, 22, 0.4);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.04);
        }

        .sponsor-note-body {
            display: flex;
            align-items: baseline;
            gap: 0.75rem;
            flex-wrap: wrap;
            line-height: 1.45;
        }

        .sponsor-note-tag {
            font-size: 0.68rem;
            font-family: var(--font-mono);
            font-weight: 800;
            color: var(--gorcelx-coral);
            text-transform: uppercase;
            letter-spacing: 0.06em;
            background: rgba(249, 115, 22, 0.1);
            padding: 0.15rem 0.5rem;
            border-radius: 6px;
            white-space: nowrap;
        }

        .sponsor-note-copy {
            color: var(--text-secondary);
            font-size: 0.88rem;
        }

        .sponsor-note-copy strong {
            color: var(--text-asphalt);
            font-weight: 700;
        }

        .btn-sponsor-mini {
            background: var(--gradient-fire);
            color: #ffffff;
            font-weight: 700;
            font-size: 0.78rem;
            padding: 0.4rem 0.95rem;
            border-radius: 16px;
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            white-space: nowrap;
            box-shadow: 0 2px 8px rgba(234, 88, 12, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.3);
            transition: all 0.2s ease;
        }

        .btn-sponsor-mini:hover {
            color: #ffffff;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(234, 88, 12, 0.45);
        }

        #carbonads-fallback {
            min-height: 0px;
            display: block;
        }

        /* ==========================================================================
           SECCIONES COMUNES
           ========================================================================== */
        section {
            padding: 3.25rem 0;
        }

        .section-header {
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            border-bottom: 1px solid var(--border-glass-subtle);
            padding-bottom: 0.85rem;
        }

        .section-title {
            font-size: 1.55rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            color: var(--text-asphalt);
        }

        .section-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--gorcelx-orange);
            box-shadow: 0 0 10px var(--gorcelx-orange);
        }

        .section-subtitle {
            color: var(--text-muted);
            font-size: 0.78rem;
            font-family: var(--font-mono);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        /* ==========================================================================
           BENTO GRID (MÁS PROTAGONISMO A LAS IMÁGENES & PADDING REDUCIDO)
           border-radius: 16px en tarjetas e imágenes
           ========================================================================== */
        .bento-grid {
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            gap: 1.5rem;
        }

        .bento-card {
            background: var(--bg-glass-card);
            border: 1px solid var(--border-glass);
            border-radius: 16px;
            overflow: hidden;
            position: relative;
            display: flex;
            flex-direction: column;
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            box-shadow: var(--shadow-glass);
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .bento-card:hover {
            background: var(--bg-glass-hover);
            transform: translateY(-4px);
            border-color: rgba(249, 115, 22, 0.35);
            box-shadow: var(--shadow-glass-hover);
        }

        .bento-card.featured {
            grid-column: span 7;
        }

        .bento-card.secondary {
            grid-column: span 5;
        }

        .bento-card.tertiary {
            grid-column: span 12;
            display: grid;
            grid-template-columns: 420px 1fr;
        }

        /* Imágenes con mayor escala y protagonismo */
        .bento-img-frame {
            position: relative;
            overflow: hidden;
            background: #f1f5f9;
            width: 100%;
            height: 260px;
        }

        .bento-card.featured .bento-img-frame {
            height: 310px;
        }

        .bento-card.tertiary .bento-img-frame {
            height: 100%;
            min-height: 240px;
        }

        .bento-img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .bento-card:hover .bento-img {
            transform: scale(1.04);
        }

        /* Padding reducido para optimizar protagonismo visual */
        .bento-content {
            padding: 1.25rem 1.45rem 1.45rem 1.45rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            flex-grow: 1;
        }

        .bento-meta {
            display: flex;
            align-items: center;
            gap: 0.65rem;
        }

        .tag-pill {
            font-size: 0.68rem;
            font-family: var(--font-mono);
            font-weight: 800;
            text-transform: uppercase;
            padding: 0.2rem 0.55rem;
            border-radius: 6px;
            background: rgba(249, 115, 22, 0.12);
            color: var(--gorcelx-coral);
            border: 1px solid rgba(249, 115, 22, 0.25);
            letter-spacing: 0.05em;
        }

        .card-date {
            color: var(--text-muted);
            font-size: 0.76rem;
            font-family: var(--font-mono);
        }

        .bento-title {
            font-size: 1.25rem;
            font-weight: 800;
            color: var(--text-asphalt);
            line-height: 1.3;
            letter-spacing: -0.02em;
        }

        .bento-card.featured .bento-title {
            font-size: 1.48rem;
        }

        .bento-desc {
            color: var(--text-secondary);
            font-size: 0.91rem;
            line-height: 1.58;
            flex-grow: 1;
        }

        .bento-link {
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--gorcelx-coral);
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            margin-top: 0.4rem;
            width: fit-content;
        }

        .bento-link svg {
            transition: transform 0.25s ease;
        }

        .bento-card:hover .bento-link svg {
            transform: translateX(4px);
        }

        /* ==========================================================================
           REUBICACIÓN DEL BANNER GORCELX: FRANJA HORIZONTAL PANORÁMICA
           Insertada entre Noticias y Herramientas. Máx. 300px de altura.
           ========================================================================== */
        .gorcelx-strip-section {
            padding: 2.5rem 0;
        }

        .gorcelx-strip-banner {
            position: relative;
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.85);
            box-shadow: var(--shadow-strip);
            min-height: 220px;
            max-height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            background: #0f172a;
        }

        .gorcelx-strip-bg {
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center;
            filter: contrast(1.05) brightness(0.65);
            transition: transform 0.8s ease;
            z-index: 1;
        }

        .gorcelx-strip-banner:hover .gorcelx-strip-bg {
            transform: scale(1.03);
        }

        .gorcelx-strip-overlay {
            position: absolute;
            inset: 0;
            background: linear-gradient(
                90deg,
                rgba(15, 23, 42, 0.82) 0%,
                rgba(15, 23, 42, 0.65) 50%,
                rgba(15, 23, 42, 0.82) 100%
            );
            backdrop-filter: blur(2px);
            z-index: 2;
            pointer-events: none;
        }

        .gorcelx-strip-content {
            position: relative;
            z-index: 3;
            padding: 2rem 2.5rem;
            max-width: 860px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.85rem;
        }

        .gorcelx-strip-badge {
            font-size: 0.7rem;
            font-family: var(--font-mono);
            font-weight: 800;
            color: #fed7aa;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            background: rgba(249, 115, 22, 0.2);
            border: 1px solid rgba(249, 115, 22, 0.4);
            padding: 0.2rem 0.65rem;
            border-radius: 16px;
        }

        .gorcelx-strip-title {
            font-size: clamp(1.4rem, 3.2vw, 2.1rem);
            font-weight: 900;
            color: #ffffff;
            letter-spacing: -0.03em;
            line-height: 1.2;
            text-shadow: 0 2px 12px rgba(0, 0, 0, 0.4);
        }

        .gorcelx-strip-desc {
            font-size: 0.95rem;
            color: #cbd5e1;
            max-width: 680px;
            line-height: 1.5;
        }

        .btn-gorcelx-strip {
            background: var(--gradient-fire);
            color: #ffffff;
            font-weight: 800;
            font-size: 0.9rem;
            padding: 0.75rem 1.6rem;
            border-radius: 16px;
            display: inline-flex;
            align-items: center;
            gap: 0.55rem;
            border: 1px solid rgba(255, 255, 255, 0.35);
            box-shadow: 0 4px 16px rgba(234, 88, 12, 0.4);
            transition: all 0.2s ease;
            margin-top: 0.25rem;
        }

        .btn-gorcelx-strip:hover {
            color: #ffffff;
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(234, 88, 12, 0.55);
            filter: brightness(1.06);
        }

        /* ==========================================================================
           TABLA DE HERRAMIENTAS (GLASSMORPHISM // BORDER-RADIUS: 16PX)
           ========================================================================== */
        .table-container {
            background: var(--bg-glass-card);
            border: 1px solid var(--border-glass);
            border-radius: 16px;
            overflow: hidden;
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            box-shadow: var(--shadow-glass);
        }

        .responsive-table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }

        .responsive-table th {
            background: rgba(248, 250, 252, 0.75);
            padding: 1.15rem 1.6rem;
            font-size: 0.75rem;
            font-family: var(--font-mono);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
            border-bottom: 1px solid var(--border-glass-subtle);
            font-weight: 700;
        }

        .responsive-table td {
            padding: 1.35rem 1.6rem;
            border-bottom: 1px solid var(--border-glass-subtle);
            vertical-align: top;
            font-size: 0.92rem;
            transition: background 0.15s ease;
        }

        .responsive-table tr:last-child td {
            border-bottom: none;
        }

        .responsive-table tr:hover td {
            background: rgba(255, 255, 255, 0.85);
        }

        .tool-category {
            font-weight: 800;
            color: var(--text-asphalt);
            display: flex;
            align-items: center;
            gap: 0.65rem;
            font-size: 0.95rem;
        }

        .tool-category::before {
            content: "";
            display: inline-block;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--gorcelx-orange);
            box-shadow: 0 0 8px var(--gorcelx-orange);
        }

        .badge-premium {
            background: var(--accent-rose-bg);
            color: var(--accent-rose);
            border: 1px solid rgba(244, 63, 94, 0.22);
            font-size: 0.68rem;
            font-family: var(--font-mono);
            font-weight: 800;
            padding: 0.2rem 0.55rem;
            border-radius: 6px;
            display: inline-block;
            margin-bottom: 0.35rem;
        }

        .badge-free {
            background: var(--accent-emerald-bg);
            color: var(--accent-emerald);
            border: 1px solid rgba(16, 185, 129, 0.25);
            font-size: 0.68rem;
            font-family: var(--font-mono);
            font-weight: 800;
            padding: 0.2rem 0.55rem;
            border-radius: 6px;
            display: inline-block;
            margin-bottom: 0.35rem;
        }

        .tool-name {
            font-weight: 700;
            color: var(--text-asphalt);
            display: block;
        }

        .tool-name a {
            color: var(--text-asphalt);
        }

        .tool-name a:hover {
            color: var(--gorcelx-coral);
        }

        .tool-detail-desc {
            color: var(--text-secondary);
            font-size: 0.88rem;
            margin-bottom: 0.4rem;
            line-height: 1.55;
        }

        .tool-free-advantage {
            color: var(--accent-emerald);
            font-size: 0.8rem;
            font-weight: 600;
        }

        /* ==========================================================================
           RUTA DE FORMACIÓN VISUAL (ROADMAP // BORDER-RADIUS: 16PX)
           ========================================================================== */
        .roadmap-container {
            position: relative;
            padding-left: 3.8rem;
            margin-top: 1rem;
        }

        .roadmap-container::before {
            content: "";
            position: absolute;
            left: 1.55rem;
            top: 2rem;
            bottom: 2.5rem;
            width: 2px;
            background: linear-gradient(
                180deg,
                var(--gorcelx-orange) 0%,
                rgba(249, 115, 22, 0.35) 60%,
                rgba(226, 232, 240, 0.75) 100%
            );
        }

        .roadmap-step {
            position: relative;
            margin-bottom: 2.25rem;
        }

        .roadmap-step:last-child {
            margin-bottom: 0;
        }

        .roadmap-node {
            position: absolute;
            left: -3.8rem;
            top: 1.5rem;
            width: 3.1rem;
            height: 3.1rem;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.95);
            border: 2px solid var(--gorcelx-orange);
            box-shadow: 0 0 16px rgba(249, 115, 22, 0.3), 0 4px 10px rgba(0, 0, 0, 0.05);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 5;
            backdrop-filter: blur(12px);
        }

        .roadmap-node-num {
            font-family: var(--font-mono);
            font-size: 0.92rem;
            font-weight: 900;
            color: var(--gorcelx-coral);
        }

        .roadmap-card {
            background: var(--bg-glass-card);
            border: 1px solid var(--border-glass);
            border-radius: 16px;
            padding: 1.85rem 2.2rem;
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            box-shadow: var(--shadow-glass);
            transition: all 0.25s ease;
            display: flex;
            flex-direction: column;
            gap: 0.85rem;
        }

        .roadmap-card:hover {
            background: var(--bg-glass-hover);
            border-color: rgba(249, 115, 22, 0.35);
            transform: translateX(4px);
            box-shadow: var(--shadow-glass-hover);
        }

        .roadmap-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.75rem;
        }

        .roadmap-phase {
            display: flex;
            align-items: center;
            gap: 0.65rem;
        }

        .roadmap-phase-label {
            font-size: 0.7rem;
            font-family: var(--font-mono);
            font-weight: 800;
            color: var(--gorcelx-coral);
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .platform-tag {
            font-size: 0.76rem;
            color: var(--text-muted);
            font-family: var(--font-mono);
            font-weight: 600;
        }

        .level-badge {
            font-size: 0.72rem;
            font-family: var(--font-mono);
            font-weight: 700;
            background: rgba(248, 250, 252, 0.9);
            border: 1px solid var(--border-glass-subtle);
            color: var(--text-secondary);
            padding: 0.25rem 0.65rem;
            border-radius: 16px;
        }

        .roadmap-title {
            font-size: 1.3rem;
            font-weight: 800;
            color: var(--text-asphalt);
            letter-spacing: -0.025em;
            line-height: 1.35;
        }

        .roadmap-desc {
            font-size: 0.93rem;
            color: var(--text-secondary);
            line-height: 1.6;
        }

        /* REPRODUCTOR YOUTUBE NATIVO RESPONSIVE (16/9, BORDER-RADIUS: 16PX) */
        .youtube-player-container {
            width: 100%;
            margin-top: 0.85rem;
        }

        .youtube-embed {
            aspect-ratio: 16 / 9;
            width: 100%;
            border: none;
            border-radius: 16px;
            display: block;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.08);
            background: #000000;
        }

        .roadmap-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 1rem;
            border-top: 1px solid var(--border-glass-subtle);
            margin-top: 0.35rem;
        }

        .duration-text {
            font-size: 0.82rem;
            font-family: var(--font-mono);
            color: var(--text-muted);
            font-weight: 600;
        }

        .btn-roadmap {
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--gorcelx-coral);
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.45rem 1rem;
            border-radius: 16px;
            border: 1px solid rgba(234, 88, 12, 0.25);
            background: rgba(249, 115, 22, 0.08);
            transition: all 0.2s ease;
        }

        .btn-roadmap:hover {
            color: #ffffff;
            background: var(--gradient-fire);
            border-color: transparent;
        }

        /* ==========================================================================
           SKILLS (PROMPT CARDS // BORDER-RADIUS: 16PX)
           ========================================================================== */
        .skills-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
            gap: 1.5rem;
        }

        .skill-card {
            background: var(--bg-glass-card);
            border: 1px solid var(--border-glass);
            border-radius: 16px;
            padding: 1.85rem;
            display: flex;
            flex-direction: column;
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            box-shadow: var(--shadow-glass);
            transition: all 0.25s ease;
        }

        .skill-card:hover {
            background: var(--bg-glass-hover);
            border-color: rgba(249, 115, 22, 0.35);
            transform: translateY(-4px);
            box-shadow: var(--shadow-glass-hover);
        }

        .skill-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.85rem;
        }

        .skill-cat {
            font-size: 0.72rem;
            font-family: var(--font-mono);
            font-weight: 800;
            color: var(--gorcelx-coral);
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .skill-title {
            font-size: 1.2rem;
            font-weight: 800;
            color: var(--text-asphalt);
            margin-bottom: 0.55rem;
            letter-spacing: -0.02em;
        }

        .skill-desc {
            color: var(--text-secondary);
            font-size: 0.9rem;
            line-height: 1.58;
            margin-bottom: 1.15rem;
        }

        .prompt-container {
            background: var(--bg-code-terminal);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 1.1rem;
            position: relative;
            margin-bottom: 1rem;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.15);
        }

        .prompt-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.75rem;
        }

        .prompt-label {
            font-size: 0.68rem;
            font-family: var(--font-mono);
            font-weight: 700;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .btn-copy {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #f1f5f9;
            padding: 0.3rem 0.8rem;
            border-radius: 16px;
            font-size: 0.75rem;
            font-family: var(--font-mono);
            font-weight: 700;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            transition: all 0.2s ease;
        }

        .btn-copy:hover {
            background: rgba(255, 255, 255, 0.2);
            color: #ffffff;
        }

        .btn-copy.copied {
            background: rgba(16, 185, 129, 0.25);
            color: #34d399;
            border-color: rgba(16, 185, 129, 0.5);
        }

        .prompt-text {
            font-family: var(--font-mono);
            font-size: 0.82rem;
            color: #e2e8f0;
            white-space: pre-wrap;
            word-break: break-word;
            max-height: 180px;
            overflow-y: auto;
            line-height: 1.55;
            padding-right: 0.5rem;
        }

        .prompt-text::-webkit-scrollbar {
            width: 4px;
        }
        .prompt-text::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 4px;
        }

        .skill-example {
            font-size: 0.82rem;
            color: var(--text-muted);
            border-left: 2px solid var(--gorcelx-orange);
            padding-left: 0.85rem;
            margin-top: auto;
            line-height: 1.5;
        }

        /* ==========================================================================
           FOOTER (BORDER-RADIUS: 16PX)
           ========================================================================== */
        footer.site-footer {
            border-top: 1px solid var(--border-glass-subtle);
            padding: 3.5rem 0;
            margin-top: 5rem;
            text-align: center;
            color: var(--text-muted);
            font-size: 0.88rem;
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(16px);
        }

        .footer-brand {
            display: inline-flex;
            align-items: center;
            gap: 0.65rem;
            margin-bottom: 0.75rem;
        }

        .footer-logo-img {
            width: 24px;
            height: 24px;
            object-fit: contain;
        }

        .footer-brand-text {
            font-weight: 900;
            color: var(--text-asphalt);
            font-size: 1.05rem;
        }

        /* ==========================================================================
           RESPONSIVIDAD
           ========================================================================== */
        @media (max-width: 900px) {
            .bento-card.featured,
            .bento-card.secondary,
            .bento-card.tertiary {
                grid-column: span 12;
            }
            .bento-card.tertiary {
                grid-template-columns: 1fr;
            }
            .gorcelx-strip-content {
                padding: 1.75rem 1.25rem;
            }
            .sponsor-box {
                flex-direction: column;
                align-items: flex-start;
                gap: 0.85rem;
                padding: 14px 18px;
            }
            .roadmap-container {
                padding-left: 2.75rem;
            }
            .roadmap-container::before {
                left: 1.15rem;
            }
            .roadmap-node {
                left: -2.75rem;
                width: 2.4rem;
                height: 2.4rem;
            }
            .roadmap-node-num {
                font-size: 0.78rem;
            }
            nav.nav-links {
                display: none;
            }
        }
    """


def render_noticias(noticias: list[dict]) -> str:
    """
    Renderiza las noticias en un Bento Grid con Glassmorphism luminoso:
    Superficies de cristal blanco translúcido y mayor escala en las imágenes.
    """
    if not noticias:
        return "<p class='empty-msg'>No hay noticias en esta edición.</p>"

    html_parts = ['<div class="bento-grid">']
    for idx, item in enumerate(noticias):
        if idx == 0:
            layout_cls = "bento-card featured"
        elif idx == 1:
            layout_cls = "bento-card secondary"
        elif idx == 2:
            layout_cls = "bento-card secondary"
        else:
            layout_cls = "bento-card tertiary"

        web_img = item.get("_web_image", "")
        img_markup = ""
        if web_img:
            img_markup = f"""
                <div class="bento-img-frame">
                    <img src="{escape(web_img)}" alt="{escape(item.get('TITULO'))}" class="bento-img" loading="lazy">
                </div>
            """

        tag_text = item.get("TAG") or item.get("CATEGORIA") or "NOTICIA"
        date_text = item.get("FECHA", "")
        title_text = item.get("TITULO", "Sin título")
        resumen_text = item.get("RESUMEN", "")
        url_text = item.get("URL", "#")

        html_parts.append(f"""
            <article class="{layout_cls}">
                {img_markup}
                <div class="bento-content">
                    <div class="bento-meta">
                        <span class="tag-pill">{escape(tag_text)}</span>
                        {f'<span class="card-date">{escape(date_text)}</span>' if date_text else ''}
                    </div>
                    <h3 class="bento-title">{escape(title_text)}</h3>
                    <p class="bento-desc">{escape(resumen_text)}</p>
                    <a href="{escape(url_text)}" target="_blank" rel="noopener noreferrer" class="bento-link">
                        <span>Leer artículo completo</span>
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="5" y1="12" x2="19" y2="12"></line>
                            <polyline points="12 5 19 12 12 19"></polyline>
                        </svg>
                    </a>
                </div>
            </article>
        """)

    html_parts.append("</div>")
    return "\n".join(html_parts)


def render_herramientas(herramientas: list[dict]) -> str:
    """Renderiza las herramientas en una tabla comparativa con Glassmorphism."""
    if not herramientas:
        return "<p class='empty-msg'>No hay herramientas registradas en esta edición.</p>"

    rows = []
    for item in herramientas:
        cat = item.get("CATEGORIA", "General")
        lider = item.get("LIDER_PREMIUM", "N/A")
        url_prem = item.get("URL_PREMIUM", "")
        gratis = item.get("EQUIVALENTE_GRATIS", "N/A")
        url_grat = item.get("URL_GRATIS", "")
        desc = item.get("DESCRIPCION", "")
        ventaja = item.get("VENTAJA_GRATIS", "")

        lider_html = f'<a href="{escape(url_prem)}" target="_blank" rel="noopener">{escape(lider)}</a>' if url_prem else escape(lider)
        gratis_html = f'<a href="{escape(url_grat)}" target="_blank" rel="noopener">{escape(gratis)}</a>' if url_grat else escape(gratis)
        ventaja_html = f'<div class="tool-free-advantage">✦ {escape(ventaja)}</div>' if ventaja else ""

        rows.append(f"""
            <tr>
                <td>
                    <div class="tool-category">{escape(cat)}</div>
                </td>
                <td>
                    <span class="badge-premium">PREMIUM</span>
                    <span class="tool-name">{lider_html}</span>
                </td>
                <td>
                    <span class="badge-free">OPEN SOURCE</span>
                    <span class="tool-name">{gratis_html}</span>
                    {ventaja_html}
                </td>
                <td>
                    <div class="tool-detail-desc">{escape(desc)}</div>
                </td>
            </tr>
        """)

    return f"""
        <div class="table-container">
            <div style="overflow-x: auto;">
                <table class="responsive-table">
                    <thead>
                        <tr>
                            <th style="width: 22%;">Categoría</th>
                            <th style="width: 24%;">Líder Premium</th>
                            <th style="width: 26%;">Alternativa Libre</th>
                            <th style="width: 28%;">Análisis & Ventajas</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join(rows)}
                    </tbody>
                </table>
            </div>
        </div>
    """


def render_formacion_roadmap(formacion: list[dict]) -> str:
    """
    Ruta de formación técnica visual en Glassmorphism:
    Detecta automáticamente enlaces de YouTube e inyecta el reproductor nativo 16:9
    reemplazando el botón 'Comenzar Fase'.
    """
    if not formacion:
        return "<p class='empty-msg'>No hay recursos formativos en esta edición.</p>"

    steps = []
    for idx, item in enumerate(formacion, start=1):
        step_str = f"{idx:02d}"
        title = item.get("TITULO", "Curso de IA")
        platform = item.get("PLATAFORMA", "Formación")
        level = item.get("NIVEL", "Todos los niveles")
        dur = item.get("DURACION", "")
        url = item.get("URL", "#")
        desc = item.get("RESUMEN", "")

        # Detectar si la URL es de YouTube
        youtube_id = extract_youtube_id(url)

        if youtube_id:
            action_element = f"""
                <div class="youtube-player-container">
                    <iframe 
                        src="https://www.youtube.com/embed/{escape(youtube_id)}" 
                        class="youtube-embed"
                        title="{escape(title)}"
                        frameborder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                        allowfullscreen>
                    </iframe>
                </div>
            """
        else:
            action_element = f"""
                <a href="{escape(url)}" target="_blank" rel="noopener" class="btn-roadmap">
                    <span>Comenzar Fase</span>
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline>
                    </svg>
                </a>
            """

        steps.append(f"""
            <div class="roadmap-step">
                <div class="roadmap-node">
                    <span class="roadmap-node-num">{step_str}</span>
                </div>
                <div class="roadmap-card">
                    <div class="roadmap-header">
                        <div class="roadmap-phase">
                            <span class="roadmap-phase-label">FASE {step_str} // ROADMAP</span>
                            <span class="platform-tag">• {escape(platform)}</span>
                        </div>
                        <span class="level-badge">{escape(level)}</span>
                    </div>
                    <h3 class="roadmap-title">{escape(title)}</h3>
                    <p class="roadmap-desc">{escape(desc)}</p>
                    {action_element}
                    <div class="roadmap-footer">
                        <span class="duration-text">⏱ Duración estimada: {escape(dur) if dur else 'Autoguiado'}</span>
                        {f'<span style="font-size:0.75rem; color:var(--text-muted); font-family:var(--font-mono);">▶ Video Tutorial Incrustado</span>' if youtube_id else ''}
                    </div>
                </div>
            </div>
        """)

    return f'<div class="roadmap-container">{"".join(steps)}</div>'


def render_skills(skills: list[dict]) -> str:
    """Renderiza tarjetas interactivas de skills con botón de copiado de prompts."""
    if not skills:
        return "<p class='empty-msg'>No hay skills registradas en esta edición.</p>"

    cards = []
    for idx, item in enumerate(skills):
        title = item.get("TITULO", "Skill")
        cat = item.get("CATEGORIA", "Prompt")
        desc = item.get("DESCRIPCION", "")
        prompt = item.get("PROMPT", "")
        example = item.get("EJEMPLO_USO") or item.get("EJEMPLO") or ""
        prompt_id = f"prompt-text-{idx}"

        cards.append(f"""
            <div class="skill-card">
                <div class="skill-top">
                    <span class="skill-cat">⚡ {escape(cat)}</span>
                </div>
                <h3 class="skill-title">{escape(title)}</h3>
                <p class="skill-desc">{escape(desc)}</p>
                <div class="prompt-container">
                    <div class="prompt-header">
                        <span class="prompt-label">SYSTEM PROMPT // PROTOCOLO</span>
                        <button type="button" class="btn-copy" onclick="copyPrompt('{prompt_id}', this)">
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                            </svg>
                            <span>Copiar</span>
                        </button>
                    </div>
                    <pre class="prompt-text" id="{prompt_id}">{escape(prompt)}</pre>
                </div>
                {f'<div class="skill-example"><strong>Aplicación en Producción:</strong> {escape(example)}</div>' if example else ''}
            </div>
        """)

    return f'<div class="skills-grid">{"".join(cards)}</div>'


def render_patrocinio(patrocinio_item: dict | None) -> str:
    """
    Desaturación de anuncios Above the Fold:
    Contenedor compacto estilo 'nota del editor', padding 12px 24px, fuente 0.9rem y botón pequeño.
    Si no existe patrocinador.txt, se inserta exactamente: <div id="carbonads-fallback"></div>
    """
    if not patrocinio_item:
        return '<div id="carbonads-fallback"></div>'

    title = patrocinio_item.get("TITULO", "Patrocinador Oficial")
    desc = patrocinio_item.get("RESUMEN", "")
    url = patrocinio_item.get("URL", "#")
    btn_text = patrocinio_item.get("BOTON_TEXTO", "Visitar")
    tag = patrocinio_item.get("TAG", "Destacado")

    return f"""
        <div class="sponsor-box">
            <div class="sponsor-note-body">
                <span class="sponsor-note-tag">Patrocinio // {escape(tag)}</span>
                <span class="sponsor-note-copy"><strong>{escape(title)}</strong> — {escape(desc)}</span>
            </div>
            <div class="sponsor-cta">
                <a href="{escape(url)}" target="_blank" rel="noopener noreferrer" class="btn-sponsor-mini">
                    <span>{escape(btn_text)}</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                        <polyline points="12 5 19 12 12 19"></polyline>
                    </svg>
                </a>
            </div>
        </div>
    """


JS_COPY_SCRIPT = """
    <script>
        function copyPrompt(elementId, btnElement) {
            const el = document.getElementById(elementId);
            if (!el) return;
            const textToCopy = el.innerText || el.textContent;
            navigator.clipboard.writeText(textToCopy).then(function() {
                const originalHtml = btnElement.innerHTML;
                btnElement.classList.add('copied');
                btnElement.innerHTML = `
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    <span>¡Copiado!</span>
                `;
                setTimeout(function() {
                    btnElement.classList.remove('copied');
                    btnElement.innerHTML = originalHtml;
                }, 2200);
            }).catch(function(err) {
                console.error('Error al copiar:', err);
            });
        }
    </script>
"""


def build_site():
    print("=" * 60)
    print(" GORCELX IA - GENERADOR DE SITIO ESTÁTICO (EDICIÓN UX/UI REFINADA)")
    print("=" * 60)

    # 1. Encontrar carpeta de la edición más reciente
    latest_week = find_latest_week_dir(REPO_DIR)
    week_folder_name = latest_week.name
    print(f"[*] Edición detectada: {week_folder_name} ({latest_week})")

    m = re.match(r"(\d{4})_semana_(\d+)", week_folder_name)
    if m:
        edition_label = f"Semana {m.group(2)} • {m.group(1)}"
    else:
        edition_label = week_folder_name.replace("_", " ").title()

    # 2. Preparar directorio dist/ y limpiar imágenes obsoletas
    if IMAGES_DIR.exists():
        shutil.rmtree(IMAGES_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # 3. Procesar subcarpetas
    def process_folder(subfolder_name: str, prefix: str) -> list[dict]:
        folder = latest_week / subfolder_name
        items = []
        if not folder.exists():
            return items
        txt_files = sorted(folder.glob("*.txt"))
        for tf in txt_files:
            data = parse_txt_file(tf)
            img = find_associated_image(tf)
            if img:
                web_img = copy_image_to_dist(img, prefix=prefix)
                data["_web_image"] = web_img
            items.append(data)
        return items

    noticias = process_folder("01_noticias", "noticia")
    herramientas = process_folder("02_herramientas", "tool")
    formacion = process_folder("03_formacion", "edu")
    skills = process_folder("04_skills", "skill")

    # 4. Manejo de patrocinio
    patrocinio_file = latest_week / "05_patrocinio" / "patrocinador.txt"
    patrocinio_data = None
    if patrocinio_file.exists():
        patrocinio_data = parse_txt_file(patrocinio_file)
        img = find_associated_image(patrocinio_file)
        if img:
            patrocinio_data["_web_image"] = copy_image_to_dist(img, prefix="sponsor")
        print(f"[*] Patrocinio: Activo ({patrocinio_data.get('TITULO', 'Patrocinador')})")
    else:
        print("[*] Patrocinio: No existe patrocinador.txt -> Inyectando fallback de carbonads.")

    print(f"[*] Noticias parseadas: {len(noticias)}")
    print(f"[*] Herramientas parseadas: {len(herramientas)}")
    print(f"[*] Cursos de formación parseados: {len(formacion)}")
    print(f"[*] Skills parseadas: {len(skills)}")

    # 5. Generar bloques HTML con el nuevo layout optimizado
    css_content = get_css()
    sponsor_html = render_patrocinio(patrocinio_data)
    noticias_html = render_noticias(noticias)
    herramientas_html = render_herramientas(herramientas)
    formacion_html = render_formacion_roadmap(formacion)
    skills_html = render_skills(skills)

    full_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gorcelx IA | {escape(edition_label)}</title>
    <meta name="description" content="Radar semanal y laboratorio de Inteligencia Artificial e Ingeniería de Agentes de Gorcelx.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
{css_content}
    </style>
</head>
<body>

    <!-- Header / Navbar con Logo Oficial (SIN ENLACE <a>) -->
    <header class="site-header">
        <div class="container header-content">
            <div class="brand-box">
                <div class="brand-identity">
                    <img src="{escape(GORCELX_LOGO_URL)}" alt="Gorcelx IA" class="brand-logo-img">
                    <span class="brand-text">GORCELX <span class="brand-ia-badge">IA</span></span>
                </div>
            </div>
            <span class="edition-badge">{escape(edition_label)}</span>
            <nav class="nav-links">
                <a href="#noticias">Noticias</a>
                <a href="#herramientas">Herramientas</a>
                <a href="#roadmap">Roadmap</a>
                <a href="#skills">Skills</a>
            </nav>
        </div>
    </header>

    <main class="container">
        <!-- Hero Section -->
        <section class="hero-section">
            <div class="hero-pill-badge">
                <span class="hero-pill-dot"></span>
                <span class="hero-pill-text">Edición Semanal Curada para Desarrolladores</span>
            </div>
            <h1 class="hero-title">El Radar Semanal de <span class="fire-gradient-text">Inteligencia Artificial</span></h1>
            <p class="hero-desc">Análisis exhaustivo de modelos de frontera, comparativa técnica de herramientas y prompts de arquitectura para sistemas autónomos.</p>
        </section>

        <!-- Bloque de Patrocinio Desaturado (Nota del Editor Above the Fold) -->
        {sponsor_html}

        <!-- 01 Noticias (Bento Grid con Mayor Escala de Imágenes) -->
        <section id="noticias">
            <div class="section-header">
                <h2 class="section-title">
                    <span class="section-indicator"></span>
                    Radar de Noticias
                </h2>
                <span class="section-subtitle">BENTO GRID // CRISTAL LUMINOSO</span>
            </div>
            {noticias_html}
        </section>

        <!-- REUBICACIÓN ESTRATÉGICA: FRANJA PANORÁMICA GORCELX.COM (MÁX. 300PX) -->
        <section class="gorcelx-strip-section">
            <div class="gorcelx-strip-banner">
                <img src="{escape(GORCELX_BANNER_IMG_URL)}" alt="Gorcelx Logistics SaaS" class="gorcelx-strip-bg" loading="lazy">
                <div class="gorcelx-strip-overlay"></div>
                <div class="gorcelx-strip-content">
                    <span class="gorcelx-strip-badge">PLATAFORMA SAAS LOGÍSTICA</span>
                    <h2 class="gorcelx-strip-title">Planifica tu almacén con tus tiempos reales, no a ojo.</h2>
                    <p class="gorcelx-strip-desc">Gorcelx captura tu histórico para mostrarte cuánto debería tardar cada operación. Sin software costoso ni consultoría.</p>
                    <a href="{escape(GORCELX_PROMO_URL)}" target="_blank" rel="noopener noreferrer" class="btn-gorcelx-strip">
                        <span>Descubre Gorcelx.com</span>
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="5" y1="12" x2="19" y2="12"></line>
                            <polyline points="12 5 19 12 12 19"></polyline>
                        </svg>
                    </a>
                </div>
            </div>
        </section>

        <!-- 02 Herramientas (Tabla Comparativa con Glassmorphism) -->
        <section id="herramientas">
            <div class="section-header">
                <h2 class="section-title">
                    <span class="section-indicator"></span>
                    Matriz de Herramientas
                </h2>
                <span class="section-subtitle">PREMIUM VS OPEN SOURCE</span>
            </div>
            {herramientas_html}
        </section>

        <!-- 03 Formación (Ruta Visual de Formación / Roadmap con Reproductor de YouTube Nativo) -->
        <section id="roadmap">
            <div class="section-header">
                <h2 class="section-title">
                    <span class="section-indicator"></span>
                    Ruta de Formación Técnica
                </h2>
                <span class="section-subtitle">ROADMAP // SECUENCIA DE APRENDIZAJE</span>
            </div>
            {formacion_html}
        </section>

        <!-- 04 Skills (Tarjetas Interactivas en Cristal con Copiado de Prompts) -->
        <section id="skills">
            <div class="section-header">
                <h2 class="section-title">
                    <span class="section-indicator"></span>
                    Skills & Prompt Architecture
                </h2>
                <span class="section-subtitle">TEMPLATES DE PRODUCCIÓN // COPY READY</span>
            </div>
            {skills_html}
        </section>
    </main>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-brand">
                <img src="{escape(GORCELX_LOGO_URL)}" alt="Gorcelx Logo" class="footer-logo-img">
                <span class="footer-brand-text">GORCELX IA</span>
            </div>
            <p>Laboratorio y publicación periódica independiente de inteligencia artificial e ingeniería de sistemas.</p>
            <p style="margin-top: 0.6rem; font-size: 0.8rem; font-family: var(--font-mono); color: var(--text-muted);">
                Generado por <code>build.py</code> • Estética Luminosa Editorial & Glassmorphism • {escape(edition_label)}
            </p>
        </div>
    </footer>

{JS_COPY_SCRIPT}
</body>
</html>
"""

    output_path = DIST_DIR / "index.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"[OK] Sitio estático generado con éxito: {output_path}")
    print(f"[OK] Tamaño: {output_path.stat().st_size:,} bytes")
    print("=" * 60)


if __name__ == "__main__":
    build_site()
