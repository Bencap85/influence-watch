import { useState, useMemo } from "react";


export interface Column<T> {
    key: keyof T;
    label: string;
    render?: (row: T) => React.ReactNode;
}


interface SortConfig<T> {
    key: keyof T | null;
    direction: "asc" | "desc" | null;
}

interface TableProps<T> {
    data: T[];
    columns: Column<T>[];
    rowKey?: (row: T) => string | number;
    onRowClick?: (rowData: T) => void;
}

export function Table<T extends object>({
    data,
    columns,
    rowKey = (row) => (row as any).id,
    onRowClick
}: TableProps<T>) {
    const [sortConfig, setSortConfig] = useState<SortConfig<T>>({
        key: null,
        direction: null
    });

    function toggleSort(column: keyof T) {
        setSortConfig((prev) => {
            if (prev.key !== column) return { key: column, direction: "asc" };
            if (prev.direction === "asc") return { key: column, direction: "desc" };
            return { key: null, direction: null };
        });
    }

    const sortedData = useMemo(() => {
        if (!sortConfig.key || !sortConfig.direction) return data;

        return [...data].sort((a, b) => {
            const key = sortConfig.key!;
            const valA = a[key];
            const valB = b[key];

            // Date sorting
            if (valA instanceof Date || valB instanceof Date) {
                const tA = new Date(valA as any).getTime();
                const tB = new Date(valB as any).getTime();
                return sortConfig.direction === "asc" ? tA - tB : tB - tA;
            }

            // String sorting
            if (typeof valA === "string" && typeof valB === "string") {
                return sortConfig.direction === "asc"
                    ? valA.localeCompare(valB)
                    : valB.localeCompare(valA);
            }

            // Number sorting
            if (typeof valA === "number" && typeof valB === "number") {
                return sortConfig.direction === "asc"
                    ? valB - valA
                    : valA - valB;
            }

            return 0;
        });
    }, [data, sortConfig]);

    return (
        <div className="border border-stone-800 shadow-[0_0_15px_rgba(0,0,0,0.3)] rounded-lg shadow-sm overflow-hidden overflow-x-auto">
            <table className="w-full text-sm">
                <thead className="shadow-[0_0_15px_rgba(0,0,0,0.3)] bg-gray-700 uppercase tracking-wide text-xs border-b border-stone-800">
                    <tr>
                        {columns.map((col) => (
                            <th
                                key={String(col.key)}
                                className="p-3 text-left cursor-pointer select-none hover:text-blue-400"
                                onClick={() => toggleSort(col.key)}
                            >
                                <div className="flex items-center gap-1">
                                    {col.label}
                                    <SortArrow
                                        active={sortConfig.key === col.key}
                                        direction={sortConfig.direction}
                                    />
                                </div>
                            </th>
                        ))}
                    </tr>
                </thead>

                <tbody>
                    {sortedData.map((row, idx) => (
                        <tr
                            key={rowKey(row)}
                            className={`
                                transition
                                ${idx % 2 === 1 ? "bg-gray-600" : "bg-stone-200/20"}
                                hover:opacity-60
                                ${onRowClick ? "cursor-pointer" : ""}
                            `}
                            onClick={() => onRowClick && onRowClick(row)}
                        >
                            {columns.map((col) => (
                                <td key={String(col.key)} className="p-3">
                                    <p>{col.render ? col.render(row) : (row[col.key] as any)}</p>
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

function SortArrow({
    active,
    direction
}: {
    active: boolean;
    direction: "asc" | "desc" | null;
}) {
    if (!active || !direction) return <span className="opacity-30">↕</span>;
    if (direction === "asc") return <span>↑</span>;
    return <span>↓</span>;
}
