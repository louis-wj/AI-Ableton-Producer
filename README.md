# AI-Ableton-Producer

[![Licence: MIT](https://img.shields.io/badge/Licence-MIT-blue.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blue.svg)](CONTRIBUTING.md)

**AI-Ableton-Producer** is an open-source, full-stack generative music framework and orchestration suite engineered to bridge the gap between Large Language Models (LLMs) and Ableton Live. By translating natural language prompts, musical theory constraints, and architectural arrangements into real-time MIDI data, automation envelopes, and session layouts, this ecosystem provides an intelligent co-producer workflow natively inside the DAW.

---

## 📖 Table of Contents
- [Features](#-features)
- [Architecture & Tech Stack](#-architecture--tech-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Installation](#local-installation)
  - [Environment Variables](#environment-variables)
- [Database Schema](#-database-schema)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [Licence](#-licence)

---

## 🚀 Features

AI-Ableton-Producer provides a robust array of functionalities built to facilitate algorithmic music composition and fluid studio orchestration:

### 🎹 Natural Language to MIDI & Clip Generation
* **Generative Arrangement:** Converts abstract textual ideas (e.g., "Create a melancholic 80s synth-wave bassline in F minor") into structurally sound MIDI loops, complete with precise note values, velocities, and humanised micro-timing.
* **Music Theory Alignment:** Enforces rigid harmonic constraints, ensuring that generated chord progressions, melodies, and counterpoints adapt to custom scale selections natively.

### 🎛️ Live Device Control & Parameter Automation
* **Max for Live (M4L) Routing:** Direct control over Ableton Live's internal parameters via low-latency API integration, manipulating device dials, audio effects, and instrument parameters on the fly.
* **Generative Envelope Curves:** Synthesises intricate automation lanes, mapping complex modulation patterns (e.g., filter sweeps, panning rhythms) directly onto selected arrangement clips.

### 🗂️ Project Structure & Session Seeding
* **Template Blueprinting:** Automatically builds, labels, and color-codes multi-track Ableton Live sets containing pre-configured channel hierarchies, auxiliary returns, and grouped instrument chains.
* **Dynamic Variation Engine:** Spawns stylistic variations of clips, generating fills, bridge transitions, and alternative melodies to rapidly build out comprehensive arrangement blocks.

### 🛡️ Local Model Auditing & Telemetry
* **Generation Profiling:** An administrative hub monitoring prompt histories, parameter seeds, and model response latency metrics.
* **Midi & Preset Mapping:** Deep data storage tracking custom configuration settings, mapping configurations, and model performance metrics.

---

## 🛠️ Architecture & Tech Stack

AI-Ableton-Producer is engineered using an asynchronous, event-driven pattern designed to safely handle heavy generative payloads alongside real-time MIDI streaming pipelines.

              ┌────────────────────────┐
              │    Producer UI         │
              │   (React / Next.js)    │
              └───────────┬────────────┘
                          │ HTTPS / WSS
                          ▼
              ┌────────────────────────┐
              │    Gateway & Router    │
              └───────────┬────────────┘
                          │
     ┌────────────────────┴────────────────────┐
     ▼                                         ▼
┌─────────────────┐                       ┌─────────────────┐│ LLM Music Engine│                       │  OSC / MIDI     ││ & Parsing Node  │                       │ Bridge Service  │└────────┬────────┘                       └────────┬────────┘│                                         │▼                                         ▼┌─────────────────┐                       ┌─────────────────┐│ Relational DB / │                       │ Ableton Live /  ││ Configuration   │                       │ Max For Live    │└─────────────────┘                       └─────────────────┘
### Frontend
* **Core Framework:** TypeScript, React.js (or Next.js) managing generative prompts, piano-roll visualisations, and session state logs.
* **State Management:** Zustand or Redux Toolkit capturing active scales, root notes, project BPM, and generation history.
* **Styling Ecosystem:** Tailwind CSS combined with dark-themed components modeled after modern DAW interfaces.

### Backend
* **Runtime Environment:** Node.js paired with Express or NestJS, running side-by-side with a Python service optimized for musical generation (using libraries like Mido and Music21).
* **Network Protocol Communication:** Open Sound Control (OSC) or specialized WebSockets bridging communication between the backend environment and Ableton Live.
* **Data Layer:** Prisma ORM mapping user templates, prompt configurations, and session presets securely.

### Databases & Ableton Interfacing
* **Persistent Storage:** PostgreSQL (or SQLite) maintaining logs of prompt strings, successfully generated MIDI blobs, and custom device mappings.
* **DAW Environment:** Ableton Live (v11/v12 Suite) executing a custom Max for Live device configured to parse incoming network arrays and manipulate the Live API.

---

## 💻 Getting Started

Follow these detailed steps to stand up a local instance of AI-Ableton-Producer for development and verification purposes.

### Prerequisites
Ensure your local host environment runs the following baseline dependencies:
* **Node.js:** `v18.x` or later
* **Python:** `v3.10+` with pip installed
* **DAW:** Ableton Live Suite (with Max for Live enabled)

### Local Installation

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/louis-wj/AI-Ableton-Producer.git](https://github.com/louis-wj/AI-Ableton-Producer.git)
   cd AI-Ableton-Producer
Install JavaScript Dependencies:Bashnpm install
Set Up the Python Generation Service:Bashcd backend/music-engine
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
Install and Link the Max for Live Device:Locate the .amxd file within the /max-device folder and drag it into your Ableton Live Master track or User Library. Ensure it is configured to listen to the specified OSC port (default: 7001).Spin Up the Local Servers:Return to the project root directory and run the unified startup script:Bashnpm run dev
Environment VariablesYour backend .env configuration template must contain the following declarations:Code snippet# Server Network Settings
PORT=5000
NODE_ENV=development

# Database Connection URI
DATABASE_URL="postgresql://db_user:db_password@localhost:5462/ai_ableton_db?schema=public"

# AI Core Configuration
OPENAI_API_KEY="sk-proj-your_secure_openai_key_for_music_generation"
ANTHROPIC_API_KEY="sk-ant-your_secure_anthropic_key"

# Ableton Interfacing Ports
OSC_OUT_PORT=7001
OSC_IN_PORT=7002
ABLETON_HOST="127.0.0.1"
📊 Database SchemaThe entity relationships inside AI-Ableton-Producer are structured to track complex track settings and parameters seamlessly:Entity TablePrimary ResponsibilityKey Attributes IncludedUsersSystem identity registryid, email, password_hash, role, created_atGenerationsLog of AI prompt executionsid, user_id, prompt_text, midi_data_blob, scale, bpmTrackTemplatesSaved track architecture blueprintsid, name, structure_json, device_chain_mappingsAutomationLanesStores generated clip shapesid, generation_id, target_parameter, envelope_points[]DeviceMappingsResolves Ableton IDS to labelsid, device_name, parameter_index, min_max_bounds⚡ API DocumentationAll request parameters, headers, and payloads interact natively using serialization standards.Project Orchestration EndpointsPOST /api/generate/midi - Submits a prompt to the Python engine, producing a MIDI object filtered by scale parameters.POST /api/generate/automation - Calculates envelope nodes for filter/modulation adjustments based on song structure context.POST /api/ableton/sync - Pushes a fully compiled track layout profile directly over the active network bridge to Ableton Live.Settings & Presets EndpointsGET /api/presets/templates - Queries saved arrangement outlines, return tracks layouts, and custom routing chains.🧪 TestingAI-Ableton-Producer guarantees reliability through comprehensive integration test blocks using structural frameworks like Jest and PyTest.Executing JavaScript Framework TestsNavigate into your root or backend instance to fire up structural node validations:Bashnpm run test
Executing Python Musical Logic TestsValidate MIDI quantization mathematical logic, scale matrices, and note processors:Bashcd backend/music-engine
pytest
🤝 ContributingContributions are vital to AI-Ableton-Producer's continuous evolution. Please follow this structural process to introduce fixes or feature enhancements:Fork the codebase at https://github.com/louis-wj/AI-Ableton-Producer.Initialise a dedicated, descriptive tracking branch: git checkout -b feature/your-awesome-feature.Commit your adjustments locally ensuring message patterns align neatly with modern git practices.Push execution states up to your repository copy: git push origin feature/your-awesome-feature.Open a detailed Pull Request outlining your architectural changes, visual improvements, or performance patches.📄 LicenceDistributed strictly under the terms of the MIT Licence. Review the complete layout parameters inside the local LICENSE asset file for comprehensive legal parameters.
