import Home from "./pages/Home";
import { useState, useEffect, useRef } from "react";
import SpeechRecognition, { useSpeechRecognition } from "react-speech-recognition";


function App() {
  const [code, setCode] = useState("// Write your code here");
  const [backendResult, setBackendResult] = useState("// AI output will appear here");
  const [listening, setListening] = useState(false);
  const [loading, setLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");
  const [intent, setIntent] = useState("");
  const [language, setLanguage] = useState("");
  const [status, setStatus] = useState("Idle");
  const [backendConnected, setBackendConnected] = useState(true);

  const { transcript, resetTranscript } = useSpeechRecognition();
  const lastTranscriptRef = useRef("");
  const [userInput, setUserInput] = useState("");
  const [chatHistory, setChatHistory] = useState([]);

  const [currentChatId, setCurrentChatId] = useState(null);
  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text: "Hello! I'm your Voice Coding Assistant. How can I help you today?",
    },
  ]);

  if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
    return <span>Your browser does not support speech recognition.</span>;
  }

  const sendToBackend = async (codeText) => {
  setLoading(true);
  setStatusMessage("AI is running...");


  try {
    const lower = codeText.toLowerCase();
    
    
  let intent = "generate_code";

  if (
    lower.includes("explain") ||
    lower.includes("what does") ||
    lower.includes("how does")
  ) {
    intent = "explain_code";
  }
  else if (
    lower.includes("debug") ||
    lower.includes("fix") ||
    lower.includes("error") ||
    lower.includes("bug")
  ) {
    intent = "debug_code";
  }
  else if (
    lower.includes("optimize") ||
    lower.includes("improve") ||
    lower.includes("faster")
  ) {
    intent = "optimize_code";
  }
  else if (
    lower.includes("convert") ||
    lower.includes("translate")
  ) {
    intent = "convert_code";
  }

    let language = "javascript";

    if (lower.includes("python")) language = "python";
    else if (lower.includes("java")) language = "java";
    else if (lower.includes("cpp") || lower.includes("c++")) language = "cpp";
    else if (lower.includes("c#")) language = "csharp";
    else if (lower.includes("html")) language = "html";
    else if (lower.includes("css")) language = "css";

    setIntent(intent);
    setLanguage(language);
    setStatus("Generating...");

    const response = await fetch("http://127.0.0.1:8000/code-assistant", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        intent: intent,
        language: language,
        task: codeText,
      }),
    });

    if (!response.ok) {
      throw new Error("Backend returned an error.");
    }

    const data = await response.json();
    setBackendConnected(true);
    setStatus("Completed");

    return {
      editedCode: data.response,
      audioURL: null,
    };
  } catch (err) {
    console.error(err);
    setStatus("Failed");
    setBackendConnected(false);
    alert("Failed to connect to backend.");

    return {
      editedCode: "Error connecting to backend.",
      audioURL: null,
    };
  } finally {
    setLoading(false);
    setStatusMessage("");
  }
};
function cleanTranscript(text) {
  return text
    .replace(/\b(uh|um|okay|ok|stop)\b/gi, "")
    .replace(/\s+/g, " ")
    .trim();
}   

const runAI = async () => {
  const input = cleanTranscript(
    userInput.trim() || transcript.trim() || code.trim()
  );
  if (!input) return;

  // Add user's message to the chat
  setMessages((prev) => [
    ...prev,
    {
      sender: "user",
      text: input,
    },
  ]);

  const result = await sendToBackend(input);

  // Update the editor
  setBackendResult(result.editedCode);
  setCode(result.editedCode);
  setUserInput("");

  // Add AI response to the chat
  setMessages((prev) => [
    ...prev,
    {
      sender: "ai",
      text: "Done! I've updated the editor with the generated code.",
    },
  ]);
};

  const toggleMic = () => {
  if (listening) {
    SpeechRecognition.stopListening();
    setListening(false);
    setStatusMessage("Processing...");
    return;
  }

  resetTranscript();

  SpeechRecognition.startListening({
    continuous: false,
    language: "en-US",
  });

  setListening(true);
  setStatusMessage("Listening...");
};
  const copyCode = () => {
  navigator.clipboard.writeText(code);
  alert("Code copied!");
};

const clearAll = () => {
  setCode("// Write your code here");
  setBackendResult("");
  resetTranscript();
  setIntent("");
  setLanguage("");
  setStatus("Idle");

  setMessages([
    {
      sender: "ai",
      text: "Hello! I'm your Voice Coding Assistant. How can I help you today?",
    },
  ]);
};

const newChat = () => {

    const id = crypto.randomUUID();

    setCurrentChatId(id);

    setMessages([
        {
            sender: "ai",
            text: "Hello! I'm your Voice Coding Assistant. How can I help you today?",
        },
    ]);

    setCode("// Write your code here");

    setUserInput("");

    resetTranscript();

    setIntent("");

    setLanguage("");

    setStatus("Idle");
};

  // Live dictation: append new speech lines to editor
  useEffect(() => {
  if (!transcript) return;

  // Just remember the latest transcript.
  lastTranscriptRef.current = transcript;
  }, [transcript]);

  useEffect(() => {
  if (!SpeechRecognition.listening && listening) {
    setListening(false);

    if (transcript.trim()) {
      setUserInput(transcript);
    }
  }
}, [transcript, listening]);

  useEffect(() => {
    if (!SpeechRecognition.listening && listening) {
      setListening(false);
    }
  }, [listening]);

  useEffect(() => {
  localStorage.setItem(
    "vcai-chat-history",
    JSON.stringify(chatHistory)
  );
}, [chatHistory]);

 useEffect(() => {

  const savedChats = localStorage.getItem("vcai-chat-history");

  if (savedChats) {

    const chats = JSON.parse(savedChats);

    setChatHistory(chats);

    if (chats.length > 0) {

      const latest = chats[chats.length - 1];

      setCurrentChatId(latest.id);

      setMessages(latest.messages);

      setCode(latest.code);
    }

  }

}, []);

 useEffect(() => {
  if (!currentChatId) return;

  const firstUserMessage = messages.find(
    (m) => m.sender === "user"
  );

  if (!firstUserMessage) return;

  setChatHistory((prev) => {

    const index = prev.findIndex(
      (chat) => chat.id === currentChatId
    );

    // Chat already exists → update it
    if (index !== -1) {

      const updated = [...prev];

      updated[index] = {
        ...updated[index],
        title: firstUserMessage.text,
        messages,
        code,
      };

      return updated;
    }

    // New chat → create it
    return [
      ...prev,
      {
        id: currentChatId,
        title: firstUserMessage.text,
        messages,
        code,
      },
    ];
  });

}, [messages, code, currentChatId]);

 return (
  <Home
    code={code}
    setCode={setCode}
    transcript={transcript}
    backendResult={backendResult}
    statusMessage={statusMessage}
    loading={loading}
    listening={listening}
    runAI={runAI}
    toggleMic={toggleMic}
    intent={intent}
    language={language}
    status={status}
    backendConnected={backendConnected}
    copyCode={copyCode}
    clearAll={clearAll}
    messages={messages}
    userInput={userInput}
    setUserInput={setUserInput}
    chatHistory={chatHistory}
    newChat={newChat}
    setMessages={setMessages}
    setCode={setCode}
    setCurrentChatId={setCurrentChatId}
  />
);
}   // <-- This closing brace is missing

export default App;

