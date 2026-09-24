# Contributing to Agentic Document Analyser

Thank you for your interest in contributing to **Agentic Document Analyser**! This project is maintained by [AiExponent](https://aiexponent.com) as part of our open-source AI governance toolchain.

We welcome pull requests, bug reports, and suggestions from the community.

---

## Code of Conduct

All contributors and participants agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md) (Contributor Covenant v2.1). Please review it before participating.

---

## Security Vulnerabilities

Please do **NOT** report security vulnerabilities through public GitHub issues. Follow our coordinated vulnerability disclosure process outlined in [SECURITY.md](SECURITY.md) and email [security@aiexponent.com](mailto:security@aiexponent.com).

---

## Development Setup

The system comprises three Python 3.11+ FastAPI microservices and a Next.js 14 frontend.

### Prerequisites

* **Python 3.11+** (virtualenv or conda recommended)
* **Node.js 20+** and `npm`
* **Poppler** (required for `pdf2image`):
  * macOS: `brew install poppler`
  * Ubuntu / Debian: `sudo apt-get install -y poppler-utils`
* **Fireworks AI API Key**: required for visual document understanding ([fireworks.ai](https://fireworks.ai))

### 1. Fast Start via Docker Compose (Recommended)

To run the entire 4-container stack locally:

```bash
# Configure environment
cp .env.cloud.template .env
# Edit .env and insert your FIREWORKS_API_KEY

# Build and start services
docker compose up --build
```

Endpoints will be available at:
* **Frontend UI**: [http://localhost:3001](http://localhost:3001)
* **Orchestrator Gateway**: [http://localhost:8000](http://localhost:8000)
* **Preprocessing Service**: [http://localhost:8001](http://localhost:8001)
* **Visual Intelligence Service**: [http://localhost:8002](http://localhost:8002)

### 2. Manual Local Service Setup

#### Python Microservices

```bash
# Create and activate Python 3.11 environment
python3.11 -m venv .venv
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies for all services
pip install -r orchestrator/requirements.txt
pip install -r preprocessing_service/requirements.txt
pip install -r visual_service/requirements.txt

# Configure your API key
export FIREWORKS_API_KEY="your_api_key_here"
```

Run each service in a separate terminal:

```bash
# Terminal 1: Preprocessing Service (Port 8001)
uvicorn preprocessing_service.main:app --port 8001 --reload

# Terminal 2: Visual Intelligence Service (Port 8002)
uvicorn visual_service.main:app --port 8002 --reload

# Terminal 3: Orchestrator Gateway (Port 8000)
uvicorn orchestrator.main:app --port 8000 --reload
```

#### Frontend Application

```bash
cd frontend
npm install
npm run dev
# Open http://localhost:3000
```

---

## Running Tests & Quality Gates

Before submitting a pull request, ensure all tests and quality checks pass locally.

### Python Backend

```bash
# Run automated test suite
pytest tests/ -v

# Run linting check
ruff check .
```

### Next.js Frontend

```bash
cd frontend
npm run lint
npm run build
```

---

## Contribution Workflow & PR Guidelines

1. **Fork and Branch**:
   * Fork the repository on GitHub.
   * Create a topic branch from `main`:
     ```bash
     git checkout -b feat/your-feature-name
     # or
     git checkout -b fix/your-bugfix-name
     ```

2. **Commit Message Conventions**:
   We follow [Conventional Commits](https://www.conventionalcommits.org/):
   * `feat(service)`: New feature or capability
   * `fix(service)`: Bug fix
   * `docs`: Documentation updates
   * `test`: Adding or updating test cases
   * `chore`: Build scripts, dependencies, CI configuration

3. **Scope and Modularity**:
   * Keep changes focused and self-contained.
   * If a change spans across the orchestrator and a worker service, clearly explain the contract evolution in the PR description.
   * Never commit API keys, secrets, or raw proprietary customer documents.

4. **Pull Request Submission**:
   * Open your PR against `main`.
   * Fill out the PR template describing the problem, solution, and testing performed.
   * Ensure GitHub Actions CI workflows pass cleanly.

---

## License

By contributing to Agentic Document Analyser, you agree that your contributions are licensed under the [Apache License 2.0](LICENSE).
