// For local developmment

// import type { NextConfig } from "next";

// const isProd = process.env.NODE_ENV === "production";

// const nextConfig: NextConfig = {
//   distDir: "out",
//   output: isProd ? 'export' : undefined,
//   basePath: isProd ? '/plant-ease' : '',
// };

// export default nextConfig;


import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  distDir: "out",
  output: 'export',
  basePath: '/plant-ease',
};

export default nextConfig;
