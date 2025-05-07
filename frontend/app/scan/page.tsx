"use client";

import React, { useState } from "react";
import Image from "next/image";
import { FileUpload } from "@/components/ui/file-upload";
import { X } from "lucide-react"; // Close icon for image preview

export default function ScanPage() {
  // --- State Management ---
  const [selectedFile, setSelectedFile] = useState<File | null>(null); // uploaded image
  const [prediction, setPrediction] = useState<string | null>(null);   // predicted label
  const [heatmap, setHeatmap] = useState<string | null>(null);         // base64 CAM heatmap
  const [error, setError] = useState<string | null>(null);             // error message
  const [isLoading, setIsLoading] = useState(false);                   // loading spinner
  const [resetKey, setResetKey] = useState(0);                         // to reset <FileUpload />

  // --- Handle File Upload ---
  const handleFileUpload = (files: File[]) => {
    if (files.length > 0) {
      const file = files[0];
      if (!file.type.startsWith("image/")) {
        setError("Only image files are allowed.");
        return;
      }
      setSelectedFile(file);
      setError(null); // clear any previous errors
    }
  };

  // --- Submit to Flask Backend ---
  const handleSubmit = async (camType: string) => {
    if (!selectedFile) {
      setError("Please upload an image first.");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);
    setIsLoading(true); // show loading indicator

    try {
      const response = await fetch(
        `https://fyp-556001537402.asia-south1.run.app/classify?cam_type=${camType}`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to classify the image.");
      }

      const data = await response.json();
      setPrediction(data.prediction);  // update result
      setHeatmap(data.cam_path);       // update CAM
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Something went wrong.");
      }
    } finally {
      setIsLoading(false); // stop loading
    }
  };

  // --- Reset Entire State ---
  const handleReset = () => {
    setSelectedFile(null);
    setPrediction(null);
    setHeatmap(null);
    setError(null);
    setResetKey((prev) => prev + 1); // trigger <FileUpload /> to remount
  };

  return (
    <div className="w-full min-h-screen bg-gradient-to-b from-green-400 via-green-600 to-green-800">
      <div className="w-full max-w-4xl mx-auto min-h-96 border border-dashed bg-white dark:bg-black border-neutral-200 dark:border-neutral-800 rounded-lg p-6 flex flex-col items-center">
        
        {/* Page Title */}
        <h1 className="text-3xl font-extrabold text-green-800 dark:text-green-300 mb-6">
          Scan an Image
        </h1>

        {/* File Upload Component (Reset via key) */}
        <FileUpload key={resetKey} onChange={handleFileUpload} />

        {/* Image Preview with Close Icon */}
        {selectedFile && (
          <div className="relative mt-4">
            <p className="text-sm text-gray-700 mb-2 text-center">Selected Image:</p>
            <div className="relative inline-block">
              <Image
                src={URL.createObjectURL(selectedFile)}
                alt="Selected"
                width={300}
                height={200}
                className="rounded-lg border shadow"
              />
              <button
                onClick={() => {
                  setSelectedFile(null);
                  setResetKey((prev) => prev + 1); // also reset file name
                }}
                className="absolute top-1 right-1 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 transition"
                aria-label="Remove image"
              >
                <X size={16} />
              </button>
            </div>
          </div>
        )}

        {/* XAI Method Buttons */}
        <div className="flex gap-4 mt-6">
          <button
            onClick={() => handleSubmit("hires")}
            disabled={!selectedFile || isLoading}
            className={`bg-green-500 text-white px-6 py-3 rounded-md shadow-md transition-all transform hover:scale-105 ${
              !selectedFile || isLoading ? "opacity-50 cursor-not-allowed" : "hover:bg-green-600"
            }`}
          >
            Generate HiRes-CAM
          </button>

          <button
            onClick={() => handleSubmit("gradcam")}
            disabled={!selectedFile || isLoading}
            className={`bg-blue-500 text-white px-6 py-3 rounded-md shadow-md transition-all transform hover:scale-105 ${
              !selectedFile || isLoading ? "opacity-50 cursor-not-allowed" : "hover:bg-blue-600"
            }`}
          >
            Generate Grad-CAM++
          </button>
        </div>

        {/* Loading Indicator */}
        {isLoading && (
          <p className="text-yellow-400 mt-4 text-lg">Processing image...</p>
        )}

        {/* Error Message */}
        {error && <p className="text-red-500 mt-4 text-lg">{error}</p>}

        {/* Prediction Text */}
        {prediction && (
          <div className="mt-6">
            <p className="text-xl font-semibold text-green-800 dark:text-green-300">
              Prediction: {prediction}
            </p>
          </div>
        )}

        {/* Heatmap Display */}
        {heatmap && (
          <div className="mt-6">
            <p className="text-xl font-semibold text-green-800 dark:text-green-300 mb-4">
              Heatmap:
            </p>
            <Image
              src={`data:image/png;base64,${heatmap}`}
              alt="XAI Heatmap"
              width={500}
              height={300}
              className="rounded-lg shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
            />

            {/* Heatmap Legend */}
            <div className="mt-4 flex flex-col items-center">
              <div className="flex w-60 h-4 bg-gradient-to-r from-blue-600 via-green-200 to-red-600 rounded-full shadow-inner" />
              <div className="flex justify-between w-60 text-xs mt-1 text-gray-600 dark:text-gray-300">
                <span>Less Important</span>
                <span>Medium Importance</span>
                <span>Most Important</span>
              </div>
            </div>
          </div>
        )}

        {/* Reset Button */}
        {(prediction || heatmap || selectedFile) && (
          <button
            onClick={handleReset}
            className="bg-red-500 text-white px-6 py-3 rounded-md shadow-md hover:bg-red-600 transition-all transform hover:scale-105 mt-6"
          >
            Upload New Image
          </button>
        )}
      </div>
    </div>
  );
}
