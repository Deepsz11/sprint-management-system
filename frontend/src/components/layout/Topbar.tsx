import { LogOut, Menu, Moon, Sun } from "lucide-react";

import { Button } from "@/components/ui/Button";
import { useAuth } from "@/features/auth/useAuth";
import { useTheme } from "@/providers/ThemeProvider";

interface TopbarProps {
  readonly onOpenSidebar: () => void;
}

function initials(name: string): string {
  return name
    .split(/\s+/)
    .map((part) => part[0])
    .filter(Boolean)
    .slice(0, 2)
    .join("")
    .toUpperCase();
}

export function Topbar({ onOpenSidebar }: TopbarProps) {
  const { user, logout } = useAuth();
  const { resolvedTheme, toggleTheme } = useTheme();

  return (
    <header className="sticky top-0 z-20 flex h-16 items-center justify-between gap-4 border-b border-border bg-background/95 px-4 backdrop-blur">
      <div className="flex items-center gap-2">
        <Button
          type="button"
          variant="ghost"
          size="icon"
          className="md:hidden"
          onClick={onOpenSidebar}
          aria-label="Open sidebar"
        >
          <Menu className="h-5 w-5" />
        </Button>
        <div className="hidden md:block">
          <h1 className="text-sm font-semibold">Sprint Outcome Tracer</h1>
          <p className="text-xs text-muted-foreground">
            Trace engineering work to business outcomes
          </p>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <Button
          type="button"
          variant="ghost"
          size="icon"
          onClick={toggleTheme}
          aria-label="Toggle theme"
        >
          {resolvedTheme === "dark" ? (
            <Sun className="h-4 w-4" />
          ) : (
            <Moon className="h-4 w-4" />
          )}
        </Button>

        {user && (
          <div className="flex items-center gap-3 rounded-md border border-border bg-card px-3 py-1.5">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-xs font-semibold text-primary-foreground">
              {initials(user.full_name)}
            </div>
            <div className="hidden sm:block">
              <p className="text-sm font-medium leading-none">{user.full_name}</p>
              <p className="text-xs text-muted-foreground">{user.email}</p>
            </div>
          </div>
        )}

        <Button
          type="button"
          variant="outline"
          size="sm"
          onClick={() => void logout()}
        >
          <LogOut className="h-4 w-4" />
          <span className="hidden sm:inline">Log out</span>
        </Button>
      </div>
    </header>
  );
}