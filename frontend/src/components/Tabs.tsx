import { useNavigate } from 'react-router-dom';

interface TabsProps {
    tabs: string[],
    activeTab: string
}

export default function Tabs({ tabs, activeTab }: TabsProps) {

    const navigate = useNavigate();

    function handleTabClick(tab: string) {
        navigate(`/${tab.toLowerCase()}`);
    }

    return (
        <div className="flex items-center g-4">
            {tabs.map(tab =>
                <div className="">
                    <button
                        className={`
                            relative text-lg p-4
                            hover:text-blue-400
                            transition
                        `}
                        onClick={() => handleTabClick(tab)}
                    >
                        {tab.charAt(0).toUpperCase() + tab.slice(1)}

                        {/* underline */}
                        <span
                            className={`
                                absolute left-0 right-0 -bottom-1 h-0.5
                                bg-blue-400
                                transition-all duration-300
                                ${tab === activeTab ? "opacity-100 scale-x-100" : "opacity-0 scale-x-0"}
                            `}
                        />
                    </button>

                </div>
            )}
        </div>
    )
}