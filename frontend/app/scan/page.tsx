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
    } catch (err: any) {
      setError(err.message || "Something went wrong!");
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4">
      <h1 className="text-2xl font-bold mb-4">Scan an Image</h1>

      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="mb-4"
      />

      <button
        onClick={handleSubmit}
        className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
      >
        Submit
      </button>

      {error && <p className="text-red-500 mt-4">{error}</p>}

      {prediction && (
        <div className="mt-6">
          <p className="text-xl font-semibold">Prediction: {prediction}</p>
        </div>
      )}

      {heatmap && (
        <div className="mt-6">
          <p className="text-xl font-semibold mb-4">Heatmap:</p>
          <img src={`data:image/png;base64,${heatmap}`} alt="HiRes-CAM Heatmap" />
        </div>
      )}
    </div>
  );
}
