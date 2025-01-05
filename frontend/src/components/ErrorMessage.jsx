export function ErrorMessage({ message }) {
    return (
        <div className="min-h-screen flex items-center justify-center">
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                {message}
            </div>
        </div>
    );
} 