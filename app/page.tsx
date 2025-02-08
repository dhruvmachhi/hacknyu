'use client';
import GlassesModel from "@/components/GlassesModel";
import ProgressBar from "@/components/ProgressBar";
import { Button } from "@/components/ui/button";
import { Canvas } from "@react-three/fiber";
import { ArrowRight } from "lucide-react";
import Link from "next/link";

const steps = [
    "Introduction",
    "Scan Face",
    "Measurements",
    "Design",
    "Review",
]

export default function Home() {
    return (
        <main>
            <div className="absolute w-full h-full">
                <Canvas camera={{ fov: 35, zoom: 1, near: 1, far: 1000 }}>
                    <ambientLight intensity={0} />
                    <GlassesModel />
                </Canvas>
            </div>
            <div className="p-4 flex gap-6 flex-col">
                <p className="text-6xl sm:text-8xl font-bold">TrueSight</p>
                <p className="text-3xl w-[600px]">Use scanning technology to create the perfect frames for your face.</p>
            </div>
            <div className="fixed right-8 bottom-1/2 -translate-y-1/2">
            <Link href={"/scan"}>
                <button className="rounded-full bg-black size-16 flex justify-center items-center">
                    <ArrowRight color="white" size={32} />
                </button>
            </Link>
            </div>
            <ProgressBar index={1} steps={steps}/>
        </main>
    );
}
