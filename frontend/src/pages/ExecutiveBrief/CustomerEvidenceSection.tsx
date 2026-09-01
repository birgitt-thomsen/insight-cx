import { Link } from "react-router-dom";
import { Card, SectionHeader } from "../../components";
import type { CustomerVerbatim } from "../../types/executiveSummary";

export function CustomerEvidenceSection({ verbatims }: { verbatims: CustomerVerbatim[] }) {
  if (verbatims.length === 0) return null;

  return (
    <section>
      <SectionHeader
        title="Customer Evidence"
        subtitle="The feedback behind the conclusions above, with a direct link back to the source record."
      />
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {verbatims.map((verbatim, index) => (
          <Card key={`${verbatim.theme}-${index}`} className="flex flex-col p-5">
            <span className="inline-flex w-fit items-center rounded-full bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-600">
              {verbatim.theme}
            </span>
            <blockquote className="mt-3 flex-1 text-sm italic text-slate-700">
              “{verbatim.comment}”
            </blockquote>
            <Link
              to={`/feedback-explorer?search=${encodeURIComponent(verbatim.comment)}`}
              className="mt-3 text-xs font-medium text-teal-800 hover:text-teal-900"
            >
              View in Feedback Explorer →
            </Link>
          </Card>
        ))}
      </div>
    </section>
  );
}
