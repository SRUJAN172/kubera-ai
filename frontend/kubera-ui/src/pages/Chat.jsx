import React, { useState } from "react";
import { Send, Paperclip, Sparkles } from "lucide-react";
import { suggestions } from "../data/mockData";
import kubera from "../assets/kubera.png";

function Chat() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async (customText = "") => {
    const query = customText || input;

    if (!query.trim() || loading) return;

    const userMessage = {
      role: "user",
      content: query,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/ask?query=${encodeURIComponent(query)}`
      );

      if (!res.ok) {
        throw new Error("Backend request failed");
      }

      const data = await res.json();

      const aiMessage = {
        role: "ai",
        content: data.answer || data.response || "No response received",
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error("Error:", error);

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          content: "Failed to connect to backend.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto min-h-[75vh] flex flex-col items-center justify-center text-center">
      {messages.length === 0 && (
        <>
          <div className="mb-12">
            <div className="flex justify-center">
              <img
                src={kubera}
                alt="Kubera"
                className="w-40 md:w-52 mb-6 opacity-90"
              />
            </div>

            <h1
              className="text-5xl md:text-6xl mb-4 tracking-[0.12em] uppercase text-[#735C00]"
              style={{ fontFamily: '"Playfair Display", serif' }}
            >
              Kubera AI
            </h1>

            <p
              className="text-lg md:text-xl italic text-[#735C00]"
              style={{ fontFamily: '"Playfair Display", serif' }}
            >
              Your AI Financial Companion
            </p>
          </div>

          <div className="flex flex-wrap justify-center gap-4 mt-2 mb-8">
            {suggestions.map((text) => (
              <button
                key={text}
                onClick={() => handleSend(text)}
                className="px-6 py-3 rounded-full border border-stone-200 bg-white text-stone-600 hover:text-[#1A3C34] hover:border-[#1A3C34]/20 transition"
              >
                {text}
              </button>
            ))}
          </div>
        </>
      )}

      {messages.length > 0 && (
        <div className="w-full max-w-3xl mb-8 space-y-4">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${
                msg.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[75%] px-5 py-4 rounded-3xl shadow-sm whitespace-pre-line text-left ${
                  msg.role === "user"
                    ? "bg-[#1A3C34] text-white rounded-br-md"
                    : "bg-white border border-stone-200 text-stone-700 rounded-bl-md"
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="max-w-[75%] px-5 py-4 rounded-3xl rounded-bl-md bg-white border border-stone-200 text-stone-500 shadow-sm">
                Thinking...
              </div>
            </div>
          )}
        </div>
      )}

      <div className="w-full max-w-3xl">
        <div className="flex items-center bg-white rounded-[30px] border border-stone-200 shadow-sm px-4 py-4">
          <Paperclip className="text-stone-400 mr-4 cursor-pointer hover:text-[#1A3C34]" />

          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleSend();
            }}
            placeholder="Ask Kubera anything about your finances..."
            className="flex-1 bg-transparent outline-none text-lg placeholder:text-stone-400"
          />

          <button
            onClick={() => handleSend()}
            disabled={loading}
            className="bg-[#1A3C34] text-white p-4 rounded-2xl hover:scale-105 transition-transform shadow-sm disabled:opacity-50"
          >
            <Send size={22} />
          </button>
        </div>
      </div>

      {messages.length === 0 && (
        <div className="mt-14 flex items-center gap-3 text-xs text-stone-400 uppercase tracking-[0.28em]">
          <div className="h-px w-8 bg-stone-300" />
          <Sparkles size={14} className="text-[#735C00]" />
          Secure &amp; Private Encryption
          <div className="h-px w-8 bg-stone-300" />
        </div>
      )}
    </div>
  );
}

export default Chat;