# Voice Coding Assistant (Frontend)

This repository contains the **frontend code** for the Voice Coding Assistant project (VCAI).  
It allows users to **write code using voice commands**, see live transcription, and view AI-generated edits in a **diff view**.

## Features

- **Voice-to-Code:** Speak your code and it will appear live in the editor.  
- **Run AI (Mock):** Press "Run AI" or say "run code" to see AI-generated changes.  
- **Diff Viewer:** Compare original code with AI-edited code side by side.  
- **Transcript Panel:** Shows live transcription of your voice commands.  

## Tech Stack

- **React 19** + **Vite**  
- **Monaco Editor**  
- **React Diff Viewer**  
- **react-speech-recognition**  
- **Tailwind CSS**  

## Notes

- Backend AI integration is still under development. Currently, `Run AI` uses a **mock function** for testing the frontend.  
- Audio playback is a placeholder and will be replaced with actual TTS from the backend.
