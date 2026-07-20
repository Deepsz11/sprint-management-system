import { cn } from "@/lib/utils";

import type { KPI, KPIDirection, KPIHealth } from "../types";

const HEALTH_STYLES: Record<KPIHealth, string> = {
  on_track:
    "border border-emerald-500/40 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300",
  at_risk:
    "border border-amber-500/40 bg-amber-500/10 text-amber-700 dark:text-amber-300",
  off_track:
    "border border-destructive/40 bg-destructive/10 text-destructive",
  achieved:
    "border border-violet-500/40 bg-violet-500/10 text-violet-700 dark:text-violet-300",
};

const HEALTH_LABELS: Record<KPIHealth, string> = {
  on_track: "On Track",
  at_risk: "At Risk",
  off_track: "Off Track",
  achieved: "Achieved",
};

function toNumber(value: string | number | null | undefined): number | null {
  if (value === null || value === undefined) return null;
  const parsed = typeof value === "number" ? value : Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function withinTolerance(
  current: number,
  baseline: number,
  tolerance = 0.05,
): boolean {
  if (baseline === 0) return current === 0;
  return Math.abs(current - baseline) <= Math.abs(baseline) * tolerance;
}

export function deriveKPIHealth(kpi: KPI): KPIHealth {
  const baseline = toNumber(kpi.baseline_value);
  const target = toNumber(kpi.target_value);
  const current = toNumber(kpi.current_value);
  const direction: KPIDirection = kpi.direction;

  if (!kpi.is_active) {
    return "off_track";
  }
  if (current === null) {
    return "at_risk";
  }
  if (target !== null) {
    if (direction === "increase" && current >= target) return "achieved";
    if (direction === "decrease" && current <= target) return "achieved";
    if (direction === "maintain" && baseline !== null) {
      if (withinTolerance(current, baseline, 0.02)) return "achieved";
    }
  }
  if (baseline === null || target === null) {
    return "at_risk";
  }

  const span = target - baseline;
  if (span === 0) {
    if (direction === "maintain" && withinTolerance(current, baseline)) {
      return "on_track";
    }
    return "at_risk";
  }
  const progress = (current - baseline) / span;
  if (direction === "increase") {
    if (progress >= 0.9) return "on_track";
    if (progress >= 0.5) return "at_risk";
    return "off_track";
  }
  if (direction === "decrease") {
    if (progress >= 0.9) return "on_track";
    if (progress >= 0.5) return "at_risk";
    return "off_track";
  }
  return withinTolerance(current, baseline) ? "on_track" : "at_risk";
}

interface KPIStatusBadgeProps {
  readonly kpi: KPI;
}

export function KPIStatusBadge({ kpi }: KPIStatusBadgeProps) {
  const health = deriveKPIHealth(kpi);
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium",
        HEALTH_STYLES[health],
      )}
    >
      {HEALTH_LABELS[health]}
    </span>
  );
}

export { HEALTH_LABELS };