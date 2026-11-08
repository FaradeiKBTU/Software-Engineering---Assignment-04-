export interface BookingInterval {
  start: number;
  end: number;
}

export type AvailabilityStatus = "available" | "unavailable";

export interface AvailabilityResult {
  status: AvailabilityStatus;
  reason: string;
}

export interface ValidationIssue {
  field: "start" | "end" | "range" | "duration";
  message: string;
}

export interface ValidationResult {
  ok: boolean;
  issues: ValidationIssue[];
}

export const MAX_DURATION_MINUTES = 120;
export const MINUTES_IN_DAY = 1440;

export const DEFAULT_BOOKINGS: BookingInterval[] = [
  { start: 600, end: 660 },
  { start: 900, end: 960 },
];

export function minutesToHHMM(minutes: number): string {
  const m = Math.max(0, Math.min(MINUTES_IN_DAY, Math.round(minutes)));
  const h = Math.floor(m / 60);
  const mm = m % 60;
  return `${h.toString().padStart(2, "0")}:${mm.toString().padStart(2, "0")}`;
}

export function intervalsOverlap(a: BookingInterval, b: BookingInterval): boolean {
  return a.start < b.end && b.start < a.end;
}

export function validateInput(
  start: number,
  end: number,
  now: number
): ValidationResult {
  const issues: ValidationIssue[] = [];

  if (!Number.isFinite(start)) {
    issues.push({ field: "start", message: "Start time must be a number." });
  }
  if (!Number.isFinite(end)) {
    issues.push({ field: "end", message: "End time must be a number." });
  }
  if (issues.length > 0) {
    return { ok: false, issues };
  }

  if (start < 0 || start > MINUTES_IN_DAY) {
    issues.push({
      field: "start",
      message: `Start must be between 0 and ${MINUTES_IN_DAY}.`,
    });
  }
  if (end < 0 || end > MINUTES_IN_DAY) {
    issues.push({
      field: "end",
      message: `End must be between 0 and ${MINUTES_IN_DAY}.`,
    });
  }

  if (!Number.isInteger(start)) {
    issues.push({ field: "start", message: "Start must be a whole number." });
  }
  if (!Number.isInteger(end)) {
    issues.push({ field: "end", message: "End must be a whole number." });
  }

  if (issues.length > 0) {
    return { ok: false, issues };
  }

  if (start >= end) {
    issues.push({
      field: "range",
      message: "Start must be strictly before end.",
    });
    return { ok: false, issues };
  }

  if (start <= now) {
    issues.push({
      field: "range",
      message: `Start must be after the current time (${minutesToHHMM(now)}).`,
    });
  }

  const duration = end - start;
  if (duration > MAX_DURATION_MINUTES) {
    issues.push({
      field: "duration",
      message: `Duration must not exceed ${MAX_DURATION_MINUTES} minutes (you entered ${duration}).`,
    });
  }

  return { ok: issues.length === 0, issues };
}

export function canBook(
  start: number,
  end: number,
  now: number,
  blocked: boolean,
  existing: BookingInterval[]
): AvailabilityResult {
  const validation = validateInput(start, end, now);
  if (!validation.ok) {
    return {
      status: "unavailable",
      reason: validation.issues[0].message,
    };
  }

  if (blocked) {
    return {
      status: "unavailable",
      reason: "Sunset Lounge is blocked and cannot be booked right now.",
    };
  }

  const request: BookingInterval = { start, end };
  const conflict = existing.find((b) => intervalsOverlap(request, b));

  if (conflict) {
    return {
      status: "unavailable",
      reason: `Overlaps an existing booking (${minutesToHHMM(conflict.start)}–${minutesToHHMM(conflict.end)}).`,
    };
  }

  return {
    status: "available",
    reason: `Sunset Lounge is free ${minutesToHHMM(start)}–${minutesToHHMM(end)}.`,
  };
}
