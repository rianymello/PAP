import { useEffect, useState } from "react"
import VideoFeed from "./components/VideoFeed"
import ChatWindow from "./components/chat-window"
import NavigationControls from "./components/navigation-controls"

export default function ChatInterface() {
  const [isLoaded, setIsLoaded] = useState(false)

  useEffect(() => {
    setIsLoaded(true)
  }, [])

  return (
    <div className="w-full min-h-screen bg-gradient-to-br from-gray-800 to-gray-900 p-4 flex items-center justify-center">
      <div
        className={`w-full max-w-6xl h-[600px] rounded-lg overflow-hidden flex flex-col md:flex-row gap-4 transition-all duration-500 ease-in-out ${
          isLoaded ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"
        }`}
      >
        {/* Video Feed - Substituindo a imagem estática pelo streaming do Flask */}
        <div className="w-full md:w-5/6 bg-[#000000] rounded-2xl overflow-hidden shadow-xl transition-all duration-300 hover:shadow-2xl transform hover:-translate-y-1">
          <div className="bg-gray-100 px-4 py-2 flex items-center border-b border-gray-200">
            <div className="flex space-x-2">
              <div className="w-3 h-3 rounded-full bg-red-500"></div>
              <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
            </div>
            <div className="mx-auto text-sm text-gray-500 font-medium">Preview</div>
          </div>
          <VideoFeed />
        </div>

        {/* Chat Panel */}
        <div
          className={`w-full md:w-2/5 flex flex-col transition-all duration-500 delay-100 ${
            isLoaded ? "opacity-100 translate-x-0" : "opacity-0 translate-x-10"
          }`}
        >
          <ChatWindow />
          <NavigationControls />
        </div>
      </div>
    </div>
  )
}
