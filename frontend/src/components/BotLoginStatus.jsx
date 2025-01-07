import { useState } from 'react';
import { API_URL } from '../config';

export function BotLoginStatus({ status, onLogin }) {
    const [showCodeInput, setShowCodeInput] = useState(false);
    const [code, setCode] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleLogin = async () => {
        if (!showCodeInput) {
            try {
                const response = await fetch(`${API_URL}/api/login`, {
                    method: 'GET'
                });

                if (response.ok) {
                    const data = await response.json();
                    setShowCodeInput(true);
                } else {
                    throw new Error('Failed to request code');
                }
            } catch (err) {
                setError('Giriş başlatılamadı');
            }
            return;
        }

        setLoading(true);
        setError('');

        try {
            const response = await fetch(`${API_URL}/api/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code }),
            });

            if (response.ok) {
                onLogin();
                setShowCodeInput(false);
                setCode('');
            } else {
                const data = await response.json();
                setError(data.detail || 'Giriş yapılamadı');
            }
        } catch (err) {
            setError('Giriş yapılamadı');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-white p-4 rounded-lg shadow space-y-4">
            <div className="flex items-center justify-between">
                <h3 className="text-lg font-medium">Bot Durumu</h3>
                <span className={`px-2 py-1 rounded text-sm ${status === 'logged_in'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800'
                    }`}>
                    {status === 'logged_in' ? 'Giriş Yapılmış' : 'Giriş Yapılmamış'}
                </span>
            </div>

            {status !== 'logged_in' && (
                <div className="space-y-4">
                    {showCodeInput && (
                        <div>
                            <label className="block text-sm font-medium text-gray-700">
                                Telefonunuza gelen kodu girin
                            </label>
                            <input
                                type="text"
                                value={code}
                                onChange={(e) => setCode(e.target.value)}
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                                placeholder="Kod"
                            />
                        </div>
                    )}

                    {error && (
                        <div className="text-sm text-red-600">
                            {error}
                        </div>
                    )}

                    <button
                        onClick={handleLogin}
                        disabled={loading}
                        className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 ${loading ? 'opacity-50 cursor-not-allowed' : ''
                            }`}
                    >
                        {loading ? 'Giriş Yapılıyor...' : showCodeInput ? 'Kodu Gönder' : 'Giriş Yap'}
                    </button>
                </div>
            )}
        </div>
    );
} 