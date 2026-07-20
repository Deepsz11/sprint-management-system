import { NavLink } from "react-router-dom";

import {
  PRIMARY_NAVIGATION,
  SECONDARY_NAVIGATION,
  type NavigationItem,
} from "@/config/navigation";
import { ENV } from "@/config/env";
import { cn } from "@/lib/utils";

interface SidebarProps {
  readonly isOpen: boolean;
  readonly onClose: () => void;
}

function NavItem({ item }: { item: NavigationItem }) {
  const Icon = item.icon;
  return (
    <NavLink
      to={item.path}
      className={({ isActive }) =>
        cn(
          "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
          isActive
            ? "bg-primary text-primary-foreground"
            : "text-muted-foreground hover:bg-accent hover:text-accent-foreground",
        )
      }
    >
      <Icon className="h-4 w-4" aria-hidden="true" />
      <span className="truncate">{item.label}</span>
    </NavLink>
  );
}

export function Sidebar({ isOpen, onClose }: SidebarProps) {
  return (
    <>
      {isOpen && (
        <div
          role="presentation"
          onClick={onClose}
          className="fixed inset-0 z-30 bg-background/60 backdrop-blur-sm md:hidden"
        />
      )}
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-border bg-card transition-transform duration-200 md:sticky md:top-0 md:translate-x-0",
          isOpen ? "translate-x-0" : "-translate-x-full",
        )}
      >
        <div className="flex h-16 shrink-0 items-center gap-2 border-b border-border px-4">
          <span className="text-sm font-semibold uppercase tracking-widest text-primary">
            SBOT
          </span>
          <span className="truncate text-sm text-muted-foreground">
            {ENV.APP_NAME}
          </span>
        </div>
        <nav className="flex-1 overflow-y-auto px-3 py-4">
          <div className="space-y-1">
            {PRIMARY_NAVIGATION.map((item) => (
              <NavItem key={item.path} item={item} />
            ))}
          </div>
          <div className="mt-8 space-y-1">
            <p className="px-3 pb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Account
            </p>
            {SECONDARY_NAVIGATION.map((item) => (
              <NavItem key={item.path} item={item} />
            ))}
          </div>
        </nav>
      </aside>
    </>
  );
}