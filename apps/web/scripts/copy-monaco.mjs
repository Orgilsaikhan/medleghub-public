/**
 * Monaco-ийн файлуудыг `public/monaco/vs` рүү хуулна.
 *
 * `@monaco-editor/react` нь анхдагчаар jsDelivr CDN-ээс татдаг. Бид өөрсдөө
 * хостолсноор:
 *   • Гуравдагч этгээдийн CDN рүү хэрэглэгчийн хүсэлт явахгүй (нууцлал),
 *   • Тухайн CDN унасан ч засварлагч ажиллана,
 *   • Хувилбар нь package-lock-оор тогтмол байна.
 */

import { cp, mkdir, rm, stat } from "node:fs/promises";
import path from "node:path";

// `monaco-editor` нь `exports` талбартай тул `require.resolve` ажиллахгүй —
// node_modules доторх байрлалыг шууд ашиглана.
const source = path.join(process.cwd(), "node_modules", "monaco-editor", "min", "vs");
const target = path.join(process.cwd(), "public", "monaco", "vs");

const exists = await stat(target).then(
  () => true,
  () => false,
);

// Аль хэдийн хуулсан бол алгасна — dev server дахин эхлэх бүрт удаашруулахгүй.
if (exists && !process.argv.includes("--force")) {
  console.log("monaco: already present, skipping");
} else {
  await rm(target, { recursive: true, force: true });
  await mkdir(path.dirname(target), { recursive: true });
  await cp(source, target, { recursive: true });
  console.log(`monaco: copied ${source} -> ${target}`);
}
