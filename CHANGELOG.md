# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-09-26

### 🎨 Brand & Positioning
- **AiExponent Brand Alignment**: Fully retired legacy "DocIntel Pro" identity across documentation, frontend, and schemas in favor of **Agentic Document Analyser**.
- **Visual Assets**: Deployed official AiExponent Caret logo, dual-mode light/dark hero banners, and brand color palette (`#0D5463`).
- **Regulatory Scope**: Articulated explicit EU AI Act Article 9 (risk management) and Annex IV (technical documentation) layout and extraction scope.

### 🛡️ Governance & Community Health
- **Security Policy (`SECURITY.md`)**: Established vulnerability reporting policy with 48-hour SLA, safe harbor provisions, and security contact info.
- **Code of Conduct (`CODE_OF_CONDUCT.md`)**: Adopted Contributor Covenant v2.1.
- **Contribution Guidelines (`CONTRIBUTING.md`)**: Comprehensive developer setup instructions, multi-service architecture guides, and PR conventions.
- **License Parity**: Standardized on Apache 2.0 license with canonical `NOTICE` file.

### 🧪 Automated Testing & Quality Gates
- **Pytest Test Suite**: Implemented centralized 29-test automated test suite across microservices (`tests/test_common.py`, `tests/test_orchestrator.py`, `tests/test_preprocessing.py`, `tests/test_visual.py`).
- **CI Modernization**: Replaced placeholder `compileall` gate in `.github/workflows/ci.yml` with strict `pytest` testing and `ruff` linting.
- **Security Auditing**: Added Bandit static code analysis, `pip-audit` dependency vulnerability scanning, and npm auditing in CI.

### 📦 Packaging, Modernization & Ecosystem
- **Container Modernization**: Bumped Python baseline in Dockerfiles to `python:3.11-slim` with standardized container naming and multi-stage builds.
- **Docker Compose Ergonomics**: Streamlined `docker-compose.yml` quickstart and verified service inter-connectivity.
- **Automated Updates**: Added `.github/dependabot.yml` for automated weekly updates across Docker, Python, GitHub Actions, and npm ecosystems.
- **5-Tool Governance Ecosystem**: Integrated reciprocal navigation footer cross-linking LitmusAI (Art. 5), License Compliance Checker (Art. 53), RAG Benchmarking (Art. 15), and RiskForge (Art. 9).

## [0.1.1] - 2024-01-31

### 🚀 Features
- **Docker Package Support**: Added Dockerfiles and GitHub Actions workflow to auto-publish packages to GHCR.
- **Visual Intelligence**: Integrated Qwen2-VL (via Fireworks AI) for unified layout analysis and OCR.
- **Frontend**:
    - Next.js 14 UI with Tailwind CSS and Shadcn/UI integration.
    - Interactive Document Visualizer with bounding box overlays.
    - Drag-and-drop file upload supporting PDF and Image formats.
- **Microservices Architecture**:
    - **Orchestrator**: Asyncio-based workflow engine managed by FastAPI.
    - **Preprocessing**: PDF-to-Image conversion and normalization pipeline.
    - **Visual Service**: Dedicated service for VLM inference and JSON parsing.

### 🐛 Bug Fixes
- Fixed "Image failed to load" race condition for multi-page PDF uploads.
- Resolved race conditions in concurrent page processing.
- Fixed TypeScript type errors in frontend components.

### 🛠 Improvements
- Establishing comprehensive CI pipeline (Linting + Build Checks).
- Standardized logging across all Python services.
- Consolidated repository structure (removed nested git).
- Added `ARCHITECTURE.md` with detailed Mermaid system diagrams.
