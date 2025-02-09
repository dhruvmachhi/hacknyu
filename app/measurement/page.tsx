'use client';

import React, { useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import ProgressBar from '@/components/ProgressBar';
import { ArrowLeft, ArrowRight, Edit2, RotateCcw, Save } from 'lucide-react';
import Link from 'next/link';

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
        setIsEditing(false);
    };

    return (
        <main className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 relative">
            <div className="max-w-4xl mx-auto px-4 py-12">
                <h1 className="text-4xl font-bold text-center mb-4 text-gray-800">Your Measurements</h1>
                <p className="text-center text-gray-600 mb-8">
                    Review and adjust your measurements before proceeding to frame design
                </p>

                <div className="bg-white rounded-2xl p-8 shadow-lg max-w-lg mx-auto">
                    {eyeWidth && bridgeWidth && bSize ? (
                        isEditing ? (
                            <form onSubmit={handleSubmit} className="space-y-6">
                                <div className="space-y-4">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">
                                            Eye Width (mm)
                                        </label>
                                        <input
                                            type="number"
                                            value={eyeWidth}
                                            onChange={(e) => setEyeWidth(e.target.value)}
                                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">
                                            Bridge Width (mm)
                                        </label>
                                        <input
                                            type="number"
                                            value={bridgeWidth}
                                            onChange={(e) => setBridgeWidth(e.target.value)}
                                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">
                                            B Size (Vertical) (mm)
                                        </label>
                                        <input
                                            type="number"
                                            value={bSize}
                                            onChange={(e) => setBSize(e.target.value)}
                                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                                            required
                                        />
                                    </div>
                                </div>
                                <Button 
                                    type="submit" 
                                    className="w-full bg-blue-600 hover:bg-blue-700 text-white py-6 text-lg"
                                >
                                    <Save className="mr-2 h-5 w-5" />
                                    Save Changes
                                </Button>
                            </form>
                        ) : (
                            <div className="space-y-6">
                                <div className="grid grid-cols-1 gap-6">
                                    <div className="bg-gray-50 p-6 rounded-xl border border-gray-100 mb-4">
                                        <div className="text-sm text-gray-500 mb-1">Eye Width</div>
                                        <div className="text-3xl font-semibold text-gray-900">{eyeWidth} mm</div>
                                    </div>
                                    <div className="bg-gray-50 p-6 rounded-xl border border-gray-100 mb-4">
                                        <div className="text-sm text-gray-500 mb-1">Bridge Width</div>
                                        <div className="text-3xl font-semibold text-gray-900">{bridgeWidth} mm</div>
                                    </div>
                                    <div className="bg-gray-50 p-6 rounded-xl border border-gray-100 mb-4">
                                        <div className="text-sm text-gray-500 mb-1">B Size (Vertical)</div>
                                        <div className="text-3xl font-semibold text-gray-900">{bSize} mm</div>
                                    </div>
                                </div>

                                <Button 
                                    onClick={handleEditToggle}
                                    variant="outline"
                                    className="w-full py-6 text-lg border-gray-300 hover:bg-gray-50"
                                >
                                    <Edit2 className="mr-2 h-5 w-5" />
                                    Edit Measurements
                                </Button>
                            </div>
                        )
                    ) : (
                        <div className="text-center py-8">
                            <p className="text-gray-500 mb-4">No measurement data available.</p>
                            <Button 
                                onClick={() => router.push('/scan')}
                                variant="outline"
                                className="w-full"
                            >
                                Return to Scan
                            </Button>
                        </div>
                    )}

                    <div className="mt-8 flex gap-4">
                        <Button 
                            onClick={() => router.push('/scan')}
                            variant="outline"
                            className="flex-1 py-6 text-lg border-gray-300 hover:bg-gray-50"
                        >
                            <RotateCcw className="mr-2 h-5 w-5" />
                            Rescan
                        </Button>
                        <Button 
                            onClick={() => router.push('/design')}
                            className="flex-1 bg-black hover:bg-blue-600 transition-colors py-6 text-lg"
                        >
                            Next Step
                            <ArrowRight className="ml-2 h-5 w-5" />
                        </Button>
                    </div>
                </div>

                <Link href="/scan" className="fixed left-8 top-1/2 -translate-y-1/2">
                    <button className="rounded-full bg-black hover:bg-blue-600 transition-colors w-16 h-16 flex justify-center items-center shadow-lg">
                        <ArrowLeft color="white" size={32} />
                    </button>
                </Link>

                <div className="mt-20">
    <ProgressBar index={3} steps={steps} />
</div>

            </div>
        </main>
    );
}