"use client";

import { Swiper, SwiperSlide } from "swiper/react";
import { Pagination, Autoplay, Navigation } from "swiper/modules";
import "swiper/css";
import "swiper/css/pagination";
import "swiper/css/navigation"; // Import navigation styles

import { AuroraBackground } from "@/components/ui/aurora-background";
import { Boxes } from "@/components/ui/background-boxes";

export default function AuroraBackgroundDemo() {
  return (
    <AuroraBackground>
      {/* Swiper Carousel */}
      <div className="w-full max-w-3xl relative">
        <Swiper
          modules={[Pagination, Autoplay, Navigation]}
          spaceBetween={20}
          slidesPerView={1}
          pagination={{ clickable: true }}
          autoplay={{ delay: 3000 }}
          navigation // Enables left & right arrows
          className="rounded-lg shadow-lg w-full max-w-3xl h-[400px]"
        >
          {/* Slide 1 */}
          <SwiperSlide>
            <div className="h-full flex items-center justify-center">
              <div
                className="text-center text-white flex flex-col justify-center items-center w-full h-full"
                style={{
                  backgroundImage: `url("/cinnamon.jpg")`,
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
                  backgroundImage: `url("/cinnamon.jpg")`,
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
                  Learn More About Us
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
                  backgroundImage: `url("/cinnamon.jpg")`,
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
                  Read Our Terms of Service
                </a>
              </div>
            </div>
          </SwiperSlide>
        </Swiper>
      </div>

      <Boxes />
    </AuroraBackground>
  );
}
