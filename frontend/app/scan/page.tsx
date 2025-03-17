"use client";

import React, { useState } from "react";
import Image from "next/image"; 
import { FileUpload } from "@/components/ui/file-upload";

export default function ScanPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [prediction, setPrediction] = useState<string | null>(null);
  const [heatmap, setHeatmap] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = (files: File[]) => {
    if (files.length > 0) {
      setSelectedFile(files[0]);
      setError(null);
    }
  };

  const handleSubmit = async (camType: string) => {
    if (!selectedFile) {
      setError("Please upload an image first.");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      const response = await fetch(
        ` https://flask-backend-426544169885.us-central1.run.app/classify?cam_type=${camType}`,
        {
          method: "POST",
          body: formData,
          mode: 'no-cors',
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to classify the image.");
      }

      const data = await response.json();
      setPrediction(data.prediction); 
      setHeatmap(data.cam_path); 
      setSelectedFile(null); 
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Something went wrong!");
      }
    }
  };

  return (
    <div className="w-full min-h-screen bg-gradient-to-b from-green-400 via-green-600 to-green-800">
      <div className="w-full max-w-4xl mx-auto min-h-96 border border-dashed bg-white dark:bg-black border-neutral-200 dark:border-neutral-800 rounded-lg p-6 flex flex-col items-center">
        <h1 className="text-3xl font-extrabold text-green-800 dark:text-green-300 mb-6">
          Scan an Image
        </h1>

        {/* File Upload Component */}
        <FileUpload onChange={handleFileUpload} />

        {/* Buttons for HiRes-CAM and Grad-CAM */}
        <div className="flex gap-4 mt-6">
          <button
            onClick={() => handleSubmit("hires")}
            className="bg-green-500 text-white px-6 py-3 rounded-md shadow-md hover:bg-green-600 transition-all transform hover:scale-105"
          >
            Generate HiRes-CAM
          </button>

          <button
            onClick={() => handleSubmit("gradcam")}
            className="bg-blue-500 text-white px-6 py-3 rounded-md shadow-md hover:bg-blue-600 transition-all transform hover:scale-105"
          >
            Generate Grad-CAM++
          </button>
        </div>

        {/* Error message */}
        {error && <p className="text-red-500 mt-4 text-lg">{error}</p>}

        {/* Prediction display */}
        {prediction && (
          <div className="mt-6">
            <p className="text-xl font-semibold text-green-800 dark:text-green-300">
              Prediction: {prediction}
            </p>
          </div>
        )}

        {/* Heatmap display */}
        {heatmap && (
          <div className="mt-6">
            <p className="text-xl font-semibold text-green-800 dark:text-green-300 mb-4">
              Heatmap:
            </p>
            <Image
              src={`data:image/png;base64,${heatmap}`}
              alt="XAI Heatmap"
              width={500} // Adjust width as needed
              height={300} // Adjust height as needed
              className="rounded-lg shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
            />
          </div>
        )}

        {/* Reset Button */}
        {(prediction || heatmap) && (
          <button
            onClick={() => {
              setSelectedFile(null);
              setPrediction(null);
              setHeatmap(null);
              setError(null);
            }}
            className="bg-red-500 text-white px-6 py-3 rounded-md shadow-md hover:bg-red-600 transition-all transform hover:scale-105 mt-4"
          >
            Upload New Image
          </button>
        )}
      </div>
    </div>
  );
}

