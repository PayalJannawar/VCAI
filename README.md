# 🎙️ Voice Coding Assistant (VCAI)

An AI-powered **Voice Coding Assistant** that enables developers to generate code using **voice** and **text commands**. The application integrates **React**, **FastAPI**, **Google Gemini**, and **Monaco Editor** to provide an interactive coding environment with AI-assisted code generation and chat-based interaction.

---
## 📷 Application Preview

### Home Screen

![Home](assets/home.png)

## 📖 Project Overview

Voice Coding Assistant (VCAI) is an AI-powered coding assistant that enables developers to interact with AI using both **voice** and **text commands**. The application combines an interactive **Monaco Code Editor** with an AI-powered assistant to help users generate, debug, optimize, convert, and explain code efficiently.

The frontend is built with **React**, while the backend uses **FastAPI** to communicate with the **Google Gemini API**. Speech recognition enables hands-free interaction, and chat history is stored locally to provide a seamless coding experience across browser sessions.

## ✨ Features

- 🎤 Voice-based code generation using browser Speech Recognition
- 💬 AI-powered text chat interface
- 📝 Monaco Code Editor integration
- 🤖 AI-assisted code generation
- 🐞 Code debugging assistance
- ⚡ Code optimization
- 🔄 Programming language conversion
- 📚 Code explanation
- 💾 Persistent chat history using Local Storage
- 📋 Copy generated code
- 🗑 Clear editor and start a new conversation
- 🌐 Multi-language support (C++, Java, Python, JavaScript, HTML, CSS)
- 🔌 FastAPI backend with Google Gemini integration

## 🛠️ Tech Stack

### Frontend
- React
- JavaScript (ES6+)
- CSS3
- Monaco Editor
- react-speech-recognition

### Backend
- FastAPI
- Python
- Google Gemini API

### Storage
- Browser Local Storage

### Development Tools
- Git
- GitHub
- Visual Studio Code

## 🏗️ Project Architecture

The application follows a client-server architecture where the React frontend handles user interactions and the FastAPI backend processes AI requests.

### Workflow

1. User provides input through **voice** or **text**.
2. Speech input is converted into text using **Browser Speech Recognition**.
3. The frontend detects the user's intent (Generate, Explain, Debug, Optimize, Convert).
4. A request is sent to the **FastAPI** backend.
5. The backend communicates with the **Google Gemini API**.
6. The AI-generated response is returned to the frontend.
7. Generated code is displayed inside the **Monaco Editor**, while the conversation is maintained in the Assistant panel.
8. Chat history is stored locally using **Local Storage**.

## 📸 Application Screenshots

### 🏠 Home Interface

![Home](assets/home.png)

---

### 💻 Monaco Code Editor

![Editor](assets/editor.png)

---

### 🤖 AI Assistant Panel

![Assistant](assets/assistant.png)

---

### 📂 Chat History

![Sidebar](assets/sidebar.png)