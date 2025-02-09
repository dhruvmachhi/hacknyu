'use client';

import React, { useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import ProgressBar from '@/components/ProgressBar';

const steps = [
  "Introduction",
  "Scan Face",
  "Measurements",
  "Design",
  "Review",
];

export default function MeasurementPage() {
  const searchParams = useSearchParams();
  const router = useRouter();

  // Retrieve measurement values from the query parameters.
  const initialEyeWidth = searchParams.get('eye_width_mm') || '';
  const initialBridgeWidth = searchParams.get('bridge_width_mm') || '';
  const initialBSize = searchParams.get('b_size_mm') || '';

  const [eyeWidth, setEyeWidth] = useState(initialEyeWidth);
  const [bridgeWidth, setBridgeWidth] = useState(initialBridgeWidth);
  const [bSize, setBSize] = useState(initialBSize);
  const [isEditing, setIsEditing] = useState(false);

  const handleEditToggle = () => {
    setIsEditing(!isEditing);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Here you can handle the submission logic, e.g., send updated measurements to an API
    setIsEditing(false);
  };

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-4">
      <h1 className="text-4xl font-bold mb-4">Measurement Results</h1>
      
      {eyeWidth && bridgeWidth && bSize ? (
        <div className="mb-8 text-center">
          <ul>
            <li>Eye Width: {eyeWidth} mm</li>
            <li>Bridge Width: {bridgeWidth} mm</li>
            <li>B Size (Vertical): {bSize} mm</li>
          </ul>
        </div>
      ) : (
        <p className="mb-8">No measurement data available.</p>
      )}

      {isEditing ? (
        <form onSubmit={handleSubmit} className="mb-8">
          <div className="flex flex-col gap-4">
            <input
              type="number"
              value={eyeWidth}
              onChange={(e) => setEyeWidth(e.target.value)}
              placeholder="Eye Width (mm)"
              className="border p-2"
              required
            />
            <input
              type="number"
              value={bridgeWidth}
              onChange={(e) => setBridgeWidth(e.target.value)}
              placeholder="Bridge Width (mm)"
              className="border p-2"
              required
            />
            <input
              type="number"
              value={bSize}
              onChange={(e) => setBSize(e.target.value)}
              placeholder="B Size (mm)"
              className="border p-2"
              required
            />
            <Button type="submit">Save Measurements</Button>
          </div>
        </form>
      ) : (
        <Button onClick={handleEditToggle}>Edit Measurements</Button>
      )}

      <div className="flex gap-4">
        <Button onClick={() => router.push('/scan')}>
          Rescan
        </Button>
        <Button onClick={() => router.push('/design')}>
          Next: Design
        </Button>
      </div>

      <div className="mt-8">
        {/* For the measurement step, we use index 2 */}
        <ProgressBar index={3} steps={steps} />
      </div>
    </main>
  );
}
