import { createContext, useCallback, useContext, useMemo, useState } from "react";

import { cn } from "@/lib/utils";

export type ToastVariant = "default" | "success" | "error";

export interface Toast {
  readonly id: string;
  readonly title?: string;
  readonly description?: string;
  readonly variant: ToastVariant;
}

interface ToastContextValue {
  readonly toast: (input: Omit<Toast, "id" | "variant"> & { variant?: ToastVariant }) => void;
  readonly dismiss: (id: string) => void;
}

const ToastContext = createContext<ToastContextValue | undefined>(undefined);

interface ToastProviderProps {
  readonly children: React.ReactNode;
}

const AUTO_DISMISS_MS = 4500;

export function ToastProvider({ children }: ToastProviderProps) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const dismiss = useCallback((id: string) => {
    setToasts((current) => current.filter((t) => t.id !== id));
  }, []);

  const toast = useCallback<ToastContextValue["toast"]>(
    (input) => {
      const id = crypto.randomUUID();
      const next: Toast = {
        id,
        title: input.title,
        description: input.description,
        variant: input.variant ?? "default",
      };
      setToasts((current) => [...current, next]);
      window.setTimeout(() => dismiss(id), AUTO_DISMISS_MS);
    },
    [dismiss],
  );

  const value = useMemo<ToastContextValue>(
    () => ({ toast, dismiss }),
    [toast, dismiss],
  );

  return (
    <ToastContext.Provider value={value}>
      {children}
      <div
        aria-live="polite"
        className="pointer-events-none fixed inset-x-0 top-0 z-[100] flex flex-col items-center gap-2 p-4 sm:items-end"
      >
        {toasts.map((t) => (
          <div
            key={t.id}
            role="status"
            className={cn(
              "pointer-events-auto w-full max-w-sm rounded-md border p-4 shadow-lg backdrop-blur",
              t.variant === "success" &&
                "border-emerald-500/40 bg-emerald-500/10 text-emerald-900 dark:text-emerald-100",
              t.variant === "error" &&
                "border-destructive/40 bg-destructive/10 text-destructive",
              t.variant === "default" &&
                "border-border bg-card text-card-foreground",
            )}
          >
            {t.title && <p className="text-sm font-medium">{t.title}</p>}
            {t.description && (
              <p className="mt-1 text-sm opacity-90">{t.description}</p>
            )}
            <button
              type="button"
              onClick={() => dismiss(t.id)}
              className="mt-2 text-xs font-medium underline-offset-2 hover:underline"
            >
              Dismiss
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast(): ToastContextValue {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error("useToast must be used within a ToastProvider");
  return ctx;
}