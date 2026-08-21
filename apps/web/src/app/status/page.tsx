import { StatusCheck } from "@/components/home/status-check"

export default function StatusPage() {
  return (
    <div className="mx-auto max-w-md px-4 py-12">
      <div className="mb-6">
        <h1 className="text-3xl font-bold tracking-tight">Track application</h1>
        <p className="mt-2 text-muted-foreground">
          Enter a synthetic application number. This prototype does not access
          government records.
        </p>
      </div>
      <StatusCheck />
    </div>
  )
}
