import { Outlet } from "react-router-dom";
import TopBar from "../components/TopBar";


export default function AppLayout() {
  return (
    <div className="min-h-screen bg-gray-800">
      <TopBar />
      <main className="flex-1 p-6">
        <Outlet />
      </main>
    </div>
  );
}
