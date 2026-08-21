import { Separator } from "@/components/ui/separator"

export function Footer() {
  return (
    <footer className="mt-auto border-t border-border bg-white">
      <div className="mx-auto max-w-5xl px-4 py-6">
        <div className="flex flex-col items-center gap-3 text-xs text-muted-foreground sm:flex-row sm:justify-between">
          <p>
            This is an independent prototype, not an official government service.
          </p>
          <div className="flex gap-4">
            <a href="#" className="hover:text-foreground">
              Contact
            </a>
            <a href="#" className="hover:text-foreground">
              Privacy
            </a>
            <a href="#" className="hover:text-foreground">
              Terms
            </a>
          </div>
        </div>
        <Separator className="my-4" />
        <p className="text-center text-[11px] text-muted-foreground">
          &copy; 2026 DigiLicense. Built for the Build What Moves India hackathon.
          All data is synthetic.
        </p>
      </div>
    </footer>
  )
}
