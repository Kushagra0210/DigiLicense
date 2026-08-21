"use client"

import Link from "next/link"
import { Menu } from "lucide-react"
import { useState } from "react"
import { Button } from "@/components/ui/button"

export function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false)

  return (
    <header className="sticky top-0 z-50 border-b border-border bg-white/80 backdrop-blur-md">
      <div className="mx-auto flex h-14 max-w-5xl items-center justify-between px-4">
        <Link href="/" className="flex items-center gap-2">
          <span className="text-lg font-bold tracking-tight text-primary">
            DigiLicense
          </span>
          <span className="hidden text-xs text-muted-foreground sm:inline">
            Delhi
          </span>
        </Link>

        <nav className="hidden items-center gap-1 md:flex">
          <Button variant="ghost" size="sm" asChild>
            <Link href="/services">Services</Link>
          </Button>

          <Button variant="ghost" size="sm" asChild>
            <Link href="/status">Track application</Link>
          </Button>
        </nav>

        <div className="flex items-center gap-2">
          <Button
            type="button"
            variant="ghost"
            size="icon-sm"
            className="md:hidden"
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-label={mobileOpen ? "Close navigation menu" : "Open navigation menu"}
            aria-expanded={mobileOpen}
            aria-controls="mobile-navigation"
          >
            <Menu className="size-4" />
          </Button>
        </div>
      </div>

      <div
        id="mobile-navigation"
        hidden={!mobileOpen}
        className="border-t border-border bg-white px-4 pb-4 pt-2 md:hidden"
      >
        <nav className="flex flex-col gap-1">
          <Link
            href="/services"
            className="rounded-md px-3 py-2 text-sm hover:bg-accent"
            onClick={() => setMobileOpen(false)}
          >
            Services
          </Link>
          <Link
            href="/status"
            className="rounded-md px-3 py-2 text-sm hover:bg-accent"
            onClick={() => setMobileOpen(false)}
          >
            Track application
          </Link>
        </nav>
      </div>
    </header>
  )
}
