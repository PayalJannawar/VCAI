import "../styles/navbar.css";

function Navbar({ backendConnected }) {
  return (
    <nav className="navbar">

      <div className="navbar-left">
        <span className="logo">🎤</span>
        <h2>Voice Coding Assistant</h2>
      </div>

      <div className="navbar-right">

        <div className="status">
          
          <span
            style={{
                color: backendConnected ? "#22c55e" : "#ef4444",
                fontWeight: "600",
            }}
          >
            {backendConnected
               ? "● Backend Connected"
               : "● Backend Offline"}
         </span>
        </div>

        <button className="launch-btn">
          Launch Assistant
        </button>

      </div>

    </nav>
  );
}

export default Navbar;