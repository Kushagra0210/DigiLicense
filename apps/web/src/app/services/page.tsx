import Link from "next/link"
import { ArrowLeft, ArrowRight } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { services } from "@/lib/services"

export default function ServicesPage() {
  return (
    <div className="mx-auto max-w-5xl px-4 py-12">
      <Button
        asChild
        variant="ghost"
        size="sm"
        className="-ml-2 mb-4 text-muted-foreground"
      >
        <Link href="/">
          <ArrowLeft className="size-3.5" />
          Back to home
        </Link>
      </Button>

      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">
          Driving licence services
        </h1>
        <p className="mt-2 text-muted-foreground">
          Select a service to apply, update licence details, book a driving
          test, pay fees, or track an application.
        </p>
      </div>

      <div className="grid auto-rows-fr gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {services.map((service) => (
          <Link
            key={service.href}
            href={service.href}
            className="group block h-full"
          >
            <Card className="h-full">
              <CardContent className="flex h-full flex-col gap-3">
                <div className="flex size-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
                  <service.icon className="size-5" />
                </div>
                <div>
                  <h2 className="font-semibold">{service.name}</h2>
                  <p className="mt-1 text-sm text-muted-foreground">
                    {service.description}
                  </p>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  className="mt-auto w-fit px-0"
                >
                  Open service
                  <ArrowRight className="size-3.5" />
                </Button>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  )
}
