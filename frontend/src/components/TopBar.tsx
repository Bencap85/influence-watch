import { useEffect, useState } from "react";
import { useLocation } from 'react-router-dom';
import SearchBar from "./SearchBar";
import Tabs from "./Tabs";


export default function TopBar({}) {

    const location = useLocation();

    const [activeTab, setActiveTab] = useState<string>(location.pathname.slice(1));

    const tabs = ["detections", "events", "articles"];

    useEffect(() => {
        const tab = location.pathname.slice(1) || "detections";
        setActiveTab(tab);
    }, [location.pathname]);

    return (
        <>
            <div id="topbar" className="w-full h-18 p-4 text-4xl flex justify-between items-center">
                <div>
                    <h1>Influence Watch</h1>
                </div>
                <Tabs tabs={tabs} activeTab={activeTab} />
                <SearchBar placeholder={`Search ${activeTab}...`}/>
            </div>
            <p className="px-4 font-mono">[{activeTab.toUpperCase()}]</p>
        </>
    )
}