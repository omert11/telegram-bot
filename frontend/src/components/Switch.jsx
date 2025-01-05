export function Switch({ checked, onChange, label }) {
    return (
        <div className="space-y-2">
            <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-gray-700">{label}</label>
                <span className="text-sm font-medium text-gray-700">
                    {checked ? 'Aktif' : 'Pasif'}
                </span>
            </div>
            <div className="flex items-center justify-end">
                <button
                    type="button"
                    role="switch"
                    aria-checked={checked}
                    onClick={() => onChange({ target: { checked: !checked } })}
                    className={`
                        relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent 
                        transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2
                        ${checked ? 'bg-green-500' : 'bg-gray-200'}
                    `}
                >
                    <span
                        aria-hidden="true"
                        className={`
                            pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 
                            transition duration-200 ease-in-out
                            ${checked ? 'translate-x-5' : 'translate-x-0'}
                        `}
                    />
                </button>
            </div>
        </div>
    );
} 