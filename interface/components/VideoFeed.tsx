import { useEffect, useState } from "react"

export default function VideoFeed() {
  const [videoUrl, setVideoUrl] = useState("")

  useEffect(() => {
    setVideoUrl("http://localhost:5000/video_feed")
  }, [])

  return (
    <div className="w-full rounded-lg overflow-hidden shadow-xl">
      <img
        src={videoUrl}
        alt="Live Video Feed"
        className="w-full h-auto object-cover"
      />
    </div>
  )
}
