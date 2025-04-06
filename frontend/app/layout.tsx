// Import types for metadata 
import type { Metadata } from "next";

// Import fonts from Google Fonts using next/font
import { Geist, Geist_Mono } from "next/font/google";

// Import global CSS
import "./globals.css";

// Import the sidebar component used across all pages
import Sidebar from '@/components/ui/Sidebar';

// Load font and assign it to a CSS variable
const geistSans = Geist({
  // Custom CSS variable name
  variable: "--font-geist-sans",  
  // Include only Latin subset for smaller size
  subsets: ["latin"],             
});

// Load font for code/monospace styling
const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

// Define metadata for the app 
export const metadata: Metadata = {
  // title for all pages
  title: "PLANT-EASE",          
   // Meta description                   
  description: "Plant Disease Detection App",     
};

// Root layout wraps all pages in the app
export default function RootLayout({
  children,
}: Readonly<{
  // All page content will be passed here
  children: React.ReactNode; 
}>) {
  return (
    // Set language attribute for accessibility and SEO
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {/* Global Sidebar shown on all pages */}
        <Sidebar /> 

        {/* Main content area where each page is rendered */}
        <main className="py-4">
          {children}
        </main>
      </body>
    </html>
  );
}
