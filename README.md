# MarketScout DUAL-AI 🚀

[🇪🇸 Español](#documentación-técnica---español) | [🇬🇧 English](#technical-documentation---english)

---

## Documentación Técnica - Español

### Resumen del Proyecto
MarketScout DUAL-AI es una plataforma avanzada de inteligencia de mercado impulsada por Inteligencia Artificial. Su arquitectura se basa en un enfoque de **"Doble Validación IA"**: lanza peticiones en paralelo a dos modelos de lenguaje de última generación (Claude 3.5 Sonnet y Claude 3 Opus) y luego utiliza un tercer proceso computacional para sintetizar, comparar y verificar las predicciones de ambos modelos.

Esta metodología reduce de forma drástica las alucinaciones de la IA y proporciona estrategias de negocio con un altísimo grado de fiabilidad, presentadas en un Dashboard visual y exportable.

### Arquitectura Técnica
El proyecto se divide en tres componentes clave, diseñados intencionalmente sin frameworks pesados (Vanilla JS) para asegurar un rendimiento ultrarrápido y portabilidad total:

1. **Frontend Interactivo (`market-scout.html`)**:
   - **Tecnologías**: HTML5, Vanilla CSS3 (Custom Properties), Vanilla JavaScript.
   - **Funciones Principales**:
     - Gestión del estado y animaciones asíncronas de la barra de progreso (3 fases).
     - Renderizado de gráficos en tiempo real mediante *HTML5 Canvas* (Gráfico de Radar para comparación entre modelos).
     - Internacionalización instantánea (Toggle ES/EN).
     - Sistema de persistencia de datos local (`localStorage`) para gestionar Claves API seguras y guardar el "Historial de Búsquedas recientes".
     - Exportación de resultados: Integración nativa de exportación a un reporte Markdown (.md) y copia cruda al portapapeles.

2. **Backend Proxy Server (`proxy.py`)**:
   - **Tecnologías**: Python 3.
   - **Propósito**: Actúa como un *CORS Middleware*. Por motivos de seguridad, plataformas como Anthropic prohíben peticiones REST directas desde un navegador (Bloqueo CORS). Este proxy recibe las peticiones `fetch` del cliente y las redirige al servidor oficial de la API firmando la cabecera `x-api-key` en el lado del servidor de forma protegida. Además, enruta el tráfico raíz (`/`) directamente a `market-scout.html`.

3. **Arquitectura de Despliegue Docker (`Dockerfile`)**:
   - **Tecnologías**: Docker, imagen `python:3.11-slim`.
   - **Propósito**: Empaqueta el proxy y el frontend en un contenedor altamente eficiente configurado para exponer el puerto `7860`. Esta es la configuración obligatoria para despliegues serverless en plataformas de IA como **Hugging Face Spaces**.

### Flujo de Datos (Data Flow)
1. **Entrada de Usuario**: El cliente introduce un nicho de mercado (ej: "Sillas de oficina").
2. **Prompts Paralelos**: El Frontend envía simultáneamente peticiones asíncronas (`Promise.all`) al backend.
   - *Pista A*: Analizado por `claude-3-5-sonnet-20240620` (rápido y analítico).
   - *Pista B*: Analizado por `claude-3-opus-20240229` (profundo y estratégico).
3. **Síntesis y Consenso**: Tras recibir ambos vectores JSON, se lanza una tercera petición, obligando a la IA a contrastar ambas salidas, calcular un *Porcentaje de Consenso (%), una valoración de Estrellas de Fiabilidad y generar una Hoja de Ruta Táctica.
4. **Visualización y Volcado**: El JSON final verificado se dibuja dinámicamente en las tarjetas del DOM y el canvas, guardándose un caché en disco duro local (`localStorage`).

---

## Technical Documentation - English

### Project Overview
MarketScout DUAL-AI is an advanced, AI-driven market intelligence platform. Its architecture relies on a **"Dual AI Validation"** approach: it triggers parallel requests to two state-of-the-art Large Language Models (Claude 3.5 Sonnet and Claude 3 Opus), subsequently utilizing a third synthesis step to compare and verify both predictions.

This methodology drastically reduces AI hallucinations and delivers highly reliable business strategies, visually presented on a dashboard ready for export.

### Technical Architecture
The project is decoupled into three key components. It was intentionally built without heavy JS frameworks (Vanilla JS) to guarantee lightning-fast performance and total portability:

1. **Interactive Frontend (`market-scout.html`)**:
   - **Stack**: HTML5, Vanilla CSS3 (CSS Variables for dynamic theming), Vanilla JavaScript.
   - **Core Features**:
     - State management and async animations for the 3-phase progression bar.
     - Real-time data visualization using native *HTML5 Canvas* (Radar Chart for Sonnet vs Opus comparison).
     - Seamless Internationalization (ES/EN toggle).
     - Local storage management (`localStorage`) for handling API keys safely and maintaining a "Recent Searches History" modal.
     - Data Export: Native Markdown (.md) report generation and raw clipboard copying features.

2. **Backend Proxy Server (`proxy.py`)**:
   - **Stack**: Python 3 standard library.
   - **Purpose**: Acts as a *CORS Middleware*. Due to security policies, services like Anthropic ban direct client-browser REST requests (CORS blocking). This proxy catches front-end HTTP `fetch` calls, acts as a secure relay injecting the `x-api-key` header on the server side, and proxies the Anthropic JSON response back to the client. It also acts as the primary web server binding traffic on `/` to the main HTML document.

3. **Docker Deployment Architecture (`Dockerfile`)**:
   - **Stack**: Docker, `python:3.11-slim` lightweight image.
   - **Purpose**: Containerizes the application (proxy + frontend UI) configured to expose port `7860`. This specific port and setup ensure absolute compliance with serverless AI hostings, specifically tailored for 1-click deployments on **Hugging Face Spaces**.

### Data Flow Execution
1. **User Input**: The user submits a specific market niche.
2. **Parallel Prompting**: The Frontend concurrently dispatches asynchronous jobs to the backend proxy.
   - *Track A*: Handled by `claude-3-5-sonnet-20240620` (analytical & fast).
   - *Track B*: Handled by `claude-3-opus-20240229` (deep reasoning & strategic).
3. **Synthesis & Consensus**: Once both JSON payloads are returned, a third AI prompt is issued to cross-reference constraints, calculate a *Consensus Percentage (%)*, output a *Reliability Star Score*, and generate a 3-Phase Tactical Roadmap.
4. **Render & Cache**: The final verified JSON object dynamically injects into the Document Object Model (DOM) and Radar Canvas, persisting in the browser's `localStorage` for future retrieval.
