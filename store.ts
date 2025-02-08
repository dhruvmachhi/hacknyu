import { create } from "zustand";

interface Measurements {
    eyeWidth: number;
    bridgeWidth: number;
    sideLength: number;
    setMeasurements: (measurements: Measurements) => void;
    resetMeasurements: () => void;
}

const useMeasurementsStore = create<Measurements>()((set) => ({
    eyeWidth: 0,
    bridgeWidth: 0,
    sideLength: 0,
    setMeasurements: (measurements) => set({ ...measurements }),
    resetMeasurements: () => set({ eyeWidth: 0, bridgeWidth: 0, sideLength: 0 }),
}));

export { useMeasurementsStore };