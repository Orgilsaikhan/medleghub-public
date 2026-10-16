import { SiteHeader } from "@/components/layout/site-header";

/**
 * Хичээлийн бүтэн дэлгэцийн layout.
 *
 * Footer байхгүй — анхаарлыг хичээл дээр төвлөрүүлнэ.
 *
 * Хуудас БҮХЭЛДЭЭ ГҮЙЛГЭГДЭХГҮЙ: өндөр нь яг дэлгэцийн өндөртэй тэнцүү
 * бөгөөд зөвхөн доторх хэсгүүд тус тусдаа гүйлгэгдэнэ. Үгүй бол агуулга
 * дуусахад хоосон дэвсгэр рүү гүйлгэгдэж, засварлагч нүднээс алга болдог.
 *
 * `100dvh` нь гар утасны хаяг оруулах мөр нуугдахад ч зөв өндөр өгнө.
 *
 * `data-hide-chat-widget`: чатботын товч засварлагчийн доод мөрний «Тест
 * ажиллуулах», «Илгээх» товчийг дардаг тул хичээлд нуугдана (`globals.css`).
 */
export default function LearnLayout({ children }: LayoutProps<"/learn">) {
  return (
    <div data-hide-chat-widget className="flex h-[100dvh] flex-none flex-col overflow-hidden">
      <SiteHeader />
      <div className="flex min-h-0 flex-1 flex-col">{children}</div>
    </div>
  );
}
