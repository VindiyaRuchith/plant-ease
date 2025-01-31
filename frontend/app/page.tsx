"use client";

import { motion } from "framer-motion";
import { Boxes } from "@/components/ui/background-boxes";
import { AuroraBackground } from "@/components/ui/aurora-background";
import { Swiper, SwiperSlide } from "swiper/react";
import { Pagination, Autoplay } from "swiper/modules";
import "swiper/css";
import "swiper/css/pagination";

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
            {/* Slide 1 */}
            <SwiperSlide>
              <div className="h-full flex items-center justify-center">
                <div
                  className="text-center text-white flex flex-col justify-center items-center w-full h-full"
                  style={{
                    backgroundImage: `url("/cinnamon.jpg")`, // Replace with your image file name
                    backgroundSize: "cover",
                    backgroundPosition: "center",
                    borderRadius: "10px",
                    height: "100%",
                    width: "100%",
                  }}
                >
                  <a
                    href="/scan"
                    className="inline-block mt-4 px-6 py-3 text-lg font-medium text-white bg-blue-500 hover:bg-blue-700 rounded-full shadow-md transition-all transform hover:scale-105"
                  >
                    Scan Your Image Now
                  </a>
                </div>
              </div>
            </SwiperSlide>

            {/* Slide 2 */}
            <SwiperSlide>
              <div className="h-full flex items-center justify-center">
                <div
                  className="text-center text-white flex flex-col justify-center items-center w-full h-full"
                  style={{
                    backgroundImage: `url("/cinnamon.jpg")`, // Replace with your image file name
                    backgroundSize: "cover",
                    backgroundPosition: "center",
                    borderRadius: "10px",
                    height: "100%",
                    width: "100%",
                  }}
                >
                  <a
                    href="/about"
                    className="inline-block mt-4 px-6 py-3 text-lg font-medium text-white bg-blue-500 hover:bg-blue-700 rounded-full shadow-md transition-all transform hover:scale-105"
                  >
                    Learn More About-Us
                  </a>
                </div>
              </div>
            </SwiperSlide>

            {/* Slide 3 */}
            <SwiperSlide>
              <div className="h-full flex items-center justify-center">
                <div
                  className="text-center text-white flex flex-col justify-center items-center w-full h-full"
                  style={{
                    backgroundImage: `url("/cinnamon.jpg")`, // Replace with your image file name
                    backgroundSize: "cover",
                    backgroundPosition: "center",
                    borderRadius: "10px",
                    height: "100%",
                    width: "100%",
                  }}
                >
                  <a
                    href="/terms"
                    className="inline-block mt-4 px-6 py-3 text-lg font-medium text-white bg-blue-500 hover:bg-blue-700 rounded-full shadow-md transition-all transform hover:scale-105"
                  >
                    Read Our Terms-of-Service
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
