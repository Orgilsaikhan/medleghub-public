import type { Metadata } from "next";
import { Suspense } from "react";

import { CourseGridSkeleton } from "@/components/courses/course-grid";
import { CtaSection } from "@/components/marketing/cta-section";
import { FeaturedCourses } from "@/components/marketing/featured-courses";
import { Hero } from "@/components/marketing/hero";
import { HowItWorks } from "@/components/marketing/how-it-works";
import { LiveShowcase } from "@/components/marketing/live-showcase";
import { Section } from "@/components/marketing/section";
import { WhyLearnHere } from "@/components/marketing/why-learn-here";
import { JsonLd } from "@/components/seo/json-ld";
import { mn } from "@/lib/i18n/mn";
import { organizationJsonLd, pageMetadata, websiteJsonLd } from "@/lib/seo";

export const metadata: Metadata = pageMetadata({
  title: mn.seo.homeTitle,
  description: mn.seo.homeDescription,
  path: "/",
  absoluteTitle: true,
});

export default function HomePage() {
  return (
    <>
      <JsonLd data={[organizationJsonLd(), websiteJsonLd()]} />
      <Hero />
      <LiveShowcase />

      {/* Онцлох сургалтууд API-аас ирэх хүртэл бусад хэсэг хүлээхгүй. */}
      <Suspense
        fallback={
          <Section title={mn.home.featuredTitle} subtitle={mn.home.featuredSubtitle}>
            <CourseGridSkeleton count={3} />
          </Section>
        }
      >
        <FeaturedCourses />
      </Suspense>

      <HowItWorks />
      <WhyLearnHere />
      <CtaSection />
    </>
  );
}
