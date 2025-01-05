import { TelegramApiForm } from './forms/TelegramApiForm';
import { BotSettingsForm } from './forms/BotSettingsForm';
import { ChannelSettingsForm } from './forms/ChannelSettingsForm';
import { GeminiApiForm } from './forms/GeminiApiForm';

export function ConfigurationForm({ config, onConfigChange, onSave, onReset }) {
    return (
        <div className="space-y-6">
            <h2 className="text-xl font-semibold">Ayarlar</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Sol Sütun */}
                <div className="space-y-4">
                    <TelegramApiForm config={config} onConfigChange={onConfigChange} />
                    <BotSettingsForm config={config} onConfigChange={onConfigChange} />
                </div>

                {/* Sağ Sütun */}
                <div className="space-y-4">
                    <ChannelSettingsForm config={config} onConfigChange={onConfigChange} />
                    <GeminiApiForm config={config} onConfigChange={onConfigChange} />
                </div>
            </div>

            {/* Action Buttons */}
            <div className="pt-6 space-y-4">
                <button
                    onClick={onSave}
                    className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                    Ayarları Kaydet
                </button>

                <button
                    onClick={onReset}
                    className="w-full flex justify-center py-2 px-4 border border-red-500 text-red-500 rounded-md shadow-sm text-sm font-medium hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                >
                    Veritabanını Sıfırla
                </button>
            </div>
        </div>
    );
} 