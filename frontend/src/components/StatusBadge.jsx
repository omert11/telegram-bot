export function StatusBadge({ status }) {
    const colors = {
        active: "bg-green-100 text-green-800",
        inactive: "bg-red-100 text-red-800",
    };

    const labels = {
        active: "AKTİF",
        inactive: "PASİF",
    };

    return (
        <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${colors[status] || "bg-gray-100 text-gray-800"}`}>
            {labels[status] || status?.toUpperCase()}
        </div>
    );
} 