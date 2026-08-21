import Link from "next/link"
import { Car, FileText, ArrowRight } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { StatusCheck } from "@/components/home/status-check"

export function JourneyCards() {
  return (
    <section
      className="mx-auto max-w-5xl px-4 pt-12"
      aria-labelledby="quick-access-heading"
    >
      <div className="mb-6">
        <h2
          id="quick-access-heading"
          className="text-2xl font-bold tracking-tight"
        >
          Quick access
        </h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Apply for a licence, manage an existing licence, or track an
          application.
        </p>
      </div>

      <div className="quick-access-carousel flex snap-x snap-mandatory items-stretch gap-4 overflow-x-auto overscroll-x-contain scroll-smooth md:grid md:auto-rows-fr md:grid-cols-3 md:overflow-visible">
        <div className="flex w-[85%] shrink-0 snap-start md:w-auto">
          <Card className="h-full w-full">
            <CardContent className="flex h-full flex-col gap-4">
              <div className="flex size-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
                <Car className="size-5" />
              </div>
              <div>
                <h3 className="text-lg font-semibold">
                  Apply for learner licence
                </h3>
                <p className="mt-1 text-sm text-muted-foreground">
                  Submit a learner licence application and complete the learner
                  process.
                </p>
              </div>
              <Button
                variant="outline"
                size="sm"
                className="mt-auto h-9 w-fit max-w-full"
                asChild
              >
                <Link href="/services/learner-licence">
                  Start application
                  <ArrowRight className="size-3.5" />
                </Link>
              </Button>
            </CardContent>
          </Card>
        </div>

        <div className="flex w-[85%] shrink-0 snap-start md:w-auto">
          <Card className="h-full w-full">
            <CardContent className="flex h-full flex-col gap-4">
              <div className="flex size-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
                <FileText className="size-5" />
              </div>
              <div>
                <h3 className="text-lg font-semibold">
                  Manage licence
                </h3>
                <p className="mt-1 text-sm text-muted-foreground">
                  Renew, replace, or update an existing licence.
                </p>
              </div>
              <Button
                variant="outline"
                size="sm"
                className="mt-auto h-9 w-fit max-w-full"
                asChild
              >
                <Link href="/services/dl-renewal">
                  Manage licence
                  <ArrowRight className="size-3.5" />
                </Link>
              </Button>
            </CardContent>
          </Card>
        </div>

        <div className="flex w-[85%] shrink-0 snap-start md:w-auto">
          <StatusCheck />
        </div>

        <div className="w-[15%] shrink-0 md:hidden" aria-hidden="true" />
      </div>
    </section>
  )
}
