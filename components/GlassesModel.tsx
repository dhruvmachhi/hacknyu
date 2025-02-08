'use client';
import { useFrame } from "@react-three/fiber";
import { useEffect, useRef } from "react";
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader'
import { useLoader } from '@react-three/fiber'
import { Object3D } from "three";


export default function GlassesModel() {
    const ref = useRef<Object3D>(null);
    const obj = useLoader(OBJLoader, '/oculos.obj');
    const mouse = useRef({ x: 0, y: 0 });

    useEffect(() => {
        const handleMouseMove = (event: MouseEvent) => {
            mouse.current.x = (event.clientX / window.innerWidth) * 2 - 1;
            mouse.current.y = (-(event.clientY / window.innerHeight)) * 2 + 1; // Inverted Y-axis
        };

        window.addEventListener('mousemove', handleMouseMove);
        return () => window.removeEventListener('mousemove', handleMouseMove);
    }, []);

    useFrame(() => {
        if (ref.current) {
            // Smoothly interpolate rotation towards mouse position
            ref.current.rotation.y += (mouse.current.x * 0.5 - ref.current.rotation.y) * 0.05;
            ref.current.rotation.x += (mouse.current.y * 0.2 - ref.current.rotation.x) * 0.05; // Inverted Y
        }
    });

    return (
        <primitive ref={ref} object={obj} />
    );
}