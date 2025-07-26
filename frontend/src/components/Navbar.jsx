import { cn } from "@/lib/utils";

const tabs = [
    { name: "Dashboard" },
    { name: "Chat" },
    { name: "Upload" },
    { name: "Documents" },
];

export default function Navbar({ activeTab, onTabChange }) {
    return (
        <nav className="w-full flex items-center justify-center bg-white border-b">
            <div className="flex gap-6 py-2">
                {tabs.map(tab => (
                    <button
                        key={tab.name}
                        className={cn(
                            "px-4 py-2 rounded-md font-semibold transition-colors duration-200",
                            activeTab === tab.name
                                ? "bg-gray-100 text-green-700 shadow"
                                : "text-gray-500 hover:bg-gray-50"
                        )}
                        onClick={() => onTabChange(tab.name)}
                    >
                        {tab.name}
                    </button>
                ))}
            </div>
        </nav>
    );
} 