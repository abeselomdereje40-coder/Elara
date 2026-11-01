ELARA — Local AI Personal Assistant

ELARA is a locally operated, AI-powered personal assistant built with Python. It combines large language models, persistent memory, document processing, web research, and image generation in a desktop application.

The project explores how multiple AI components can work together to create a private, locally operated assistant.

Features

- Conversational AI: Interact with a locally hosted language model.
- Persistent Memory: Store and retrieve conversation history and personal context.
- Knowledge Management: Upload, process, search, and retrieve information from documents.
- Project Management: Organize project information and maintain project context.
- Web Research: Search the web, retrieve sources, and extract relevant information.
- Image Generation: Generate images using a local Stable Diffusion model through OpenVINO.
- Desktop Interface: Dark-themed graphical interface built with CustomTkinter.
- Local Processing: Run the main AI workflow using locally hosted models.

Technology Stack

- Python
- CustomTkinter
- SQLite
- llama.cpp
- Qwen3 1.7B
- Sentence Transformers
- RapidOCR
- OpenVINO
- Stable Diffusion
- DuckDuckGo Search

Architecture

ELARA uses a modular architecture that separates the graphical interface, reasoning system, memory management, and specialized tools.

ELARA
│
├── GUI
│
├── Brain
│   ├── Decision Engine
│   ├── Context Engine
│   ├── Memory Recall
│   └── Prompt Builder
│
├── Memory System
│   ├── Database
│   ├── Memory Manager
│   └── Knowledge Management
│
├── Tools
│   ├── File Processing
│   ├── Calculator
│   ├── Image Generation
│   └── Knowledge Processing
│
└── Web Research
    ├── Search Provider
    ├── Source Fetcher
    ├── Research Planner
    └── Evidence Extractor

Requirements

- Windows
- Python
- Git
- llama.cpp
- Qwen3 1.7B GGUF model
- Required Python dependencies

Additional model and runtime requirements depend on the features you want to use.

Documentation

The project includes a consolidated technical documentation file:

"Elara document.docx"

It describes the project files, imports, classes, functions, and their responsibilities.

Project Status

ELARA has reached its initial completed development milestone. Its current implementation is available in this repository.

Further improvements and refinements may be made over time.

Author

Abeselom Dereje Kebede

Information Systems Student | Aspiring AI Developer

GitHub: "@abeselomdereje40-coder" (https://github.com/abeselomdereje40-coder)

---

Built as a personal project to explore local AI systems, software architecture, and intelligent automation.