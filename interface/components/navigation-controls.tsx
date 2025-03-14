"use client"

import { Circle, Clock, Home, ImageIcon, User } from "lucide-react"
import { useState } from "react"

export default function NavigationControls() {
  const [activeIcon, setActiveIcon] = useState<string>("home")

  const icons = [
    { id: "home", icon: Home, label: "Home" },
    { id: "gallery", icon: ImageIcon, label: "Gallery" },
    { id: "record", icon: Circle, label: "Record" },
    { id: "history", icon: Clock, label: "History" },
    { id: "profile", icon: User, label: "Profile" },
  ]

  return (
    <div className="flex justify-around items-center p-4 bg-white rounded-2xl mt-2 shadow-md transition-all duration-300 hover:shadow-lg">
      {icons.map((item) => {
        const Icon = item.icon
        return (
          <button
            key={item.id}
            className={`p-2 relative group transition-all duration-200 ${
              activeIcon === item.id ? "text-purple-600" : "text-gray-500 hover:text-purple-600"
            }`}
            onClick={() => setActiveIcon(item.id)}
          >
            <Icon
              className={`w-6 h-6 transition-all duration-200 ${
                activeIcon === item.id ? "scale-110" : "group-hover:scale-110"
              }`}
            />

            {/* Active indicator dot */}
            {activeIcon === item.id && (
              <span className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-1.5 h-1.5 bg-purple-600 rounded-full" />
            )}

            {/* Tooltip */}
            <span className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-xs py-1 px-2 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none">
              {item.label}
            </span>
          </button>
        )
      })}
    </div>
  )
}

