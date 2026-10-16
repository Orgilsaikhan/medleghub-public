import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { cache } from "react";

import { CourseDetailView } from "@/components/courses/course-detail-view";
import { JsonLd } from "@/components/seo/json-ld";
import { ApiError } from "@/lib/api/client";
import { getCourse } from "@/lib/api/courses";
import { mn } from "@/lib/i18n/mn";
import {
  breadcrumbJsonLd,
  courseJsonLd,
  courseSeoTitle,
  pageMetadata,
  trimDescription,
} from "@/lib/seo";
import type { CourseDetail } from "@/lib/types/api";

/** Metadata ба хуудас хоёулаа ашиглана — нэг хүсэлтэд API-г нэг л удаа дуудна. */
const loadCourse = cache(async (slug: string): Promise<CourseDetail> => {
  try {
    return await getCourse(slug, { cache: "no-store" });
  } catch (error) {
    if (error instanceof ApiError && error.isNotFound) notFound();
    throw error;
  }
});

export async function generateMetadata({
  params,
}: PageProps<"/courses/[slug]">): Promise<Metadata> {
  const { slug } = await params;
  try {
    const course = await loadCourse(slug);
    return pageMetadata({
      title: courseSeoTitle(course),
      description: trimDescription(course.description),
      path: `/courses/${course.slug}`,
      // Хичээлгүй («тун удахгүй») сургалт — хоосон хуудсыг индекслэхгүй.
      noindex: course.lesson_count === 0,
      image: course.thumbnail_url ? { url: course.thumbnail_url, alt: course.title } : undefined,
    });
  } catch {
    return {};
  }
}

export default async function CourseDetailPage({ params }: PageProps<"/courses/[slug]">) {
  const { slug } = await params;
  const course = await loadCourse(slug);
  return (
    <>
      <JsonLd
        data={[
          courseJsonLd(course),
          breadcrumbJsonLd([
            { name: mn.seo.home, path: "/" },
            { name: mn.courses.title, path: "/courses" },
            { name: course.title, path: `/courses/${course.slug}` },
          ]),
        ]}
      />
      <CourseDetailView initialCourse={course} />
    </>
  );
}
