import { Routes, Route } from "react-router-dom";
import AppLayout from "./layout/AppLayout";
import EventsPage from "./pages/EventsPage";
import EventDetailsPage from "./pages/details/EventDetailsPage";
import DetectionsPage from "./pages/DetectionsPage";
import ArticlesPage from "./pages/ArticlesPage";
import { SearchProvider } from "./context/SearchContext";
import ArticleDetails from "./components/ArticleDetails";
import DetectionDetailsPage from "./pages/details/DetectionDetailsPage";


export default function App() {
  return (
    <div className="min-h-screen bg-zinc-100">
      <SearchProvider>
        <Routes>
          <Route element={<AppLayout />}>
            <Route path="/events" element={<EventsPage />} />
            <Route path="/detections" element={<DetectionsPage />} />
            <Route path="/articles" element={<ArticlesPage />} />

            <Route path="/event/:id" element={<EventDetailsPage />} />
            <Route path="/detection/:id" element={<DetectionDetailsPage />} />
            <Route path="/article/:id" element={<ArticleDetails />} />
          </Route>
        </Routes>
      </SearchProvider>
    </div>
  );
}
