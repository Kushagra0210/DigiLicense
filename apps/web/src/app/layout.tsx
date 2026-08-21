import type { Metadata } from "next"
import { Navbar } from "@/components/layout/navbar"
import { Footer } from "@/components/layout/footer"
import "./globals.css"

export const metadata: Metadata = {
  title: "DigiLicense — Delhi",
  description:
    "Apply, track, and manage your services in Delhi.",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="flex min-h-screen flex-col bg-gray-50 text-gray-900 antialiased">
        <Navbar />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  )
}
