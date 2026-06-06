import type { SystemStats } from "../types/systemStats";

interface SystemStatsProps {
    systemStats: SystemStats;
}

export default function SystemStatsSummary({ systemStats }: SystemStatsProps) {

    const statColors: Record<string, string> = {
        total_articles: "text-cyan-400",
        total_countries: "text-blue-400",
        total_distinct_sources: "text-emerald-400"
    };

    if (!systemStats) return "Loading system stats...";

    return (
        <div className="grid grid-cols-3 gap-4">
            {Object.entries(systemStats).map(([key, val]) => (
                <div
                    key={key}
                    className="p-4 bg-white/20 border border-white/10 rounded-lg shadow-sm"
                >
                    <div className="text-xs uppercase text-stone-400">
                        {key.replace(/_/g, " ")}
                    </div>
                    <div className="text-2xl font-semibold tracking-wide text-stone-600">
                        {val}
                    </div>
                </div>
            ))}
        </div>
    )
}