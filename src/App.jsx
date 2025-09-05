import { useState } from "react";
import Editor from "@monaco-editor/react";

export default function App() {
  const [code, setCode] = useState("// Write your JavaScript code here...");
  const [output, setOutput] = useState("");

const runCode = () => {
  const logs = [];
  const originalLog = console.log;
  console.log = (...args) => {
    logs.push(args.join(" "));
    originalLog(...args);
  };

  try {
    // eslint-disable-next-line no-eval
    // Evaluate the code entered by the user
    // Use Function constructor to provide a safer scope than eval
    // eslint-disable-next-line no-new-func
    new Function(code)();
    setOutput(logs.length > 0 ? logs.join("\n") : "No output");
  } catch (error) {
    setOutput(error.toString());
  }

  console.log = originalLog; // Restore original console.log
};


  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
      <h1 className="text-3xl font-bold mb-6">Online Code Editor</h1>
      
      {/* Code Editor */}
      <div className="w-full max-w-4xl h-[400px] border rounded-lg shadow-lg overflow-hidden">
        <Editor
          height="100%"
          language="javascript"
          value={code}
          onChange={(value) => setCode(value || "")}
          theme="vs-dark"
        />
      </div>

      {/* Run Button */}
      <button
        onClick={runCode}
        className="mt-4 px-6 py-2 bg-blue-500 text-white rounded-lg shadow hover:bg-blue-600 transition"
      >
        Run Code
      </button>

      {/* Output Box */}
      <div className="w-full max-w-4xl bg-white mt-6 p-4 border rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-2">Output:</h2>
        <pre className="text-gray-800">{output}</pre>
      </div>
    </div>
  );
}
