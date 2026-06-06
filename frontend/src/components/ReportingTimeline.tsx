import {
    ResponsiveContainer,
    AreaChart,
    Area,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid
} from "recharts";
import { useMemo } from "react";
import { format } from "date-fns";
import type { Article } from "../types/article";

export function ReportingTimeline({ articles }: { articles: Article[] }) {
    const { chartData, countryList } = useMemo(
        () => buildTimelineData(articles),
        [articles]
    );

    const countryColors = useMemo(
        () => getCountryColors(countryList),
        [countryList]
    );

    return (
        <div
            style={{ width: "100%", height: 220 }}
            className="bg-tech-panel border border-tech-border rounded-lg p-6 py-2 shadow-[0_0_20px_rgba(0,255,255,0.05)]"
        >
            <h3 className="">Reporting Timeline</h3>
                
            {/* Legend */}
            <div className="flex gap-4 text-xs text-gray-400 mb-3 my-2">
                {countryList.map(c => (
                    <div key={c} className="flex items-center gap-1">
                        <span
                            className="w-3 h-3 rounded-sm"
                            style={{ background: countryColors[c] }}
                        />
                        {c}
                    </div>
                ))}
            </div>

            <ResponsiveContainer>
                <AreaChart
                    data={chartData}
                    margin={{ top: 10, right: 20, left: 0, bottom: 50 }}
                >
                    <defs>
                        {countryList.map(c => (
                            <linearGradient id={`${c}-grad`} key={c} x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor={countryColors[c]} stopOpacity={0.8} />
                                <stop offset="95%" stopColor={countryColors[c]} stopOpacity={0.15} />
                            </linearGradient>
                        ))}
                    </defs>

                    <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />

                    <XAxis
                        dataKey="timestamp"
                        type="number"
                        scale="time"
                        domain={["auto", "auto"]}
                        tickFormatter={(ts) => format(new Date(ts), "MMM d, HH:mm")}
                        stroke="#6b7280"
                        tick={{ fontSize: 11 }}
                    />

                    <YAxis
                        allowDecimals={false}
                        stroke="#6b7280"
                        tick={{ fontSize: 11 }}
                        label={{
                            value: "Articles",
                            angle: -90,
                            position: "insideLeft",
                            style: { fill: "#65676c", fontSize: 12 }
                        }}
                    />

                    <Tooltip
                        labelFormatter={(ts) => format(new Date(ts), "MMM d, HH:mm")}
                        contentStyle={{
                            background: "#111827",
                            border: "1px solid #374151",
                            borderRadius: "4px",
                            color: "#e5e7eb",
                            fontSize: "0.75rem"
                        }}
                    />

                    {countryList.map((country) => (
                        <Area
                            key={country}
                            type="monotone"
                            dataKey={country}
                            stroke={countryColors[country]}
                            fill={`url(#${country}-grad)`}
                            strokeWidth={2}
                        />
                    ))}
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
}

/* -----------------------------
    Helpers
------------------------------ */

function buildTimelineData(articles: Article[]) {
    // bucket by hour
    const timeline: Record<number, Record<string, number>> = {};
    const countries = new Set<string>();

    for (const a of articles) {
        const d = new Date(a.published_at);
        const bucket = new Date(
            d.getFullYear(),
            d.getMonth(),
            d.getDate(),
            d.getHours(),
            0,
            0,
            0
        ).getTime(); // numeric timestamp for time-scale axis

        const country = a.country;
        countries.add(country);

        if (!timeline[bucket]) timeline[bucket] = {};
        if (!timeline[bucket][country]) timeline[bucket][country] = 0;

        timeline[bucket][country] += 1;
    }

    const countryList = Array.from(countries).sort();

    const chartData = Object.entries(timeline)
        .sort(([t1], [t2]) => Number(t1) - Number(t2))
        .map(([timestamp, counts]) => {
            const row: Record<string, number> & { timestamp: number } = {
                timestamp: Number(timestamp)
            };
            for (const c of countryList) {
                row[c] = counts[c] || 0;
            }
            return row;
        });

    return { chartData, countryList };
}

function getCountryColors(countryList: string[]) {
    const palette = [
        "#4F46E5", "#0EA5E9", "#10B981", "#F59E0B",
        "#EF4444", "#8B5CF6", "#14B8A6", "#F43F5E"
    ];

    const colors: Record<string, string> = {};
    countryList.forEach((c, i) => {
        colors[c] = palette[i % palette.length];
    });

    return colors;
}
