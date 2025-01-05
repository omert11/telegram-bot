import { Switch } from '../Switch';

export function BotSettingsForm({ config, onConfigChange }) {
    return (
        <div className="bg-gray-50 p-4 rounded-lg space-y-4">
            <h3 className="font-medium text-gray-900 mb-4">Bot Ayarları</h3>

            <div className="space-y-4">
                <div className="bg-white rounded-lg p-3 shadow-sm">
                    <Switch
                        checked={config.is_active}
                        onChange={(e) => onConfigChange('is_active', e.target.checked)}
                        label="Bot Durumu"
                    />
                </div>

                <div className="bg-white rounded-lg p-3 shadow-sm">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        Çalışma Aralığı
                    </label>
                    <div className="flex items-center">
                        <input
                            type="number"
                            min="1"
                            value={config.interval_minutes}
                            onChange={(e) => onConfigChange('interval_minutes', parseInt(e.target.value))}
                            className="block w-full px-3 py-2 rounded-md border border-gray-300 focus:ring-green-500 focus:border-green-500"
                        />
                        <span className="ml-2 text-sm text-gray-500">dakika</span>
                    </div>
                </div>

                <div className="bg-white rounded-lg p-3 shadow-sm">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        Komisyon
                    </label>
                    <div className="flex items-center">
                        <input
                            type="number"
                            value={config.add_fee}
                            onChange={(e) => onConfigChange('add_fee', parseInt(e.target.value))}
                            className="block w-full px-3 py-2 rounded-md border border-gray-300 focus:ring-green-500 focus:border-green-500"
                        />
                        <span className="ml-2 text-sm text-gray-500">TL</span>
                    </div>
                </div>
            </div>
        </div>
    );
} 