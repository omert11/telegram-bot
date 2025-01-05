export function GeminiApiForm({ config, onConfigChange }) {
    return (
        <div className="bg-gray-50 p-4 rounded-lg space-y-4">
            <h3 className="font-medium text-gray-900">Gemini API Ayarları</h3>

            <div>
                <label className="block text-sm font-medium text-gray-700">API Key</label>
                <div className="mt-1">
                    <input
                        type="text"
                        value={config.gemini_api_key}
                        onChange={(e) => onConfigChange('gemini_api_key', e.target.value)}
                        className="block w-full px-3 py-2 rounded-md border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
                    />
                </div>
            </div>
        </div>
    );
} 