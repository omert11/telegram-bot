import { useState, useEffect } from 'react';
import { StatusCard } from './components/StatusCard';
import { RunHistory } from './components/RunHistory';
import { TelegramApiForm } from './components/forms/TelegramApiForm';
import { LoadingSpinner } from './components/LoadingSpinner';
import { ErrorMessage } from './components/ErrorMessage';
import { ConfigurationForm } from './components/ConfigurationForm';
import Swal from 'sweetalert2';
import { LoginForm } from './components/LoginForm';
import { BotLoginStatus } from './components/BotLoginStatus';
import { API_URL } from './config';

function App() {
    const [status, setStatus] = useState(null);
    const [config, setConfig] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [history, setHistory] = useState([]);
    const [isAuthenticated, setIsAuthenticated] = useState(
        !!localStorage.getItem('auth_token')
    );
    const [botStatus, setBotStatus] = useState(null);

    const fetchWithAuth = async (endpoint, options = {}) => {
        const token = localStorage.getItem('auth_token');
        const headers = {
            ...options.headers,
            'Authorization': `Basic ${token}`,
            'Content-Type': 'application/json',
        };

        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers,
            mode: 'cors',
        });

        if (response.status === 401) {
            setIsAuthenticated(false);
            localStorage.removeItem('auth_token');
            throw new Error('Unauthorized');
        }
        return response;
    };

    const fetchStatus = async () => {
        try {
            const response = await fetchWithAuth('/api/status');
            const data = await response.json();
            setStatus(data);
            setError(null);
        } catch (err) {
            setError('Failed to fetch bot status');
        }
    };

    const fetchConfig = async () => {
        try {
            const response = await fetchWithAuth('/api/config');
            const data = await response.json();
            setConfig(data);
            setError(null);
        } catch (err) {
            setError('Failed to fetch configuration');
        } finally {
            setLoading(false);
        }
    };

    const fetchHistory = async () => {
        try {
            const response = await fetchWithAuth('/api/history');
            const data = await response.json();
            setHistory(data);
        } catch (err) {
            console.error('Failed to fetch history:', err);
        }
    };

    const handleProcess = async () => {
        setLoading(true);
        try {
            const response = await fetch(`${API_URL}/api/process`, {
                method: 'POST',
            });
            const data = await response.json();
            alert(data.message);
        } catch (err) {
            alert('Failed to process channels');
        } finally {
            setLoading(false);
            fetchStatus();
        }
    };

    const showAlert = async (type, title, text) => {
        await Swal.fire({
            icon: type,
            title: title,
            text: text,
            confirmButtonColor: '#3B82F6',
        });
    };

    const showConfirm = async (title, text) => {
        const result = await Swal.fire({
            icon: 'question',
            title: title,
            text: text,
            showCancelButton: true,
            confirmButtonColor: '#3B82F6',
            cancelButtonColor: '#EF4444',
            confirmButtonText: 'Evet',
            cancelButtonText: 'İptal',
        });
        return result.isConfirmed;
    };

    const handleConfigChange = (key, value) => {
        setConfig(prev => ({
            ...prev,
            [key]: value
        }));
    };

    const handleSaveConfig = async () => {
        const confirmed = await showConfirm(
            'Ayarları Kaydet',
            'Tüm ayarları güncellemek istediğinizden emin misiniz?'
        );

        if (!confirmed) return;

        setLoading(true);
        try {
            const response = await fetch(`${API_URL}/api/config/bulk`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(config),
            });

            const data = await response.json();

            if (response.ok) {
                await showAlert('success', 'Başarılı', data.message);
                await Promise.all([
                    fetchStatus(),
                    fetchConfig(),
                ]);
            } else {
                throw new Error(data.detail);
            }
        } catch (err) {
            await showAlert('error', 'Hata', 'Ayarlar güncellenirken hata oluştu');
        } finally {
            setLoading(false);
        }
    };

    const handleToggle = async () => {
        try {
            const response = await fetch(`${API_URL}/api/toggle`, {
                method: 'POST',
            });
            const data = await response.json();
            if (response.ok) {
                await showAlert('success', 'Başarılı', data.message);
                await Promise.all([
                    fetchStatus(),
                    fetchConfig(),
                    fetchHistory(),
                ]);
            } else {
                throw new Error(data.detail);
            }
        } catch (err) {
            await showAlert('error', 'Hata', 'Bot durumu değiştirilemedi');
        }
    };

    const handleReset = async () => {
        const confirmed = await showConfirm(
            'Veritabanını Sıfırla',
            'Geçmiş kayıtlar silinecek. Devam etmek istiyor musunuz?'
        );

        if (!confirmed) return;

        try {
            const response = await fetch(`${API_URL}/api/reset`, {
                method: 'POST',
            });
            const data = await response.json();

            if (response.ok) {
                await showAlert('success', 'Başarılı', data.message);
                await Promise.all([
                    fetchStatus(),
                    fetchHistory(),
                ]);
            } else {
                throw new Error(data.detail);
            }
        } catch (err) {
            await showAlert('error', 'Hata', 'Veritabanı sıfırlanırken hata oluştu');
        }
    };

    const fetchBotStatus = async () => {
        try {
            const response = await fetchWithAuth('/api/bot-status');
            const data = await response.json();
            setBotStatus(data.status);
        } catch (err) {
            console.error('Failed to fetch bot status:', err);
        }
    };

    useEffect(() => {
        if (isAuthenticated) {
            fetchBotStatus();
            fetchStatus();
            fetchConfig();
            fetchHistory();
            const interval = setInterval(() => {
                fetchStatus();
                fetchHistory();
            }, 30000);
            return () => clearInterval(interval);
        }
    }, [isAuthenticated]);

    if (!isAuthenticated) {
        return <LoginForm onLogin={() => setIsAuthenticated(true)} />;
    }

    if (loading) return <LoadingSpinner />;
    if (error) return <ErrorMessage message={error} />;

    if (botStatus !== 'logged_in') {
        return (
            <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
                <div className="relative py-3 sm:max-w-xl sm:mx-auto">
                    <div className="relative px-4 py-10 bg-white mx-8 md:mx-0 shadow rounded-3xl sm:p-10">
                        <div className="max-w-md mx-auto">
                            <h1 className="text-2xl font-bold mb-8 text-center text-gray-900">
                                Telegram Bot Kontrol Paneli
                            </h1>
                            <BotLoginStatus
                                status={botStatus}
                                onLogin={fetchBotStatus}
                            />
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
            <div className="relative py-3 sm:max-w-5xl sm:mx-auto">
                <div className="flex flex-col lg:flex-row gap-6">
                    <div className="flex-1">
                        <div className="relative px-4 py-10 bg-white mx-8 md:mx-0 shadow rounded-3xl sm:p-10">
                            <div className="max-w-md mx-auto">
                                <h1 className="text-2xl font-bold mb-8 text-center text-gray-900">
                                    Telegram Bot Kontrol Paneli
                                </h1>

                                <StatusCard status={status} />

                                {config && (
                                    <ConfigurationForm
                                        config={config}
                                        onConfigChange={handleConfigChange}
                                        onSave={handleSaveConfig}
                                        onReset={handleReset}
                                    />
                                )}
                            </div>
                        </div>
                    </div>

                    <div className="lg:w-80">
                        <RunHistory history={history} />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;
