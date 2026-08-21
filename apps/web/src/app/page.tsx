import { HeroSection } from "@/components/home/hero-section"
import { ServicesCarousel } from "@/components/home/services-carousel"
import { JourneyCards } from "@/components/home/journey-cards"

export default function Home() {
  return (
    <>
      <HeroSection />
      <JourneyCards />
      <ServicesCarousel />
    </>
  )
}
