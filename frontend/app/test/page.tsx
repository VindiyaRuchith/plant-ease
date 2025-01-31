"use client";

import { motion } from "framer-motion";
import { Boxes } from "@/components/ui/background-boxes";
import { cn } from "@/lib/utils";
import React from "react";
import { AuroraBackground } from "@/components/ui/aurora-background";
import { Swiper, SwiperSlide } from "swiper/react";
import { Pagination, Autoplay } from "swiper/modules";
import "swiper/css";
import "swiper/css/pagination";
import { useState } from "react";

export default function AuroraBackgroundDemo() {

  return (
    <AuroraBackground>
      <motion.div
        initial={{ opacity: 0.0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{
          delay: 0.3,
          duration: 0.8,
          ease: "easeInOut",
        }}
        className="relative flex flex-col gap-4 items-center justify-center px-4"
      >
        {/* Swiper Carousel */}
        <div className="w-full max-w-3xl">
          <Swiper
          modules={[Pagination, Autoplay]}
          spaceBetween={20}
          slidesPerView={1}
          pagination={{ clickable: true }}
          autoplay={{ delay: 3000 }}
          className="rounded-lg shadow-lg w-full max-w-3xl h-[400px]" // Adjust height here
          >
            <SwiperSlide>
              {/* Slide Content */}
              <div className="h-full flex items-center justify-center">
                <div
                className="text-center text-white animate-fadeIn flex flex-col justify-center items-center w-full h-full"
                style={{
                  background: "linear-gradient(145deg,rgb(73, 73, 242),rgb(81, 161, 240))",
                  padding: "20px",
                  borderRadius: "10px",
                  height: "100%", // Ensures the div fills the SwiperSlide height
                  width: "100%", // Ensures full width
                }}
                >
                  <h2 className="text-3xl font-extrabold text-shadow-lg mb-4">
                    Scan-Leaf
                  </h2>
                  <p className="mt-2 text-lg leading-relaxed font-semibold">
                    Find out what disease your crop suffers from
                  </p>
                  <a
                  href="/scan"
                  className="inline-block mt-4 px-6 py-3 text-lg font-medium text-white bg-blue-500 hover:bg-blue-700 rounded-full shadow-md transition-all transform hover:scale-105"
                  >
                  </a>
                </div>
              </div>
            </SwiperSlide>
            <SwiperSlide>
              {/* Slide Content */}
              <div className="h-full flex items-center justify-center">
                <div
                className="text-center text-white animate-fadeIn flex flex-col justify-center items-center w-full h-full"
                style={{
                  background: "linear-gradient(145deg,rgb(5, 101, 16),rgb(49, 233, 52))",
                  padding: "20px",
                  borderRadius: "10px",
                  height: "100%", // Ensures the div fills the SwiperSlide height
                  width: "100%", // Ensures full width
                }}
                >
                  <h2 className="text-3xl font-extrabold text-shadow-lg mb-4">
                    About-Us
                  </h2>
                  <p className="mt-2 text-lg leading-relaxed font-semibold">
                    Find out more about us
                  </p>
                  <a
                  href="/about"
                  className="inline-block mt-4 px-6 py-3 text-lg font-medium text-white bg-blue-500 hover:bg-blue-700 rounded-full shadow-md transition-all transform hover:scale-105"
                  >
                  </a>
                </div>
              </div>
            </SwiperSlide>
            <SwiperSlide>
              {/* Slide Content */}
              <div className="h-full flex items-center justify-center">
                <div
                className="text-center text-white animate-fadeIn flex flex-col justify-center items-center w-full h-full"
                style={{
                  background: "linear-gradient(145deg,rgb(5, 101, 16),rgb(49, 233, 52))",
                  padding: "20px",
                  borderRadius: "10px",
                  height: "100%", // Ensures the div fills the SwiperSlide height
                  width: "100%", // Ensures full width
                }}
                >
                  <h2 className="text-3xl font-extrabold text-shadow-lg mb-4">
                    Terms-of-Service
                  </h2>
                  <p className="mt-2 text-lg leading-relaxed font-semibold">
                    Read our Terms of Service
                  </p>
                  <a
                  href="terms"
                  className="inline-block mt-4 px-6 py-3 text-lg font-medium text-white bg-blue-500 hover:bg-blue-700 rounded-full shadow-md transition-all transform hover:scale-105"
                  >
                    Go to Terms-of-Service Page
                  </a>
                </div>
              </div>
            </SwiperSlide>
          </Swiper>

        </div>
      </motion.div>
      
      <Boxes />
    </AuroraBackground>
  );
}
