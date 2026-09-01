export function Logo({
  withTagline = true,
  size = "md",
}: {
  withTagline?: boolean;
  size?: "sm" | "md";
}) {
  return (
    <div className="text-center">
      <p className={`font-semibold tracking-tight ${size === "sm" ? "text-base" : "text-4xl"}`}>
        <span className="text-indigo-900">Insight</span>
        <span className="text-teal-800">CX</span>
      </p>
      {withTagline && (
        <p className="mt-1 text-xs font-medium text-teal-800">Every Voice. Every Insight.</p>
      )}
    </div>
  );
}
