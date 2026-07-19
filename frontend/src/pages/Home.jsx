import "../styles/layout.css";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import EditorPanel from "../components/EditorPanel";
import ConsolePanel from "../components/ConsolePanel";
import ControlButtons from "../components/ControlButtons";

function Home({
  code,
  transcript,
  backendResult,
  statusMessage,
  loading,
  listening,
  runAI,
  toggleMic,
  intent,
  language,
  status,
  backendConnected,
  copyCode,
  clearAll,
  messages,
  userInput,
  setUserInput,
  chatHistory,
  newChat,
  setMessages,
  setCode,
  setCurrentChatId,
}) {
  return (
    <div>
      <Navbar backendConnected={backendConnected} />

      <div className="main-layout">
        <Sidebar
            chatHistory={chatHistory}
            newChat={newChat}
            setMessages={setMessages}
            setCode={setCode}
            setCurrentChatId={setCurrentChatId}
        />

        <EditorPanel
          code={code}
          setCode={setCode}
          runAI={runAI}
          toggleMic={toggleMic}
          listening={listening}
          loading={loading}
          copyCode={copyCode}
          clearAll={clearAll}
        />
        
        
        <ConsolePanel
          messages={messages}
          loading={loading}
          runAI={runAI}
          userInput={userInput}
          setUserInput={setUserInput}
        />
      </div>

      <div
        style={{
          display: "flex",
          justifyContent: "center",
          marginTop: "20px",
        }}
      >
       
      </div>
    </div>
  );
}

export default Home;