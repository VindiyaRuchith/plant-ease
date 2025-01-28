"use client";

import Image from "next/image";
import { useState } from "react";

export default function Home() {
  const [currentSlide, setCurrentSlide] = useState(0);

  const slides = [
    { title: "Scan-Leaf", link: "/scan" },
    { title: "About-Us", link: "/terms" },
    { title: "Terms-of-Service", link: "/terms" },
  ];

  const nextSlide = () => setCurrentSlide((prev) => (prev + 1) % slides.length);
  const prevSlide = () =>
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);

  return (
    <div
      className="flex items-center justify-center min-h-screen p-8"
      style={{
        backgroundImage: "url('/R.jpg')",
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      {/* Main Card */}
      <div
        className="w-full max-w-screen-md p-8 shadow-2xl backdrop-blur-md rounded-2xl animate-fadeIn"
        style={{
          background: "linear-gradient(135deg, #d4f7dc, #a8e6b1)",
        }}
      >
        {/* Header Section */}
        <header className="flex flex-col items-center gap-4 mb-8">
          <Image
            src="/DALL·E 2025-01-28 21.11.34 - A modern and sleek word logo for 'PLANT-EASE', incorporating a natural and eco-friendly theme. The text 'PLANT-EASE' is styled with a combination of g.webp"
            alt="App logo"
            width={180}
            height={38}
            priority
          />
          <p className="text-center text-gray-700 font-semibold text-lg">
            Empowering farmers and estate owners with advanced AI for detecting 
            and managing cinnamon diseases effectively.
          </p>
        </header>

        {/* Carousel Section */}
        <div
          className="relative w-full max-w-lg p-6 shadow-lg rounded-xl mx-auto animate-slideUp"
          style={{
            background: "linear-gradient(to right,rgb(95, 47, 2),rgb(214, 126, 78))",
          }}
        >
          {/* Left Arrow */}
          <button
            className="absolute top-1/2 left-4 transform -translate-y-1/2 text-3xl text-white hover:scale-110 transition-transform"
            onClick={prevSlide}
            aria-label="Previous Slide"
          >
            {"<"}
          </button>

          {/* Slide Content */}
          <div
          className="text-center text-white animate-fadeIn"
          style={{
            background: "linear-gradient(145deg,rgb(5, 101, 16),rgb(49, 233, 52))",
            padding: "20px",
            borderRadius: "10px",
          }}
          >
          <h2 className="text-3xl font-extrabold text-shadow-lg mb-4">
          {slides[currentSlide].title}
          </h2>
          <p className="mt-2 text-lg leading-relaxed font-semibold">
          Ready to explore the next step?{" "}
          </p>
          <a
          href={slides[currentSlide].link}
          className="inline-block mt-4 px-6 py-3 text-lg font-medium text-white bg-blue-500 hover:bg-blue-700 rounded-full shadow-md transition-all transform hover:scale-105"
          >
            Go to {slides[currentSlide].title}
          </a>
          </div>



          {/* Right Arrow */}
          <button
            className="absolute top-1/2 right-4 transform -translate-y-1/2 text-3xl text-white hover:scale-110 transition-transform"
            onClick={nextSlide}
            aria-label="Next Slide"
          >
            {">"}
          </button>
        </div>

        {/* Interactive Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mt-8">
          <a
            className="bg-gradient-to-r from-green-400 to-blue-500 text-white rounded-full px-6 py-3 font-semibold shadow-lg hover:scale-105 transition-transform"
            href="https://vercel.com/new?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
            target="_blank"
            rel="noopener noreferrer"
          >
            Deploy Now
          </a>
          <a
            className="bg-gray-200 rounded-full px-6 py-3 font-semibold shadow-lg hover:bg-gray-300 hover:scale-105 transition-transform"
            href="https://nextjs.org/docs?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
            target="_blank"
            rel="noopener noreferrer"
          >
            Read Docs
          </a>
        </div>

        {/* Footer Section */}
        <footer className="flex flex-wrap items-center justify-center gap-4 mt-8 text-sm">
          <a
            href="https://nextjs.org/learn"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:text-blue-700 transition"
          >
            Learn
          </a>
          <a
            href="https://vercel.com/templates"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:text-blue-700 transition"
          >
            Templates
          </a>
          <a
            href="https://nextjs.org"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:text-blue-700 transition"
          >
            Visit Next.js →
          </a>
        </footer>
      </div>
    </div>
  );
}
