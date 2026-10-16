import { loader } from "@monaco-editor/react";

/**
 * Monaco-г өөрийн домэйнээс ачаална.
 *
 * Анхдагчаар `@monaco-editor/react` нь jsDelivr CDN-ээс татдаг. Файлуудыг
 * `scripts/copy-monaco.mjs` нь `public/monaco/vs` рүү хуулсан байна.
 */
let configured = false;

export function configureMonaco(): void {
  if (configured) return;
  configured = true;
  loader.config({
    paths: { vs: "/monaco/vs" },
    // Засварлагчийн интерфейс монгол хэлээр байхгүй тул англиар үлдээв —
    // хөгжүүлэгчид танил нэр томъёо (Find, Replace, …) хэвээр байна.
    "vs/nls": { availableLanguages: {} },
  });
}
