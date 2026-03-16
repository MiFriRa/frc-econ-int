# FRC-ECON-INT: Autonomous OSINT Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Powered by Gemini](https://img.shields.io/badge/AI-Gemini%203.1%20Pro-orange.svg)](https://ai.google.dev/)

> **Frimer-Rasmussen Consulting Intelligence Engine**
> A configuration-driven, autonomous OSINT engine designed to monitor geopolitical and economic indicators with clinical precision.

## 核心 (The Core)

This engine automates the intelligence lifecycle through three distinct phases:

1.  **Scout (Detection)**: Uses Google Search Grounding to monitor trackers defined in `trackers.json`.
2.  **Vacuum (Extraction)**: Distills raw text into structured claims, stripping away journalistic bias.
3.  **Truth Check (Verification)**: Cross-references claims directly against official entities and primary sources.

## 🎛️ Architecture

- **Logic (`Python`)**: Agnostic scripts for orchestration and data processing.
- **Intelligence (`JSON`)**: Configuration files (`trackers.json`, `verified_sources.json`) that drive the engine's focus.
- **Real-time Feed**: A premium dashboard displaying live analysis events and verified intelligence.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Google Gemini API Key

### Installation

```powershell
# Clone the repository
git clone https://github.com/frimer-rasmussen/frc-econ-int.git
cd frc-econ-int

# Setup environment
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
# Create a .env file with:
# GEMINI_API_KEY=your_key_here
```

### Usage

```powershell
# Run the OSINT Engine
python engine.py

# Start the Intelligence Dashboard
python app.py
```

## 🛡️ Axioms

All development follows the **Frimer-Rasmussen Consulting Axioms**:
- **Joy**: Premium aesthetics and UX.
- **Utility**: Focus on high-impact OSINT data.
- **Transparency**: Clinical data provenance.
- **Continuous Verification**: Trust but verify via Search Grounding.

---
*Developed by Frimer-Rasmussen Consulting. Clinical. Neutral. Precise.*
