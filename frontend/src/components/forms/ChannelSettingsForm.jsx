export function ChannelSettingsForm({ config, onConfigChange }) {
    return (
        <div className="bg-gray-50 p-4 rounded-lg space-y-4">
            <h3 className="font-medium text-gray-900">Kanal Ayarları</h3>

            <div>
                <label className="block text-sm font-medium text-gray-700">Kaynak Kanallar</label>
                <div className="mt-1">
                    <textarea
                        value={config.source_channels.join('\n')}
                        onChange={(e) => onConfigChange('source_channels', e.target.value.split('\n').filter(Boolean))}
                        rows="3"
                        className="block w-full px-3 py-2 rounded-md border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
                        placeholder="Her satıra bir kanal adı"
                    />
                </div>
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700">Hedef Kanal</label>
                <div className="mt-1">
                    <input
                        type="text"
                        value={config.target_channel}
                        onChange={(e) => onConfigChange('target_channel', e.target.value)}
                        className="block w-full px-3 py-2 rounded-md border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
                    />
                </div>
            </div>
        </div>
    );
} 