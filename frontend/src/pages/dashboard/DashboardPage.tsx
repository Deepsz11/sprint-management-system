import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/Card";
import { useAuth } from "@/features/auth/useAuth";

const STATS: ReadonlyArray<{
  label: string;
  value: string;
  description: string;
}> = [
  {
    label: "Active Sprints",
    value: "—",
    description: "Sprints currently in progress",
  },
  {
    label: "Outcomes On Track",
    value: "—",
    description: "Business outcomes with healthy progress",
  },
  {
    label: "KPIs Monitored",
    value: "—",
    description: "Metrics under active tracking",
  },
  {
    label: "Attribution Coverage",
    value: "—",
    description: "Completed work items linked to outcomes",
  },
];

export default function DashboardPage() {
  const { user } = useAuth();

  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-2xl font-semibold tracking-tight">
          Welcome{user ? `, ${user.full_name.split(" ")[0]}` : ""}.
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Your organization's business outcome tracker.
        </p>
      </header>

      <section
        aria-label="Key metrics"
        className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4"
      >
        {STATS.map((stat) => (
          <Card key={stat.label}>
            <CardHeader className="pb-2">
              <CardDescription className="text-xs uppercase tracking-wide">
                {stat.label}
              </CardDescription>
              <CardTitle className="text-3xl">{stat.value}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                {stat.description}
              </p>
            </CardContent>
          </Card>
        ))}
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Recent Sprints</CardTitle>
            <CardDescription>
              Sprint activity across your projects will appear here.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Once modules are enabled, this panel will summarize sprint
              velocity, completion rate, and outcome attribution.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Outcomes At Risk</CardTitle>
            <CardDescription>
              Outcomes flagged as at risk or off track will be listed here.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Progress vs. time-elapsed will drive automated risk detection
              once outcomes and KPIs are populated.
            </p>
          </CardContent>
        </Card>
      </section>
    </div>
  );
}