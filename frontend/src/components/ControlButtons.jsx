import "../styles/buttons.css";

function ControlButtons({
  runAI,
  toggleMic,
  listening,
  loading,
  copyCode,
  clearAll,
}) {
  return (
    <div className="button-group">

      <button
        className="generate-btn"
        onClick={runAI}
        disabled={loading}
      >
        {loading ? "Generating..." : "Generate Code"}
      </button>

      <button
        className={listening ? "stop-btn" : "speak-btn"}
        onClick={toggleMic}
        disabled={loading}
      >
        {listening ? "Stop" : "Speak"}
      </button>

      <button
        className="copy-btn"
        onClick={copyCode}
      >
        Copy
      </button>

      <button
        className="clear-btn"
        onClick={clearAll}
      >
        Clear
      </button>

    </div>
  );
}

export default ControlButtons;