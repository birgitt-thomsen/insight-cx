import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AppShell } from "./AppShell";
import ExecutiveBrief from "../pages/ExecutiveBrief";
import FeedbackExplorer from "../pages/FeedbackExplorer";
import Upload from "../pages/Upload";
import AIEvaluation from "../pages/AIEvaluation";
import Administration from "../pages/Administration";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route element={<AppShell />}>
            <Route index element={<Navigate to="/executive-brief" replace />} />
            <Route path="/executive-brief" element={<ExecutiveBrief />} />
            <Route path="/feedback-explorer" element={<FeedbackExplorer />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/ai-evaluation" element={<AIEvaluation />} />
            <Route path="/administration" element={<Administration />} />
            <Route path="*" element={<Navigate to="/executive-brief" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
