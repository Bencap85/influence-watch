import { useNavigate } from 'react-router-dom';

export default function BackButton() {

    const navigate = useNavigate();

    return (
        <button
            onClick={() => navigate(-1)}
            className="
                    flex items-center gap-2
                    px-3 py-1.5
                    text-m font-medium
                    text-gray-300
                    bg-gray-600
                    border border-gray-700/50
                    rounded-md
                    hover:bg-gray-800/70 hover:text-blue-400
                    transition
                "
        >
            ← Back
        </button>
    );
}