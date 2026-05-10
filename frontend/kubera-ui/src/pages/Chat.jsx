import React, { useState, useRef, useEffect } from "react";
import { Send, Paperclip, Sparkles } from "lucide-react";
import { suggestions } from "../data/mockData";
import { apiFetch } from "../utils/api";
import kubera from "../assets/kubera.png";

function Chat() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const bottomRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const typeMessage = (text, index) => {
    let i = 0;
    let current = "";

    const interval = setInterval(() => {
      current += text[i];
      i++;

      setMessages((prev) => {
        const updated = [...prev];
        updated[index] = {
          role: "ai",
          content: current,
        };
        return updated;
      });

      if (i >= text.length) {
        clearInterval(interval);
        setLoading(false);
      }
    }, 15);
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file || loading) return;

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: `Uploaded file: ${file.name}`,
      },
    ]);

    try {
      const res = await apiFetch("/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          content: `CSV uploaded successfully.\n${data.inserted || 0} transactions added.\n${data.skipped || 0} rows skipped.`,
        },
      ]);
    } catch (error) {
      console.error("Upload Error:", error);

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          content: "CSV upload failed. Please check your file format.",
        },
      ]);
    } finally {
      setLoading(false);
      e.target.value = "";
    }
  };

  const handleSend = async (customText = "") => {
    const query = customText || input;

    if (!query.trim() || loading) return;

    const userMessage = {
      role: "user",
      content: query,
    };

    const updatedMessages = [...messages, userMessage];

    setMessages(updatedMessages);
    setInput("");
    setLoading(true);

    try {
      const res = await apiFetch("/ask", {
        method: "POST",
        body: JSON.stringify({
          query,
          history: updatedMessages.slice(-6),
        }),
      });

      if (!res.ok) {
        throw new Error("Backend request failed");
      }

      const data = await res.json();

      let fullText = "";

      if (data.answer) {
        const explanation = data.answer.explanation || "";
        const advice = data.answer.advice || "";

        fullText = `Explanation:\n${explanation}\n\nAdvice:\n${advice}`;
      } else {
        fullText = "No response received";
      }

      const aiIndex = updatedMessages.length;

      setMessages((prev) => [...prev, { role: "ai", content: "" }]);

      typeMessage(fullText, aiIndex);
    } catch (error) {
      console.error("Error:", error);

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          content: "Failed to connect to backend.",
        },
      ]);

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

            <h1 className="text-5xl md:text-6xl mb-4 tracking-[0.12em] uppercase text-[#735C00]">
              Kubera AI
            </h1>

            <p className="text-lg md:text-xl italic text-[#735C00]">
              Your AI Financial Companion
            </p>
          </div>

          <div className="flex flex-wrap justify-center gap-4 mt-2 mb-8">
            {suggestions.map((text) => (
              <button
                key={text}
                onClick={() => handleSend(text)}
                className="px-6 py-3 rounded-full border border-stone-200 bg-white text-stone-600 hover:text-[#1A3C34] transition"
              >
                {text}
              </button>
            ))}
          </div>
        </>
      )}

      {messages.length > 0 && (
        <div className="w-full max-w-3xl mb-8 space-y-4 max-h-[60vh] overflow-y-auto pr-2">
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
                    : "bg-[#F9F8F4] border border-stone-200 text-stone-800 rounded-bl-md"
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="max-w-[75%] px-5 py-4 rounded-3xl rounded-bl-md bg-[#F9F8F4] border border-stone-200 text-stone-500 shadow-sm">
                <div className="flex items-center gap-2 animate-pulse">
                  <Sparkles size={16} />
                  Kubera AI is analyzing...
                </div>
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>
      )}

      <div className="w-full max-w-3xl">
        <div className="flex items-center bg-white rounded-[30px] border border-stone-200 shadow-sm px-4 py-4">
          <Paperclip
            className="text-stone-400 mr-4 cursor-pointer hover:text-[#1A3C34]"
            onClick={() => fileInputRef.current.click()}
          />

          <input
            type="file"
            accept=".csv"
            ref={fileInputRef}
            className="hidden"
            onChange={handleFileUpload}
          />

          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleSend();
            }}
            placeholder="Ask Kubera anything..."
            className="flex-1 bg-transparent outline-none text-lg"
          />

          <button
            onClick={() => handleSend()}
            disabled={loading}
            className="bg-[#1A3C34] text-white p-4 rounded-2xl disabled:opacity-50"
          >
            <Send size={22} />
          </button>
        </div>
      </div>
    </div>
  );
}

export default Chat;