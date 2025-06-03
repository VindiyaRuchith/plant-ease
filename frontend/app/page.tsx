"use client";

import Link from "next/link";
import { AuroraBackground } from "@/components/ui/aurora-background";

export default function AuroraBackgroundDemo() {
  return (
    <AuroraBackground>
      <h1 className="text-4xl font-bold text-green-600 text-center mb-10">
        PLANT-EASE
      </h1>

      <div className="max-w-5xl mx-auto px-4 grid grid-cols-1 md:grid-cols-2 gap-8 relative z-10">
        {[
          {
            title: "Scan Your Image",
            description: "Instantly check your cinnamon plant's health with AI-powered image scanning.",
            link: "/scan",
            button: "Scan Now",
          },
          {
            title: "About Us",
            description: "Learn more about how PLANT-EASE supports sustainable farming with cutting-edge technology.",
            link: "/about",
            button: "Learn More",
          },
          {
            title: "Terms of Service",
            description: "Understand how we ensure responsible use and data protection in PLANT-EASE.",
            link: "/terms",
            button: "Read Terms",
          },
          {
            title: "Get Support",
            description: "Need help using the app? Check out our comprehensive guides and resources.",
            link: "/howto",
            button: "View Help",
          },
        ].map((card, index) => (
          <div
            key={index}
            className="relative group bg-cover bg-center rounded-xl shadow-lg overflow-hidden transition-transform duration-500 hover:scale-105"
            style={{ backgroundImage: `url("/cinnamon.jpg")` }}
          >
            {/* Light overlay on hover */}
            <div className="absolute inset-0 bg-black/50 group-hover:bg-black/30 transition duration-500"></div>

            {/* Subtle glow effect */}
            <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition duration-500">
              <div className="w-full h-full bg-gradient-to-tr from-blue-400/20 to-purple-400/20 blur-2xl"></div>
            </div>

            {/* Content */}
            <div className="relative z-10 flex flex-col justify-center items-center h-full p-8 text-white text-center">
              <h2 className="text-2xl font-semibold mb-4 drop-shadow-lg">{card.title}</h2>
              <p className="mb-4 drop-shadow-md">{card.description}</p>
              <Link
                href={card.link}
                className="px-6 py-3 bg-blue-500 hover:bg-blue-700 rounded-full shadow-md text-white transition-all transform hover:scale-110 hover:shadow-lg"
              >
                {card.button}
              </Link>
            </div>
          </div>
        ))}
      </div>
    </AuroraBackground>
  );
}
