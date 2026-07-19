import "../styles/sidebar.css";

function Sidebar({
  chatHistory,
  newChat,
  setMessages,
  setCode,
}) {

  return (
    <div className="sidebar card">

      <h2>Chats</h2>

      <button
        className="new-chat-btn"
        onClick={newChat}
      >
        + New Chat
      </button>

      <div className="chat-history">

        <h4>TODAY'S CHATS</h4>

        {chatHistory.length === 0 ? (

          <p className="empty-chat">
            No chats yet
          </p>

        ) : (

          chatHistory
            .slice()
            .reverse()
            .map((chat) => (

              <div
                key={chat.id}
                className="chat-item"
                onClick={() => {
                
                  setCurrentChatId(chat.id);

                  setMessages(chat.messages);

                  setCode(chat.code);

                }}
              >
                {chat.title}
              </div>

            ))

        )}

      </div>

    </div>
  );
}

export default Sidebar;