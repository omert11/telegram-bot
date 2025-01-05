import { Clock, CheckCircle2, XCircle, RefreshCcw } from 'lucide-react';

export function RunHistory({ history }) {
    const getIcon = (status) => {
        switch (status) {
            case 'success':
                return <CheckCircle2 className="text-green-500 flex-shrink-0" size={18} />;
            case 'error':
                return <XCircle className="text-red-500 flex-shrink-0" size={18} />;
            case 'info':
                return <RefreshCcw className="text-blue-500 flex-shrink-0" size={18} />;
            default:
                return <XCircle className="text-gray-500 flex-shrink-0" size={18} />;
        }
    };

    return (
        <div className="bg-white shadow rounded-lg p-4">
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-gray-900">Çalışma Geçmişi</h2>
                <Clock className="text-gray-500" size={20} />
            </div>
            <div className="space-y-3">
                {history.map((run, index) => (
                    <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                        {getIcon(run.status)}
                        <div className="flex-1 min-w-0">
                            <p className="text-sm text-gray-900 truncate">{run.message}</p>
                            <p className="text-xs text-gray-500">
                                {new Date(run.created_at).toLocaleString('tr-TR')}
                            </p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
} 