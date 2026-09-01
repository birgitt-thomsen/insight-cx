import { useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { fetchAiSettings } from "../../api/aiSettings";
import { fetchLatestExecutiveSummary } from "../../api/executiveSummary";
import { PageHeader, Tabs } from "../../components";
import { formatDateTime } from "../../lib/format";
import { AiConfigurationTab } from "./AiConfigurationTab";
import { ExecutiveSummaryTab } from "./ExecutiveSummaryTab";
import { MaintenanceTab } from "./MaintenanceTab";

const TAB_ITEMS = [
  { value: "configuration", label: "AI Configuration" },
  { value: "executive-summary", label: "Executive Summary" },
  { value: "maintenance", label: "Maintenance" },
];

export default function Administration() {
  const [searchParams, setSearchParams] = useSearchParams();
  const activeTab = searchParams.get("tab") ?? "configuration";

  const { data: aiSettings } = useQuery({
    queryKey: ["ai-settings", "administration"],
    queryFn: fetchAiSettings,
  });

  const { data: summaryData } = useQuery({
    queryKey: ["executive-summary", "latest"],
    queryFn: fetchLatestExecutiveSummary,
  });

  function setTab(tab: string) {
    const params = new URLSearchParams(searchParams);
    params.set("tab", tab);
    setSearchParams(params);
  }

  return (
    <div>
      <PageHeader
        title="Administration"
        subtitle="Control the models, prompts, and maintenance operations behind InsightCX analysis."
        actions={
          aiSettings ? (
            <div className="flex flex-wrap gap-2 text-xs">
              <span className="rounded-full bg-slate-100 px-2.5 py-1 font-medium text-slate-600">
                Analysis {aiSettings.settings.feedback_model}
              </span>
              <span className="rounded-full bg-slate-100 px-2.5 py-1 font-medium text-slate-600">
                Executive {aiSettings.settings.executive_model}
              </span>
              {summaryData?.latest && (
                <span className="rounded-full bg-slate-100 px-2.5 py-1 font-medium text-slate-600">
                  Last generated {formatDateTime(summaryData.latest.generated_at)}
                </span>
              )}
            </div>
          ) : undefined
        }
      />

      <div className="mb-6">
        <Tabs items={TAB_ITEMS} value={activeTab} onChange={setTab} />
      </div>

      {activeTab === "configuration" && <AiConfigurationTab aiSettings={aiSettings} />}
      {activeTab === "executive-summary" && <ExecutiveSummaryTab aiSettings={aiSettings} />}
      {activeTab === "maintenance" && <MaintenanceTab />}
    </div>
  );
}
