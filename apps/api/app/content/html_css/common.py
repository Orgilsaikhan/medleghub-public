"""HTML & CSS хичээлийн олон файлтай код.

`initial_code` нь React сургалтын адил `// @file <нэр>` мөрөөр файлуудад
хуваагдана (`apps/web/src/lib/sandbox/react/files.ts`). Тэмдэггүй код нь
бүхэлдээ ганц файл: HTML хичээлд `index.html`, CSS хичээлд `style.css`.

Засварлагч файл бүрийг tab-аар харуулж, «Хөтөч» нь `index.html`-ийг (эсвэл
эхний `.html` файлыг) харуулна. `<link rel="stylesheet" href="style.css">`
нь хичээлийн `style.css`-ийг холбоно — жинхэнэ сайт шиг, холбоогүй бол CSS
нөлөөлөхгүй.

CSS хичээл бүр `css_page()`-ээр `index.html` + `style.css` болно: сурагч
загвараа бичихэд түүнд хэрэглэгдэх HTML бэлэн байна.
"""

import re

MARKER = re.compile(r"^// @file (\S+)( locked)?\s*$")


def files(*entries: tuple[str, str]) -> str:
    """`("index.html", код), ("style.css", код)` → нэг `initial_code` мөр."""
    return "".join(f"// @file {name}\n{code.strip()}\n" for name, code in entries)


def css_page(*, title: str, body: str, css: str) -> str:
    """CSS хичээл: `style.css`-ийг холбосон `index.html` ба `style.css`.

    `body` — `<body>` доторх HTML, доголгүйгээр бичнэ (энд 4 зайгаар
    доголно). Зөвхөн Модул 0-6-д заасан элементүүдийг ашиглана.
    """
    indented = "\n".join(f"    {line}" if line.strip() else "" for line in body.strip().split("\n"))
    html = f"""\
<!DOCTYPE html>
<html lang="mn">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <link rel="stylesheet" href="style.css" />
  </head>

  <body>
{indented}
  </body>
</html>
"""
    return files(("index.html", html), ("style.css", css))


def parse_files(source: str, default: str) -> list[tuple[str, str]]:
    """`initial_code` → `[(нэр, код)]`. Тэмдэггүй бол `[(default, source)]`."""
    parsed: list[tuple[str, str]] = []
    name: str | None = None
    lines: list[str] = []
    for line in source.split("\n"):
        match = MARKER.match(line)
        if match:
            if name is not None:
                parsed.append((name, "\n".join(lines)))
            name, lines = match[1], []
        else:
            lines.append(line)
    if name is not None:
        parsed.append((name, "\n".join(lines)))
    return parsed or [(default, source)]
