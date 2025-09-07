import { useState, useEffect, useRef } from "react";
import Editor from "@monaco-editor/react";
import { Mic } from "lucide-react";
import SpeechRecognition, { useSpeechRecognition } from "react-speech-recognition";
import ReactDiffViewer from "react-diff-viewer";

// Editor panel
function EditorPanel({ code, setCode }) {
  return (
    <Editor
      height="300px"
      defaultLanguage="javascript"
      value={code}
      onChange={(value) => setCode(value || "")}
      theme="vs-dark"
    />
  );
}

// Mic controls
function MicControls({ listening, toggleMic }) {
  return (
    <button
      onClick={toggleMic}
      className={`px-4 py-2 rounded flex items-center gap-2 ${
        listening ? "bg-red-500 hover:bg-red-600" : "bg-green-500 hover:bg-green-600"
      } text-white`}
    >
      <Mic size={18} />
      {listening ? "Stop" : "Speak"}
    </button>
  );
}

// Transcript panel
function TranscriptPanel({ transcript }) {
  return (
    <div className="mt-4">
      <h2 className="font-semibold">Transcript:</h2>
      <p className="bg-gray-100 p-2 rounded min-h-[40px] overflow-auto">
        {transcript || "Say something..."}
      </p>
    </div>
  );
}

// Diff panel
function DiffPanel({ oldCode, newCode }) {
  return (
    <div className="mt-4">
      <h2 className="font-semibold">AI Output (Diff View):</h2>
      <div className="bg-gray-100 p-2 rounded min-h-[100px] overflow-auto">
        <ReactDiffViewer oldValue={oldCode} newValue={newCode} splitView={true} />
      </div>
    </div>
  );
}

function App() {
  const [code, setCode] = useState("// Write your code here");
  const [backendResult, setBackendResult] = useState("// AI output will appear here");
  const [listening, setListening] = useState(false);
  const [audioPlaying, setAudioPlaying] = useState(false);
  const [loading, setLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");

  const audioRef = useRef(null);
  const { transcript, resetTranscript } = useSpeechRecognition();
  const lastTranscriptRef = useRef("");

  if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
    return <span>Your browser does not support speech recognition.</span>;
  }

  // Mock backend
  const sendToBackend = async (codeText) => {
    setLoading(true);
    setStatusMessage("AI is running...");
    return new Promise((resolve) => {
      setTimeout(() => {
        const edited = codeText.split("\n").reverse().join("\n"); // dummy AI edit
        const audioURL = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3";
        resolve({ editedCode: edited, audioURL });
        setLoading(false);
        setStatusMessage("");
      }, 1000);
    });
  };

  const runAI = async () => {
    if (!code) return;
    setLoading(true);
    setStatusMessage("Running AI...");
    const result = await sendToBackend(code);

    if (audioRef.current) audioRef.current.pause();

    setBackendResult(result.editedCode);

    audioRef.current = new Audio(result.audioURL);
    setAudioPlaying(true);
    setStatusMessage("Playing audio...");
    audioRef.current.play();
    audioRef.current.onended = () => {
      setAudioPlaying(false);
      setStatusMessage("");
    };
    setLoading(false);
  };

  const toggleMic = () => {
    if (listening) {
      SpeechRecognition.stopListening();
      setListening(false);
      setStatusMessage("");
    } else {
      if (audioRef.current && audioPlaying) {
        audioRef.current.pause();
        setAudioPlaying(false);
      }
      resetTranscript();
      lastTranscriptRef.current = "";
      SpeechRecognition.startListening({ continuous: true, language: "en-US" });
      setListening(true);
      setStatusMessage("Listening...");
    }
  };

  // Live dictation: append new speech lines to editor
  useEffect(() => {
    if (!transcript) return;

    // Detect new words since last update
    const newPart = transcript.replace(lastTranscriptRef.current, "").trim();
    if (newPart) {
      setCode((prev) => (prev === "// Write your code here" ? newPart : prev + "\n" + newPart));
      lastTranscriptRef.current = transcript;
    }

    if (transcript.toLowerCase().includes("run code")) {
      runAI();
      resetTranscript();
      lastTranscriptRef.current = "";
    }
  }, [transcript]);

  return (
    <div className="flex flex-col items-center p-4 min-h-screen bg-gray-100">
      <h1 className="text-2xl font-bold mb-4">Voice Coding Assistant</h1>

      <div className="w-full max-w-4xl bg-white rounded-xl shadow-lg p-4">
        <EditorPanel code={code} setCode={setCode} />

        <div className="flex gap-2 mt-4">
          <button
            onClick={runAI}
            disabled={loading}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
          >
            Run AI
          </button>

          <MicControls listening={listening} toggleMic={toggleMic} />
        </div>

        {statusMessage && (
          <p className="mt-2 text-sm font-medium text-gray-700">{statusMessage}</p>
        )}

        <TranscriptPanel transcript={transcript} />
        <DiffPanel oldCode={code} newCode={backendResult} />
      </div>
    </div>
  );
}

export default App;

