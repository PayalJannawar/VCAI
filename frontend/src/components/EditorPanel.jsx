import Editor from "@monaco-editor/react";
import ControlButtons from "./ControlButtons";
import "../styles/editor.css";

function EditorPanel({
  code,
  setCode,
  runAI,
  toggleMic,
  listening,
  loading,
  copyCode,
  clearAll,
}) {
  return (
    <div className="editor-panel card">

      <h2>Code Editor</h2>

      <div className="editor-wrapper">
        <Editor
          height="100%"
          defaultLanguage="javascript"
          value={code}
          onChange={(value) => setCode(value || "")}
          theme="vs-dark"
        />
      </div>

      <ControlButtons
        runAI={runAI}
        toggleMic={toggleMic}
        listening={listening}
        loading={loading}
        copyCode={copyCode}
        clearAll={clearAll}
      />

    </div>
  );
}

export default EditorPanel;