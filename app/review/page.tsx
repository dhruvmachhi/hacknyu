'use client';

import GlassesModel from '@/components/GlassesModel';
import ProgressBar from '@/components/ProgressBar';
import { Button } from '@/components/ui/button';
import { Canvas } from '@react-three/fiber';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import React from 'react';

const steps = [
  "Introduction",
  "Scan Face",
  "Measurements",
  "Review",
];

export default function Review() {
  return (
    <main className="flex flex-col items-center justify-center p-4">
      <h1 className="text-4xl font-bold text-center mb-4 text-gray-800">Frames Model Complete!</h1>
      <p>Press the button below to begin downloading your frames.</p>
      <a href="https://cad.onshape.com/documents/2d31f5e10fa056c96e0a75c6/w/8fc670243965225a2baeaa59/e/6c046a925cf8e0f222c96fba">
      <Button 
        variant="outline"
        className="flex-1 py-6 text-lg border-gray-300 hover:bg-gray-50 h-9 m-5"
      >
        Download My Frames
      </Button>
      </a>
      <div className="fixed left-8 top-1/2 -translate-y-1/2 z-10">
                    <button className="rounded-full bg-black hover:bg-blue-600 transition-colors w-16 h-16 flex justify-center items-center shadow-lg" onClick={() => window.history.back()}>
                        <ArrowLeft color="white" size={32} />
                    </button>
      </div>
      <div className="absolute w-full h-full bottom-0 z-0">
                <Canvas camera={{ fov: 35, zoom: 8, near: 1, far: 1000 }}>
                    <ambientLight intensity={0} />
                    <GlassesModel />
                </Canvas>
            </div>
      <ProgressBar index={4} steps={steps}/>
    </main>
  );
}