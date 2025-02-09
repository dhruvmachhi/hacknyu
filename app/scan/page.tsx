// app/scan/page.tsx
'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import ProgressBar from '@/components/ProgressBar';
import { ArrowLeft } from 'lucide-react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Camera } from 'lucide-react';

const steps = [
  "Introduction",
  "Scan Face",
  "Measurements",
  "Design",
  "Review",
];

export default function ScanPage() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const router = useRouter();
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Request access to the user's webcam.
  useEffect(() => {
    async function initCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.onloadedmetadata = () => {
            videoRef.current?.play();
          };
        }
      } catch (err) {
        console.error("Error accessing the camera:", err);
        setError("Error accessing the camera. Please allow camera access and try again.");
      }
    }
    initCamera();
  }, []);

  const startScan = async () => {
    setScanning(true);
    setError(null);
    try {
      if (!videoRef.current) {
        setError("Video not available.");
        setScanning(false);
        return;
      }
      const video = videoRef.current;
      // Ensure the video is ready (non-zero dimensions)
      if (video.videoWidth === 0 || video.videoHeight === 0) {
        setError("Video not ready. Please wait a moment and try again.");
        setScanning(false);
        return;
      }
      // Capture a frame from the video stream.
      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext('2d');
      if (!ctx) {
        setError("Could not get canvas context.");
        setScanning(false);
        return;
      }
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      const imageDataUrl = canvas.toDataURL('image/jpeg');

      // Send the image to your Flask API.
      const response = await fetch('http://127.0.0.1:5000/api/measure', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: imageDataUrl })
      });
      const data = await response.json();
      if (data.error) {
        setError(data.error);
      } else {
        // Automatically navigate to the Measurement page with query parameters.
        router.push(
          `/measurement?eye_width_mm=${data.eye_width_mm}&bridge_width_mm=${data.bridge_width_mm}&b_size_mm=${data.b_size_mm}`
        );
      }
    } catch (err: any) {
      setError("An error occurred: " + err.message);
    }
    setScanning(false);
  };

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-4 relative">
      <h1 className="text-4xl font-bold mb-4">Face Scan</h1>

      <div className="relative mx-auto max-w-lg">
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <div className="relative mb-6" style={{ height: '500px' }}>
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="w-full h-full aspect-video rounded-lg bg-gray-100"
              style={{ transform: 'scaleX(-1)' }}
            />
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
              <div
                className="border-4 border-blue-400 border-dashed rounded-full opacity-70"
                style={{ width: '25%', height: '39%' }}
              />
            </div>
          </div>

          {scanning ? (
            <div className="text-center text-gray-600 mb-6">
              <div className="animate-pulse">Scanning in progress...</div>
            </div>
          ) : error ? (
            <div className="text-center text-red-500 mb-6 bg-red-50 p-4 rounded-lg">
              {error}
            </div>
          ) : (
            <p className="text-center text-gray-600 mb-6">
              Position your face inside the oval guide and ensure good lighting
            </p>
          )}

          <Button 
            onClick={startScan} 
            disabled={scanning}
            className="w-full py-4 text-lg bg-blue-600 hover:bg-blue-700 transition-colors rounded-lg shadow-md"
          >
            <Camera className="mr-2" />
            {scanning ? "Scanning..." : "Start Scan"}
          </Button>
        </div>
      </div>

      {/* Optional back arrow to go back to Home */}
      <div className="fixed left-8 top-1/2 -translate-y-1/2">
        <Link href="/">
          <button className="rounded-full bg-black w-16 h-16 flex justify-center items-center">
            <ArrowLeft color="white" size={32} />
          </button>
        </Link>
      </div>

      <div className="mt-28">
        <ProgressBar index={1} steps={steps} />
      </div>
    </main>
  );
}
