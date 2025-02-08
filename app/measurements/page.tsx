import ProgressBar from "@/components/ProgressBar";

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
            <ProgressBar index={3} steps={steps}/>
        </main>
    );
    }