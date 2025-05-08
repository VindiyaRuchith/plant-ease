"use client";

import React from "react";

const HowToUse = () => {
  return (
    <div className="bg-gradient-to-b from-green-100 to-green-300 min-h-screen p-6 flex flex-col items-center justify-center">
      {/* Main content container */}
      <div className="max-w-6xl w-full grid grid-cols-1 md:grid-cols-2 gap-8">

        {/* Demo Video Section */}
        <div className="bg-white rounded-lg shadow-xl p-6">
          <h2 className="text-2xl font-bold text-green-700 mb-4 text-center">Watch the Demo</h2>
          <div className="aspect-w-16 aspect-h-9">
            <iframe 
              src="https://www.youtube.com/embed/767n3Y7qSHk" // Replace with your actual video URL
              title="PLANT-EASE Demo"
              className="w-full h-[360px] rounded-md"
              allowFullScreen
            />
          </div>
        </div>

        {/* Steps Section */}
        <div className="bg-white rounded-lg shadow-xl p-6">
          <h2 className="text-2xl font-bold text-green-700 mb-4 text-center">How to Use PLANT-EASE</h2>
          <ol className="list-decimal list-inside space-y-3 text-gray-700 text-lg">
            <li>Go to the <span className="font-semibold text-green-800">Scan</span> page.</li>
            <li>Click <span className="font-semibold">Upload Image</span>.</li>
            <li>Browse and select the image of the cinnamon leaf.</li>
            <li>Press <span className="font-semibold">OK</span> to confirm.</li>
            <li>Select your preferred XAI method:
              <ul className="list-disc list-inside ml-5 text-sm mt-1">
                <li><span className="font-semibold">HiRes-CAM</span> – Sharper, more localized, and faithful heatmaps.</li>
                <li><span className="font-semibold">Grad-CAM++</span> – Broader, general highlighting.</li>
              </ul>
            </li>
            <li>Click <span className="font-semibold">Upload Image</span> again if you want to analyze a new image.</li>
          </ol>
        </div>
      </div>
    </div>
  );
};

export default HowToUse;