import { StatusBadge } from './StatusBadge';

export function StatusCard({ status }) {
    return (
        <div className="bg-gray-50 rounded-lg p-4 mb-8">
            <div className="flex items-center justify-between mb-2">
                <h2 className="text-xl font-semibold">Bot Durumu</h2>
                <StatusBadge status={status?.status} />
            </div>
            <p className="text-gray-600 text-sm whitespace-pre-line">
                {status?.message}
            </p>
        </div>
    );
} 