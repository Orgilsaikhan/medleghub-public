/**
 * Сургалтын урьдчилсан мэдлэг — сургалтын хуудсанд анхааруулга болж гарна.
 *
 * Зөвхөн анхааруулга: сурагч аль хэдийн мэддэг бол шууд эхэлж болно.
 * Сургалтын `slug`-аар түлхүүрлэнэ.
 */
export const COURSE_PREREQUISITES: Record<string, { slug: string; title: string }[]> = {
  "react-app-buteeh": [
    { slug: "javascript-undes", title: "JavaScript үндэс" },
    { slug: "html-css-undes", title: "HTML & CSS үндэс" },
  ],
};
