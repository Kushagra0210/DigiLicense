import {
  BookOpen,
  Car,
  RefreshCw,
  Copy,
  MapPin,
  Smartphone,
  Calendar,
  CreditCard,
  FileSearch,
  Upload,
} from "lucide-react"

export interface Service {
  name: string
  description: string
  href: string
  icon: React.ComponentType<{ className?: string }>
  shortLabel: string
}

export const services: Service[] = [
  {
    name: "Apply for learner licence",
    shortLabel: "Apply for learner licence",
    description:
      "Submit a learner licence application and complete the learner test.",
    href: "/services/learner-licence",
    icon: BookOpen,
  },
  {
    name: "Apply for licence",
    shortLabel: "Apply for licence",
    description:
      "Submit a permanent licence application after the learner period.",
    href: "/services/driving-licence",
    icon: Car,
  },
  {
    name: "Renew licence",
    shortLabel: "Renew licence",
    description: "Renew an expiring or expired licence.",
    href: "/services/dl-renewal",
    icon: RefreshCw,
  },
  {
    name: "Replace licence",
    shortLabel: "Replace licence",
    description:
      "Request a replacement for a lost, stolen, or damaged licence.",
    href: "/services/duplicate-dl",
    icon: Copy,
  },
  {
    name: "Change licence address",
    shortLabel: "Change licence address",
    description: "Update the address on an existing licence.",
    href: "/services/change-address",
    icon: MapPin,
  },
  {
    name: "Update mobile number",
    shortLabel: "Update mobile number",
    description:
      "Update the mobile number linked to a licence.",
    href: "/services/mobile-update",
    icon: Smartphone,
  },
  {
    name: "Book driving test",
    shortLabel: "Book driving test",
    description:
      "Book or change a driving test appointment, or join the waitlist.",
    href: "/services/appointments",
    icon: Calendar,
  },
  {
    name: "Pay licence fees",
    shortLabel: "Pay licence fees",
    description:
      "View application and test fees, then make a simulated payment.",
    href: "/services/fee-payments",
    icon: CreditCard,
  },
  {
    name: "Track application",
    shortLabel: "Track application",
    description: "Check the current stage and next action for an application.",
    href: "/status",
    icon: FileSearch,
  },
  {
    name: "Upload documents",
    shortLabel: "Upload documents",
    description:
      "Upload the identity, address, or medical documents required for an application.",
    href: "/services/upload-document",
    icon: Upload,
  },
]
