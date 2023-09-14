// export default Chatbot;
import { useState, useEffect, useRef } from "react";
import axios from "axios";

const Chatbot = ({ chat_type }) => {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  var link = "";
  var initialText = "Hi, how can I help?";

  if (chat_type === "Original") {
    link = "http://127.0.0.1:5001/ask";
  } else if (chat_type === "University") {
    link = "http://127.0.0.1:5002/chat";
    initialText = "Greetings! What would you like to know about the Data Science Department at Prestigia University?";
  }

  const endOfMessagesRef = useRef(null); // Create a reference

  // Use the useEffect hook to scroll to the last message when messages change
  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    const initialMessage = {
      text: initialText,
      name: "Chatbot",
      avatar:
        "https://media.istockphoto.com/vectors/chat-bot-robot-avatar-in-circle-round-shape-isolated-on-white-stock-vector-id1250000899?k=20&m=1250000899&s=170667a&w=0&h=PmKAjrRbSAwobkDCOh55X4GeMXIvLHAHKOIlFc41D7k=",
      uid: "botUID",
    };
    setMessages([initialMessage]);
  }, []);

  const handleAsk = async (e) => {
    e.preventDefault(); // Prevent default form submission

    if (message.trim() === "") return;

    try {
      const response = await axios.post(link, {
        message: message,
      });
      const newMessage = {
        text: message,
        name: "You",
        avatar:
          "https://webstockreview.net/images/happiness-clipart-kind-face-3.jpg",
        uid: "userUID",
      };
      const botMessage = {
        text: response.data.response,
        name: "Chatbot",
        avatar:
          "https://media.istockphoto.com/vectors/chat-bot-robot-avatar-in-circle-round-shape-isolated-on-white-stock-vector-id1250000899?k=20&m=1250000899&s=170667a&w=0&h=PmKAjrRbSAwobkDCOh55X4GeMXIvLHAHKOIlFc41D7k=",
        uid: "botUID",
      };
      setMessages([...messages, newMessage, botMessage]);
      setMessage(""); // Clear the message input
    } catch (error) {
      console.error("Error asking chatbot:", error);
    }
  };

  return (
    <>
      <div className="pb-56">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`chat ${
              msg.uid === "userUID" ? "chat-end" : "chat-start"
            }`}
          >
            <div className="chat-image avatar">
              <div className="w-10 rounded-full">
                <img src={msg.avatar} alt={`${msg.name}'s Avatar`} />
              </div>
            </div>
            <div className="chat-header">{msg.name}</div>
            <div className="chat-bubble">{msg.text}</div>
          </div>
        ))}
        <div ref={endOfMessagesRef}></div> {/* Add the reference here */}
      </div>

      <div className="pt-30">
        <div className="bg-gray-200 fixed bottom-0 w-full py-10 px-10 shadow-lg rounded-md left-0 right-0">
          <form onSubmit={handleAsk} className="px-2 containerWrap flex">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              className="input w-full focus:outline-none bg-gray-100 rounded-r-none"
              placeholder="Ask something..."
            />
            <button
              type="submit"
              className="w-auto bg-gray-500 text-white rounded-r-lg px-5 text-sm"
            >
              Ask
            </button>
          </form>
        </div>
      </div>
    </>
  );
};

export default Chatbot;
