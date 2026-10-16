/**
 * Дадлагын REST API — `fetch("/api/products")`.
 *
 * Sandbox нь интернетгүй (CSP + opaque origin). API-тай ажиллах хичээлүүд
 * (Модул 5, 9, 14) нь бодит сервер шиг ажилладаг энэ санах ойн API-г
 * ашиглана: хоцролттой, алдааны код буцаадаг, AbortController-ийг хүндэлдэг.
 * Өгөгдөл нь ажиллуулалт бүрт шинээр эхэлнэ.
 *
 *     GET    /api/<цуглуулга>            жагсаалт (?q=, ?category=, ?_limit=)
 *     GET    /api/<цуглуулга>/<id>       нэг бичлэг, эсвэл 404
 *     POST   /api/<цуглуулга>            шинэ бичлэг, 201
 *     PUT    /api/<цуглуулга>/<id>       бүтнээр солих
 *     PATCH  /api/<цуглуулга>/<id>       хэсэгчлэн засах
 *     DELETE /api/<цуглуулга>/<id>       устгах
 *
 * Цуглуулгууд: products, courses, users, todos, posts, enrollments, orders.
 *
 * Бүх замд `?_delay=2000` (хоцролт, мс) болон `?_status=500` (алдаа) нэмж
 * ачаалах / алдааны төлвийг туршиж болно.
 */

type Item = Record<string, unknown> & { id: number };

export interface ApiRequest {
  method: string;
  path: string;
  body: unknown;
  /** Жижиг үсгээр: `{ "content-type": "application/json" }`. */
  headers: Record<string, string>;
}

function seed(): Record<string, Item[]> {
  return {
    products: [
      { id: 1, name: "Банана", price: 3500, category: "Жимс", emoji: "🍌", stock: 24 },
      { id: 2, name: "Алим", price: 2800, category: "Жимс", emoji: "🍎", stock: 40 },
      { id: 3, name: "Жүрж", price: 4200, category: "Жимс", emoji: "🍊", stock: 15 },
      { id: 4, name: "Лууван", price: 1900, category: "Ногоо", emoji: "🥕", stock: 30 },
      { id: 5, name: "Төмс", price: 1500, category: "Ногоо", emoji: "🥔", stock: 60 },
      { id: 6, name: "Брокколи", price: 5200, category: "Ногоо", emoji: "🥦", stock: 0 },
      { id: 7, name: "Сүү", price: 3200, category: "Сүүн бүтээгдэхүүн", emoji: "🥛", stock: 18 },
      { id: 8, name: "Бяслаг", price: 12500, category: "Сүүн бүтээгдэхүүн", emoji: "🧀", stock: 7 },
      { id: 9, name: "Талх", price: 2500, category: "Гурил", emoji: "🍞", stock: 12 },
      { id: 10, name: "Өндөг (10ш)", price: 6500, category: "Бусад", emoji: "🥚", stock: 20 },
    ],
    courses: [
      { id: 1, title: "HTML & CSS үндэс", level: "Анхан", lessons: 60, category: "Вэб" },
      { id: 2, title: "JavaScript үндэс", level: "Анхан", lessons: 90, category: "Вэб" },
      { id: 3, title: "React-ээр апп бүтээх", level: "Дунд", lessons: 80, category: "Вэб" },
      { id: 4, title: "Python програмчлал", level: "Анхан", lessons: 110, category: "Програмчлал" },
      { id: 5, title: "SQL өгөгдлийн сан", level: "Дунд", lessons: 50, category: "Өгөгдөл" },
    ],
    users: [
      { id: 1, name: "Бат", email: "bat@example.mn", city: "Улаанбаатар" },
      { id: 2, name: "Сараа", email: "saraa@example.mn", city: "Дархан" },
      { id: 3, name: "Тэмүүлэн", email: "temuulen@example.mn", city: "Эрдэнэт" },
      { id: 4, name: "Ану", email: "anu@example.mn", city: "Улаанбаатар" },
    ],
    todos: [
      { id: 1, title: "React хичээл үзэх", done: true },
      { id: 2, title: "useState дасгал хийх", done: false },
      { id: 3, title: "Төсөл эхлүүлэх", done: false },
    ],
    enrollments: [],
    orders: [],
    posts: [
      { id: 1, title: "Анхны component", body: "Өнөөдөр анхны component-оо бичлээ.", userId: 1 },
      {
        id: 2,
        title: "State гэж юу вэ",
        body: "State бол цаг хугацаанд өөрчлөгдөх өгөгдөл.",
        userId: 2,
      },
      { id: 3, title: "Effect-ийн цэвэрлэгээ", body: "Timer-ээ заавал цэвэрлэ!", userId: 1 },
    ],
  };
}

export class MockApi {
  private data = seed();
  private failures = new Map<string, number>();
  /** Хариу бүрийн хоцролт (мс). Тестэд богино, урьдчилан харахад бодит. */
  delay: number;
  readonly requests: ApiRequest[] = [];

  constructor(delay: number) {
    this.delay = delay;
  }

  /** Тестэд: цуглуулгын өгөгдлийг солих. */
  set(collection: string, items: Item[]): void {
    this.data[collection] = items.map((item) => ({ ...item }));
  }

  get(collection: string): Item[] {
    return (this.data[collection] ?? []).map((item) => ({ ...item }));
  }

  /** Тестэд: тухайн замын дараагийн хүсэлтүүд алдаа буцаана. */
  fail(path: string, status = 500): void {
    this.failures.set(path.replace(/\/$/, ""), status);
  }

  reset(): void {
    this.data = seed();
    this.failures.clear();
    this.requests.length = 0;
  }

  fetch = async (input: RequestInfo | URL, init: RequestInit = {}): Promise<Response> => {
    const raw = typeof input === "string" ? input : input instanceof URL ? input.href : input.url;
    const method = (init.method ?? (input instanceof Request ? input.method : "GET")).toUpperCase();
    const url = new URL(raw, "http://localhost");

    if (url.hostname !== "localhost" || !url.pathname.startsWith("/api/")) {
      throw new TypeError(
        `Failed to fetch — sandbox интернетгүй. Зөвхөн «/api/…» дадлагын API ажиллана (${raw}).`,
      );
    }

    let body: unknown = undefined;
    if (typeof init.body === "string") {
      try {
        body = JSON.parse(init.body);
      } catch {
        body = init.body;
      }
    }
    const path = url.pathname.replace(/\/$/, "");
    const headers: Record<string, string> = {};
    new Headers(init.headers ?? (input instanceof Request ? input.headers : undefined)).forEach(
      (value, key) => {
        headers[key] = value;
      },
    );
    this.requests.push({ method, path: path + url.search, body, headers });

    const delay = Number(url.searchParams.get("_delay") ?? this.delay);
    await wait(delay, init.signal ?? undefined);

    const forced = Number(url.searchParams.get("_status") ?? this.failures.get(path) ?? 0);
    if (forced >= 400) return json({ error: "Серверийн алдаа гарлаа" }, forced);

    return this.handle(method, path, url.searchParams, body);
  };

  private handle(method: string, path: string, params: URLSearchParams, body: unknown): Response {
    const [, , collection, idText] = path.split("/");
    const items = this.data[collection];
    if (!items) return json({ error: `«/api/${collection}» гэсэн зам байхгүй` }, 404);

    const id = idText === undefined ? undefined : Number(idText);
    const index = id === undefined ? -1 : items.findIndex((item) => item.id === id);
    const payload = body && typeof body === "object" ? (body as Record<string, unknown>) : {};

    if (id === undefined) {
      if (method === "GET") return json(filterList(items, params));
      if (method === "POST") {
        const created = { ...payload, id: Math.max(0, ...items.map((item) => item.id)) + 1 };
        items.push(created);
        return json(created, 201);
      }
      return json({ error: `${method} энэ зам дээр ажиллахгүй` }, 405);
    }

    if (index === -1) return json({ error: "Олдсонгүй" }, 404);
    if (method === "GET") return json(items[index]);
    if (method === "PUT") {
      items[index] = { ...payload, id: id! };
      return json(items[index]);
    }
    if (method === "PATCH") {
      items[index] = { ...items[index], ...payload, id: id! };
      return json(items[index]);
    }
    if (method === "DELETE") {
      const [removed] = items.splice(index, 1);
      return json(removed);
    }
    return json({ error: `${method} энэ зам дээр ажиллахгүй` }, 405);
  }
}

function filterList(items: Item[], params: URLSearchParams): Item[] {
  let result = items;
  const query = params.get("q")?.trim().toLowerCase();
  if (query) {
    result = result.filter((item) =>
      Object.values(item).some(
        (value) => typeof value === "string" && value.toLowerCase().includes(query),
      ),
    );
  }
  for (const [key, value] of params) {
    if (key === "q" || key.startsWith("_")) continue;
    result = result.filter((item) => String(item[key]) === value);
  }
  const limit = Number(params.get("_limit") ?? 0);
  return limit > 0 ? result.slice(0, limit) : result;
}

function json(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

function wait(ms: number, signal?: AbortSignal): Promise<void> {
  return new Promise((resolve, reject) => {
    const aborted = () => new DOMException("The operation was aborted.", "AbortError");
    // Аль хэдийн цуцлагдсан signal — хөтчийн fetch шиг шууд AbortError.
    if (signal?.aborted) return reject(aborted());
    const abort = () => {
      clearTimeout(timer);
      reject(aborted());
    };
    const timer = setTimeout(() => {
      signal?.removeEventListener("abort", abort);
      resolve();
    }, ms);
    signal?.addEventListener("abort", abort, { once: true });
  });
}
