"use client"

import { useState, useRef, useEffect } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Send, Smile } from "lucide-react"
import { io } from "socket.io-client"

type MessageType = "system" | "user"

interface Message {
  id: string
  content: string
  type: MessageType
  timestamp: Date
}

export default function ChatWindow() {
  const [message, setMessage] = useState("")
  const [messages, setMessages] = useState<Message[]>([])
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const socket = useRef(io("http://localhost:5000"))

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom()

    socket.current.on('chat_message', (data: { content: string }) => {
      const newMessage: Message = {
        id: Date.now().toString(),
        content: data.content,
        type: "system",
        timestamp: new Date(),
      }
      setMessages((prevMessages) => [...prevMessages, newMessage])
    })

    return () => {
      socket.current.disconnect()
    }
  }, [])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  const handleSendMessage = () => {
    if (message.trim()) {
      // Adiciona nova mensagem ao estado
      const newMessage: Message = {
        id: Date.now().toString(),
        content: message,
        type: "user",
        timestamp: new Date(),
      }

      setMessages([...messages, newMessage])
      setMessage("") // Limpa o campo de entrada
    }
  }

  // Formatar o timestamp para exibir de forma legível
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
  }

  return (
    <div className="flex-1 flex flex-col bg-gray-100 rounded-2xl overflow-hidden shadow-md transition-all duration-300 hover:shadow-lg">
      {/* Chat Header */}
      <div className="p-4 bg-white border-b border-gray-200">
        <div className="flex items-center gap-2">
          <div className="flex gap-1">
            <div className="w-4 h-4 rounded-full bg-purple-600 animate-pulse"></div>
            <div className="w-4 h-4 rounded-full bg-gray-800"></div>
          </div>
          <span className="font-semibold text-lg">Zoia</span>
          <span className="text-xs bg-green-100 text-green-800 px-2 py-0.5 rounded-full ml-2">Online</span>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`px-4 py-2 shadow-sm transform transition-all duration-300 hover:-translate-y-1 hover:shadow-md ${
              msg.type === "system" ? "bg-white rounded-lg" : "bg-purple-100 rounded-lg ml-auto max-w-[80%]"
            }`}
          >
            <p>{msg.content}</p>
            <p className="text-xs text-gray-500 mt-1">{formatTime(msg.timestamp)}</p>
          </div>
        ))}
        <div ref={messagesEndRef} /> {/* Empty div for scrolling to bottom */}
      </div>

      {/* Chat Input */}
      <div className="p-4 bg-white border-t border-gray-200">
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon" className="text-gray-500">
            <Smile className="h-5 w-5" />
          </Button>
          <Input
            placeholder="Type your message here..."
            className="w-full bg-gray-50 focus:ring-2 focus:ring-purple-500 transition-all duration-200"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
          />
          <Button
            variant="ghost"
            size="icon"
            className={`${message.trim() ? "text-purple-600" : "text-gray-400"} transition-colors duration-200`}
            onClick={handleSendMessage}
            disabled={!message.trim()}
          >
            <Send className="h-5 w-5" />
          </Button>
        </div>
      </div>
    </div>
  )
}
