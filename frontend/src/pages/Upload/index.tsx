import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { uploadFeedbackCsv } from "../../api/upload";
import type { UploadResult } from "../../api/upload";
import { Card, PageHeader } from "../../components";
import { parseCsvPreview } from "../../lib/csv";
import type { CsvPreviewResult } from "../../lib/csv";
import { UploadStepper } from "./UploadStepper";
import { UploadDropzone } from "./UploadDropzone";
import { UploadPreview } from "./UploadPreview";
import { UploadConfirmation } from "./UploadConfirmation";

type Stage = "select" | "preview" | "done";

export default function Upload() {
  const [stage, setStage] = useState<Stage>("select");
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<CsvPreviewResult | null>(null);
  const [selectError, setSelectError] = useState<string | null>(null);
  const [result, setResult] = useState<UploadResult | null>(null);

  const uploadMutation = useMutation({
    mutationFn: (selectedFile: File) => uploadFeedbackCsv(selectedFile),
    onSuccess: (data) => {
      setResult(data);
      setStage("done");
    },
  });

  async function handleFileSelected(selectedFile: File) {
    setSelectError(null);

    if (!selectedFile.name.toLowerCase().endsWith(".csv")) {
      setSelectError("Only CSV files are allowed.");
      return;
    }

    try {
      const text = await selectedFile.text();
      const parsed = parseCsvPreview(text);

      if (!parsed) {
        setSelectError("This file appears to be empty.");
        return;
      }

      setFile(selectedFile);
      setPreview(parsed);
      setStage("preview");
    } catch {
      setSelectError("Could not read this file. Please try again.");
    }
  }

  function reset() {
    setStage("select");
    setFile(null);
    setPreview(null);
    setSelectError(null);
    setResult(null);
    uploadMutation.reset();
  }

  const stepIndex =
    stage === "select" ? 0 : stage === "preview" ? (uploadMutation.isPending ? 2 : 1) : 3;

  return (
    <div>
      <PageHeader
        title="Upload"
        subtitle="Import NPS and CSAT feedback datasets for AI analysis and executive reporting."
      />

      <Card className="p-6">
        <div className="mb-6">
          <UploadStepper currentIndex={stepIndex} />
        </div>

        {stage === "select" && (
          <UploadDropzone onFileSelected={handleFileSelected} error={selectError} />
        )}

        {stage === "preview" && file && preview && (
          <UploadPreview
            fileName={file.name}
            preview={preview}
            isImporting={uploadMutation.isPending}
            importError={
              uploadMutation.isError
                ? uploadMutation.error instanceof Error
                  ? uploadMutation.error.message
                  : "Import failed."
                : null
            }
            onImport={() => uploadMutation.mutate(file)}
            onChooseDifferentFile={reset}
          />
        )}

        {stage === "done" && result && (
          <UploadConfirmation result={result} onUploadAnother={reset} />
        )}
      </Card>
    </div>
  );
}
