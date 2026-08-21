import Link from "next/link"
import { ArrowLeft } from "lucide-react"
import { notFound } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { services } from "@/lib/services"

type ServicePageProps = {
  params: Promise<{ slug: string }>
}

const serviceEntries = services.flatMap((service) => {
  const slug = service.href.startsWith("/services/")
    ? service.href.slice("/services/".length)
    : null

  return slug ? [{ service, slug }] : []
})

export function generateStaticParams() {
  return serviceEntries.map(({ slug }) => ({ slug }))
}

export default async function ServicePage({ params }: ServicePageProps) {
  const { slug } = await params
  const entry = serviceEntries.find((item) => item.slug === slug)

  if (!entry) {
    notFound()
  }

  const { service } = entry
  const ServiceIcon = service.icon

  return (
    <div className="mx-auto max-w-2xl px-4 py-12">
      <Button variant="ghost" size="sm" className="mb-6" asChild>
        <Link href="/services">
          <ArrowLeft className="size-3.5" />
          All services
        </Link>
      </Button>

      <Card>
        <CardContent className="space-y-5">
          <div className="flex size-11 items-center justify-center rounded-lg bg-primary/10 text-primary">
            <ServiceIcon className="size-5" />
          </div>
          <div>
            <p className="mb-2 text-xs font-medium text-muted-foreground">
              Independent prototype
            </p>
            <h1 className="text-3xl font-bold tracking-tight">
              {service.name}
            </h1>
            <p className="mt-3 text-muted-foreground">
              {service.description}
            </p>
          </div>
          <div className="rounded-lg border bg-muted/50 p-4 text-sm">
            This route is available for the prototype. It does not submit data
            to a government system.
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
