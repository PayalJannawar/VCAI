import "../styles/console.css";

function ConsolePanel({
  messages,
  loading,
  userInput,
  setUserInput,
  runAI,
}) {
  return (
    <div className="console-panel card">

      <h2>Assistant</h2>

      <div className="chat-window">

        {messages.map((msg, index) => (
          <div
            key={index}
            className={
              msg.sender === "user"
                ? "user-msg"
                : "ai-msg"
            }
          >
            <div className="msg-title">
              {msg.sender === "user"
                ? "👤 You"
                : "🤖 Assistant"}
            </div>

            <p>{msg.text}</p>
          </div>
        ))}

      {loading && (
        <div className="ai-msg">
          <div className="msg-title">🤖 Assistant</div>
          <p>Thinking...</p>
        </div>
      )}

    </div>

    <div className="chat-input">

      <input
        type="text"
        placeholder="Ask me anything about code..."
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            runAI();
          }
        }}
      />

      <button onClick={runAI}>
        Send
      </button>

    </div>

  </div>
);
}

export default ConsolePanel;