# Contributing to FRC-ECON-INT

Welcome! We appreciate your interest in contributing to the Frimer-Rasmussen Consulting OSINT Engine.

## Coding Standards

- **Tone**: All analytical outputs should follow a clinical, neutral OSINT tone. Avoid descriptive adjectives or "spin".
- **Architecture**: Keep the "Motor" (Python) separate from the "Intelligence" (JSON).
- **Security**: Never commit API keys or experimental data. All raw data should stay in the `data/` directory (gitignored).

## Process

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

## Environment Setup

```bash
# Initialize virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---
*By contributing, you agree that your contributions will be licensed under the MIT License.*
