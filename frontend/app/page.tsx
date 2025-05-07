"use client"; // Enables client-side rendering in Next.js 13+

// Import Swiper components and required modules
import { Swiper, SwiperSlide } from "swiper/react";
import { Pagination, Autoplay, Navigation } from "swiper/modules";

// Swiper styles
import "swiper/css";
import "swiper/css/pagination";
import "swiper/css/navigation";

// Next.js router for navigation links
import Link from "next/link";

// Custom background components
import { AuroraBackground } from "@/components/ui/aurora-background";
import { Boxes } from "@/components/ui/background-boxes";

export default function AuroraBackgroundDemo() {
  return (
    // Wrap everything in a custom animated background component
    <AuroraBackground>
      {/* Container centered on screen with padding */}
      <div className="w-full max-w-4xl mx-auto px-4 relative z-10">

        {/*Swiper carousel setup*/}
        <Swiper
          // Enable pagination, autoplay, and arrows
          modules={[Pagination, Autoplay, Navigation]} 
          // Space between slides
          spaceBetween={20}
          // Only one slide visible at a time 
          slidesPerView={1} 
          // Dots are clickable
          pagination={{ clickable: true }} 
          // Slides auto-change every 3 seconds
          autoplay={{ delay: 3000 }} 
          // Show next/previous arrows
          navigation 
          className="rounded-lg shadow-lg w-full h-[400px]" // Styling
        >

          {/*Slide 1*/}
          <SwiperSlide>
            <div className="h-full flex items-center justify-center">
              <div
                className="text-center text-white flex flex-col justify-center items-center w-full h-full"
                style={{
                  // Background image
                  backgroundImage: `url("/public/cinnamon.jpg")`, 
                  backgroundSize: "cover",
                  backgroundPosition: "center",
                  borderRadius: "10px",
                  height: "100%",
                  width: "100%",
                }}
              >
                {/*Link to the scan page*/}
                <Link
                  href="/scan"
                  className="inline-block mt-4 px-6 py-3 text-lg font-medium text-white bg-blue-500 hover:bg-blue-700 rounded-full shadow-md transition-all transform hover:scale-105"
                >
                  Scan Your Image Now
                </Link>
              </div>
            </div>
          </SwiperSlide>

          {/*Slide 2*/}
          <SwiperSlide>
            <div className="h-full flex items-center justify-center">
              <div
                className="text-center text-white flex flex-col justify-center items-center w-full h-full"
                style={{
                  // Reusing the same image
                  backgroundImage: `url("/public/cinnamon.jpg")`, 
                  backgroundSize: "cover",
                  backgroundPosition: "center",
                  borderRadius: "10px",
                  height: "100%",
                  width: "100%",
                }}
              >
                {/*Link to the about page*/}
                <Link
                  href="/about"
                  className="inline-block mt-4 px-6 py-3 text-lg font-medium text-white bg-blue-500 hover:bg-blue-700 rounded-full shadow-md transition-all transform hover:scale-105"
                >
                  Learn More About Us
                </Link>
              </div>
            </div>
          </SwiperSlide>

          {/*Slide 3*/}
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
                {/* Link to the terms page */}
                <Link
                  href="/terms"
                  className="inline-block mt-4 px-6 py-3 text-lg font-medium text-white bg-blue-500 hover:bg-blue-700 rounded-full shadow-md transition-all transform hover:scale-105"
                >
                  Read Our Terms of Service
                </Link>
              </div>
            </div>
          </SwiperSlide>

          {/*Slide 4*/}
          <SwiperSlide>
            <div className="h-full flex items-center justify-center">
              <div
                className="text-center text-white flex flex-col justify-center items-center w-full h-full"
                style={{
                  // Reusing the same image
                  backgroundImage: `url("/public/cinnamon.jpg")`, 
                  backgroundSize: "cover",
                  backgroundPosition: "center",
                  borderRadius: "10px",
                  height: "100%",
                  width: "100%",
                }}
              >
                {/*Link to the about page*/}
                <Link
                  href="/howto"
                  className="inline-block mt-4 px-6 py-3 text-lg font-medium text-white bg-blue-500 hover:bg-blue-700 rounded-full shadow-md transition-all transform hover:scale-105"
                >
                  Learn More About Us
                </Link>
              </div>
            </div>
          </SwiperSlide>


        </Swiper>
      </div>

      {/*Background animated box effect*/}
      <Boxes />
    </AuroraBackground>
  );
}

