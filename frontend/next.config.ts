// For local developmment

// import type { NextConfig } from "next";

// const isProd = process.env.NODE_ENV === "production";

// const nextConfig: NextConfig = {
//   distDir: "out",
//   output: isProd ? 'export' : undefined,
//   basePath: isProd ? '/plant-ease' : '',
// };

// export default nextConfig;


/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  distDir: 'out',
  basePath: '/plant-ease',
  images: {
    unoptimized: true, // Important for static export!
  },
};

export default nextConfig;
