import { create } from "zustand";

interface Measurements {
    eyeWidth: number;
    bridgeWidth: number;
    sideLength: number;
}

interface MeasurementsStore {
    setMeasurements: (measurements: Measurements) => void;
    resetMeasurements: () => void;
    measurements: Measurements | null; // Add the measurements property to the interface
}

const useMeasurementsStore = create<MeasurementsStore>()((set) => ({
    measurements: null,
    setMeasurements: (measurements) => set({ measurements }),
    resetMeasurements: () => set({ measurements: null }),

}));

export { useMeasurementsStore };