import { useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { fetchAiSettings } from "../../api/aiSettings";
import { PageHeader, Tabs } from "../../components";
import { SingleFeedbackTab } from "./SingleFeedbackTab";
import { BenchmarkLabTab } from "./BenchmarkLabTab";
import { ModelComparisonTab } from "./ModelComparisonTab";

const TAB_ITEMS = [
  { value: "single", label: "Single Feedback" },
  { value: "benchmark", label: "Benchmark Lab" },
  { value: "comparison", label: "Model Comparison" },
];

export default function AIEvaluation() {
  const [searchParams, setSearchParams] = useSearchParams();

  const feedbackIdParam = searchParams.get("feedback_id");
  const initialFeedbackId = feedbackIdParam ? Number(feedbackIdParam) : null;
  const activeTab = searchParams.get("tab") ?? "single";

  const { data: aiSettings } = useQuery({
    queryKey: ["ai-settings", "evaluation"],
    queryFn: fetchAiSettings,
  });

  function setTab(tab: string) {
    const params = new URLSearchParams(searchParams);
    params.set("tab", tab);

    // Once the user deliberately switches tabs, drop the one-time
    // feedback_id deep link so it doesn't keep reopening that record.
    if (tab !== "single") {
      params.delete("feedback_id");
    }

    setSearchParams(params);
  }

  return (
    <div>
      <PageHeader
        title="AI Evaluation"
        subtitle="Test, compare, benchmark, and evaluate AI analysis quality before promoting a configuration to production."
        actions={
          aiSettings ? (
            <div className="flex flex-wrap gap-2 text-xs">
              <span className="rounded-full bg-slate-100 px-2.5 py-1 font-medium text-slate-600">
                Production prompt {aiSettings.settings.feedback_prompt_version}
              </span>
              <span className="rounded-full bg-slate-100 px-2.5 py-1 font-medium text-slate-600">
                Executive prompt {aiSettings.settings.executive_prompt_version}
              </span>
            </div>
          ) : undefined
        }
      />

      <div className="mb-6">
        <Tabs items={TAB_ITEMS} value={activeTab} onChange={setTab} />
      </div>

      {activeTab === "single" && (
        <SingleFeedbackTab aiSettings={aiSettings} initialFeedbackId={initialFeedbackId} />
      )}
      {activeTab === "benchmark" && <BenchmarkLabTab aiSettings={aiSettings} />}
      {activeTab === "comparison" && <ModelComparisonTab />}
    </div>
  );
}
