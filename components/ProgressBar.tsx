

function ProgressElement({ color, name} : {color: string, name: string}) {
    return (
        <div className="flex-1 flex flex-col items-center gap-2">
            <span className="text-center text-xs sm:text-base">{name}</span>
            <span className={`h-4 rounded-full w-full ${color}`}></span>
        </div>
    )
}
export default function ProgressBar({index, steps} : {index: number, steps: string[]}) {
    return (
        <div className="absolute w-full max-w-[800px] flex bottom-12 gap-6 left-1/2 -translate-x-1/2 p-3">
            {
                steps.map((step, i) => {
                    return (
                        <ProgressElement key={i} color={i < index ? "bg-blue-500" : "bg-gray-300"} name={step} />
                    )
                })
            }
        </div>
    )
}