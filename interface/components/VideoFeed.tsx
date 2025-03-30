import { useEffect, useState } from "react";
import io from "socket.io-client";

export default function VideoFeed() {
  const [videoUrl, setVideoUrl] = useState("");

  useEffect(() => {
    // Configuração de Socket.IO
    const socket = io("http://localhost:5000", {
      transports: ["websocket"],
    });

    socket.on("connect", () => {
      console.log("Conectado ao servidor Socket.IO");
    });

    socket.on("disconnect", () => {
      console.log("Desconectado do servidor");
    });

    // Configura o URL do feed de vídeo
    setVideoUrl("http://localhost:5000/video_feed");

    // Cleanup ao desconectar
    return () => {
      socket.disconnect();
    };
  }, []);

  return (
    <div className="w-full rounded-lg overflow-hidden shadow-xl">
      <img
        src={videoUrl}
        alt="Live Video Feed"
        className="w-full h-auto object-cover"
      />
    </div>
  );
}
