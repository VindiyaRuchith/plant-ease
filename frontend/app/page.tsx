"use client";

import Link from "next/link";
import { AuroraBackground } from "@/components/ui/aurora-background";
import { Boxes } from "@/components/ui/background-boxes";

export default function AuroraBackgroundDemo() {
  return (
    <AuroraBackground>
      <h1 className="text-4xl font-bold text-green-600 text-center mb-10">
        PLANT-EASE
      </h1>

      <div className="max-w-5xl mx-auto px-4 grid grid-cols-1 md:grid-cols-2 gap-8 relative z-10">
        {/* Container 1 */}
        <div
          className="bg-cover bg-center rounded-xl shadow-lg overflow-hidden transform hover:scale-105 transition duration-500"
          style={{ backgroundImage: `url("/cinnamon.jpg")` }}
        >
          <div className="bg-black/50 flex flex-col justify-center items-center h-full p-8 text-white text-center">
            <h2 className="text-2xl font-semibold mb-4">Scan Your Image</h2>
            <p className="mb-4">Instantly check your cinnamon plant&apos;s health with AI-powered image scanning.</p>
            <Link
              href="/scan"
              className="px-6 py-3 bg-blue-500 hover:bg-blue-700 rounded-full shadow-md text-white transition-all transform hover:scale-105"
            >
              Scan Now
            </Link>
          </div>
        </div>

        {/* Container 2 */}
        <div
          className="bg-cover bg-center rounded-xl shadow-lg overflow-hidden transform hover:scale-105 transition duration-500"
          style={{ backgroundImage: `url("/cinnamon.jpg")` }}
        >
          <div className="bg-black/50 flex flex-col justify-center items-center h-full p-8 text-white text-center">
            <h2 className="text-2xl font-semibold mb-4">About Us</h2>
            <p className="mb-4">Learn more about how PLANT-EASE supports sustainable farming with cutting-edge technology.</p>
            <Link
              href="/about"
              className="px-6 py-3 bg-blue-500 hover:bg-blue-700 rounded-full shadow-md text-white transition-all transform hover:scale-105"
            >
              Learn More
            </Link>
          </div>
        </div>

        {/* Container 3 */}
        <div
          className="bg-cover bg-center rounded-xl shadow-lg overflow-hidden transform hover:scale-105 transition duration-500"
          style={{ backgroundImage: `url("/cinnamon.jpg")` }}
        >
          <div className="bg-black/50 flex flex-col justify-center items-center h-full p-8 text-white text-center">
            <h2 className="text-2xl font-semibold mb-4">Terms of Service</h2>
            <p className="mb-4">Understand how we ensure responsible use and data protection in PLANT-EASE.</p>
            <Link
              href="/terms"
              className="px-6 py-3 bg-blue-500 hover:bg-blue-700 rounded-full shadow-md text-white transition-all transform hover:scale-105"
            >
              Read Terms
            </Link>
          </div>
        </div>

        {/* Container 4 */}
        <div
          className="bg-cover bg-center rounded-xl shadow-lg overflow-hidden transform hover:scale-105 transition duration-500"
          style={{ backgroundImage: `url("/cinnamon.jpg")` }}
        >
          <div className="bg-black/50 flex flex-col justify-center items-center h-full p-8 text-white text-center">
            <h2 className="text-2xl font-semibold mb-4">Get Support</h2>
            <p className="mb-4">Need help using the app? Check out our comprehensive guides and resources.</p>
            <Link
              href="/howto"
              className="px-6 py-3 bg-blue-500 hover:bg-blue-700 rounded-full shadow-md text-white transition-all transform hover:scale-105"
            >
              View Help
            </Link>
          </div>
        </div>
      </div>

      <Boxes />
    </AuroraBackground>
  );
}
