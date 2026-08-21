import Link from "next/link"
import { ArrowRight } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { services } from "@/lib/services"

export function ServicesCarousel() {
  return (
    <section className="overflow-hidden px-4 py-12">
      <div className="mx-auto max-w-5xl">
        <div className="mb-6">
          <h2 className="text-2xl font-bold tracking-tight">
            Driving licence services
          </h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Review applications, updates, appointments, payments, and status
            services.
          </p>
        </div>
      </div>

      <div
        className="services-marquee mx-auto hidden max-w-5xl md:block"
        aria-label="Driving licence services"
      >
        <div className="services-marquee-track">
          {[false, true].map((isDuplicate) => (
            <div
              key={String(isDuplicate)}
              className="flex shrink-0 gap-4 pr-4"
              aria-hidden={isDuplicate || undefined}
            >
              {services.map((service) => (
                <Card key={service.href} className="w-[280px] shrink-0">
                  <CardContent className="flex flex-col gap-3">
                    <div className="flex size-9 items-center justify-center rounded-lg bg-primary/10 text-primary">
                      <service.icon className="size-4.5" />
                    </div>
                    <div>
                      <h3 className="font-semibold">{service.name}</h3>
                      <p className="mt-1 text-sm text-muted-foreground">
                        {service.description}
                      </p>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ))}
        </div>
      </div>

      <div className="mx-auto grid max-w-md grid-cols-2 gap-3 md:hidden">
        {services.slice(0, 4).map((service) => (
          <Link
            key={service.href}
            href={service.href}
            className="group block h-full rounded-xl transition-transform active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
          >
            <Card className="h-full min-w-0 gap-4 py-4 transition-colors group-active:bg-accent/50">
              <CardContent className="flex flex-col gap-3 px-4">
                <div className="flex size-9 items-center justify-center rounded-lg bg-primary/10 text-primary">
                  <service.icon className="size-4.5" />
                </div>
                <h3 className="text-sm font-semibold leading-snug">
                  {service.name}
                </h3>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>

      <div className="mx-auto max-w-5xl">
        <div className="mt-6 text-center">
          <Button variant="ghost" size="sm" asChild>
            <Link href="/services">
              More services
              <ArrowRight className="size-3.5" />
            </Link>
          </Button>
        </div>
      </div>
    </section>
  )
}
