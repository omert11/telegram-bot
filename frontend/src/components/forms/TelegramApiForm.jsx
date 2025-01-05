export function TelegramApiForm({ config, onConfigChange }) {
    return (
        <div className="bg-gray-50 p-4 rounded-lg space-y-4">
            <h3 className="font-medium text-gray-900">Telegram API Ayarları</h3>

            <div>
                <label className="block text-sm font-medium text-gray-700">API ID</label>
                <div className="mt-1">
                    <input
                        type="number"
                        value={config.api_id}
                        onChange={(e) => onConfigChange('api_id', parseInt(e.target.value))}
                        className="block w-full px-3 py-2 rounded-md border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
                    />
                </div>
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700">API Hash</label>
                <div className="mt-1">
                    <input
                        type="text"
                        value={config.api_hash}
                        onChange={(e) => onConfigChange('api_hash', e.target.value)}
                        className="block w-full px-3 py-2 rounded-md border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
                    />
                </div>
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700">Telefon Numarası</label>
                <div className="mt-1">
                    <input
                        type="text"
                        value={config.phone_number}
                        onChange={(e) => onConfigChange('phone_number', e.target.value)}
                        className="block w-full px-3 py-2 rounded-md border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
                        placeholder="905xxxxxxxxx"
                    />
                </div>
            </div>
        </div>
    );
} 