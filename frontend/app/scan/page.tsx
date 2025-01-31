"use client";

import React, { useState } from "react";

export default function ScanPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [prediction, setPrediction] = useState<string | null>(null);
  const [heatmap, setHeatmap] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
      setError(null);
    }
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
        setError("Please upload an image first.");
        return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
        const response = await fetch("http://127.0.0.1:5000/classify", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Failed to classify the image.");
        }

        const data = await response.json();
        setPrediction(data.prediction);
        setHeatmap(data.cam_path);
        setSelectedFile(null); // Clear the file input
    } catch (err: any) {
        setError(err.message || "Something went wrong!");
    }
  };


  return (
    <div className="min-h-screen bg-gradient-to-b from-green-200 to-green-400 flex flex-col items-center justify-center p-6">
      <h1 className="text-4xl font-extrabold text-green-800 mb-6 animate__animated animate__fadeIn">
        Scan an Image
      </h1>

      {/* File input with animated transition */}
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="mb-4 p-4 rounded-md border-2 border-green-500 shadow-md hover:shadow-xl transition-all ease-in-out duration-300 transform hover:scale-105"
      />

      {/* Submit button with hover animation */}
      <button
        onClick={handleSubmit}
        className="bg-green-500 text-white px-6 py-3 rounded-md shadow-md hover:bg-green-600 transition-all ease-in-out duration-300 transform hover:scale-105"
      >
        Submit
      </button>

      {/* Error message with animation */}
      {error && (
        <p className="text-red-500 mt-4 text-lg animate__animated animate__shakeX">
          {error}
        </p>
      )}

      {/* Prediction display with animation */}
      {prediction && (
        <div className="mt-6 animate__animated animate__fadeIn animate__delay-1s">
          <p className="text-xl font-semibold text-green-800">Prediction: {prediction}</p>
        </div>
      )}

      {/* Heatmap display with fade-in animation */}
      {heatmap && (
        <div className="mt-6 animate__animated animate__fadeIn animate__delay-2s">
          <p className="text-xl font-semibold text-green-800 mb-4">Heatmap:</p>
          <img
            src={heatmap ? `data:image/png;base64,${heatmap}` : ""}
            alt="HiRes-CAM Heatmap"
            className="rounded-lg shadow-lg hover:shadow-xl transition-all ease-in-out duration-300 transform hover:scale-105"
          />
        </div>
      )}
    </div>
  );
}
