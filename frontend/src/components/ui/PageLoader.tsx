import { Spinner } from "./Spinner";

export function PageLoader() {
  return (
    <div className="flex h-full min-h-[60vh] w-full items-center justify-center">
      <Spinner className="text-muted-foreground" />
    </div>
  );
}