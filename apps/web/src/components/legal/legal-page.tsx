import { LegalLanguageTabs } from "@/components/legal/legal-language-tabs";
import { LegalMarkdown } from "@/components/legal/legal-markdown";
import { readLegalDocument, type LegalDocument } from "@/lib/legal";

/** Нууцлалын бодлого, Үйлчилгээний нөхцөлийн нийтлэг бүтэц — хоёр хэлээр. */
export function LegalPage({ doc }: { doc: LegalDocument }) {
  return (
    <div className="container-page py-10 lg:py-14">
      <article className="mx-auto max-w-3xl">
        <LegalLanguageTabs
          mn={<LegalMarkdown source={readLegalDocument(doc, "mn")} />}
          en={<LegalMarkdown source={readLegalDocument(doc, "en")} />}
        />
      </article>
    </div>
  );
}
