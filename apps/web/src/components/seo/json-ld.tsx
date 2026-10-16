/**
 * Бүтэцлэгдсэн өгөгдөл (schema.org JSON-LD) — Next-ийн зөвлөмжөөр хуудас
 * дотор `<script>` болгож render хийнэ. `<`-г escape хийж, агуулга дахь
 * `</script>` нь tag-ийг хаахаас сэргийлнэ.
 */
export function JsonLd({ data }: { data: object | object[] }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data).replace(/</g, "\\u003c") }}
    />
  );
}
