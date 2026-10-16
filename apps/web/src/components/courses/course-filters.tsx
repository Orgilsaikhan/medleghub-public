"use client";

import { LayoutGridIcon, SearchIcon, XIcon } from "lucide-react";
import { useRouter, useSearchParams } from "next/navigation";
import { type ReactNode, useEffect, useLayoutEffect, useRef, useState, useTransition } from "react";

import { CategoryLogo } from "@/components/courses/category-logo";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { categoryLabels, difficultyLabels, difficultyOrder, mn } from "@/lib/i18n/mn";
import type { Category } from "@/lib/types/api";
import { cn } from "@/lib/utils";

const ALL = "all";
const SEARCH_DEBOUNCE_MS = 350;
const PANEL_ID = "course-search-panel";

/** Хуудасны гарчиг — хайлтын товч `children`-ээр гарчгийн мөрийн баруун захад орно. */
export function CoursesHeading({ children }: { children?: ReactNode }) {
  return (
    <header>
      <div className="flex items-center justify-between gap-4">
        <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">{mn.courses.title}</h1>
        {children}
      </div>
      <p className="text-muted-foreground mt-2">{mn.courses.subtitle}</p>
    </header>
  );
}

/**
 * Гарчиг ба хайлт. Гарчгийн мөрийн баруун захын хайлтын товч дарахад доор
 * нь хайлт, ангилал, түвшний шүүлтүүр гулсаж нээгдэнэ. Шүүлтүүр идэвхтэй
 * ирсэн бол (`?q=`, `?category=`…) анхнаасаа нээлттэй.
 *
 * Шүүлтүүрийн төлөв нь URL дотор байрлана — хуваалцах, буцах товч, refresh
 * бүгд зөв ажиллана. Хайлт бичих бүрт биш, богино завсарлагааны дараа л
 * хүсэлт илгээнэ.
 *
 * `categories` — сургалттай ангиллууд (хоосон ангиллыг харуулахгүй).
 */
export function CourseFilters({ categories }: { categories: Category[] }) {
  const router = useRouter();
  const params = useSearchParams();
  const [isPending, startTransition] = useTransition();

  const queryParam = params.get("q") ?? "";
  const category = params.get("category") ?? ALL;
  const difficulty = params.get("difficulty") ?? ALL;
  const [search, setSearch] = useState(queryParam);
  const [syncedParam, setSyncedParam] = useState(queryParam);

  const activeCount = [queryParam, category !== ALL, difficulty !== ALL].filter(Boolean).length;
  const [open, setOpen] = useState(activeCount > 0);
  const toggleRef = useRef<HTMLButtonElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // URL гаднаас өөрчлөгдвөл (жишээ нь «цэвэрлэх», буцах товч) оролтыг тэгшитгэнэ.
  // Render-ийн үед төлөв засварлах нь React-ийн зөвлөсөн хэв маяг.
  if (queryParam !== syncedParam) {
    setSyncedParam(queryParam);
    setSearch(queryParam);
  }

  const apply = (next: Record<string, string | null>) => {
    const updated = new URLSearchParams(params.toString());
    for (const [key, value] of Object.entries(next)) {
      if (!value || value === ALL) updated.delete(key);
      else updated.set(key, value);
    }
    updated.delete("page"); // шүүлтүүр солигдвол эхний хуудас руу
    const search = updated.toString();
    startTransition(() => router.replace(search ? `/courses?${search}` : "/courses"));
  };

  useEffect(() => {
    if (search === queryParam) return;
    const timer = setTimeout(() => apply({ q: search.trim() || null }), SEARCH_DEBOUNCE_MS);
    return () => clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [search]);

  const toggle = () => {
    if (open) {
      setOpen(false);
      return;
    }
    setOpen(true);
    // `inert` арилсны дараа л фокуслах боломжтой.
    requestAnimationFrame(() => inputRef.current?.focus({ preventScroll: true }));
  };

  // URL-аар ирсэн ангилал жагсаалтад байхгүй бол ч (хоосон ангилал) сонгогдсон харагдана.
  const chips: string[] = [ALL, ...categories];
  if (category !== ALL && !chips.includes(category)) chips.push(category);

  const label = open ? mn.courses.searchClose : mn.courses.searchOpen;

  return (
    <div>
      <CoursesHeading>
        <button
          ref={toggleRef}
          type="button"
          aria-expanded={open}
          aria-controls={PANEL_ID}
          aria-label={
            activeCount > 0 ? `${label} (${mn.courses.activeFilters(activeCount)})` : label
          }
          title={label}
          onClick={toggle}
          className={cn(
            "relative grid size-11 shrink-0 place-items-center rounded-full border transition-[background-color,border-color,box-shadow,translate,scale,rotate] duration-300",
            "focus-visible:ring-ring focus-visible:ring-offset-background focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:outline-none",
            open
              ? "border-primary bg-primary text-primary-foreground shadow-primary/30 shadow-lg"
              : "bg-card hover:border-primary/50 hover:shadow-primary/15 hover:shadow-md motion-safe:hover:scale-105",
          )}
        >
          <SearchIcon
            aria-hidden
            className={cn(
              "absolute size-5 transition-[translate,scale,rotate,opacity] duration-300 motion-reduce:transition-none",
              open ? "scale-50 rotate-90 opacity-0" : "opacity-100",
            )}
          />
          <XIcon
            aria-hidden
            className={cn(
              "absolute size-5 transition-[translate,scale,rotate,opacity] duration-300 motion-reduce:transition-none",
              open ? "opacity-100" : "scale-50 -rotate-90 opacity-0",
            )}
          />
          {!open && activeCount > 0 && (
            <span
              aria-hidden
              className="bg-primary text-primary-foreground ring-background absolute -top-1 -right-1 grid size-5 place-items-center rounded-full text-[11px] font-bold ring-2"
            >
              {activeCount}
            </span>
          )}
        </button>
      </CoursesHeading>

      {/* grid-rows 0fr → 1fr: өндрөө мэдэхгүйгээр зөөлөн нээгдэнэ. Хаалттай үед `inert`. */}
      <div
        id={PANEL_ID}
        inert={!open}
        data-open={open || undefined}
        onKeyDown={(event) => {
          if (event.key !== "Escape") return;
          event.stopPropagation();
          setOpen(false);
          toggleRef.current?.focus();
        }}
        className="group/panel grid grid-rows-[0fr] opacity-0 transition-[grid-template-rows,opacity,margin-top] duration-500 ease-[cubic-bezier(0.2,0.8,0.2,1)] data-open:mt-6 data-open:grid-rows-[1fr] data-open:opacity-100 motion-reduce:transition-none"
      >
        <div className="min-h-0 overflow-hidden">
          <div className="bg-card/70 relative isolate -translate-y-3 space-y-6 overflow-hidden rounded-2xl border p-4 transition-transform duration-500 ease-[cubic-bezier(0.2,0.8,0.2,1)] group-data-open/panel:translate-y-0 motion-reduce:transition-none sm:p-6">
            <span
              aria-hidden
              className="bg-primary/10 pointer-events-none absolute -top-24 -right-24 -z-10 size-72 rounded-full blur-3xl"
            />

            <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
              <Label htmlFor="course-search" className="sr-only">
                {mn.courses.searchLabel}
              </Label>
              <div className="relative flex-1">
                <SearchIcon
                  aria-hidden
                  className="text-muted-foreground pointer-events-none absolute top-1/2 left-4 size-5 -translate-y-1/2"
                />
                <Input
                  ref={inputRef}
                  id="course-search"
                  type="search"
                  value={search}
                  onChange={(event) => setSearch(event.target.value)}
                  placeholder={mn.courses.searchPlaceholder}
                  className="h-12 rounded-xl pl-12 text-base"
                  data-pending={isPending ? "" : undefined}
                />
              </div>
              {activeCount > 0 && (
                <Button
                  variant="ghost"
                  onClick={() => apply({ q: null, category: null, difficulty: null })}
                  className="shrink-0 self-start sm:self-auto"
                >
                  <XIcon className="size-4" />
                  {mn.courses.clearFilters}
                </Button>
              )}
            </div>

            <FilterGroup id="filter-category" label={mn.courseDetail.category}>
              <div role="group" aria-labelledby="filter-category" className="flex flex-wrap gap-2">
                {chips.map((value, index) => (
                  <Appear key={value} open={open} index={index}>
                    <CategoryChip
                      value={value}
                      selected={category === value}
                      onSelect={() => apply({ category: value })}
                    />
                  </Appear>
                ))}
              </div>
            </FilterGroup>

            <FilterGroup id="filter-difficulty" label={mn.courseDetail.difficulty}>
              <Appear open={open} index={chips.length}>
                <SegmentedControl
                  labelledBy="filter-difficulty"
                  value={difficulty}
                  onChange={(value) => apply({ difficulty: value })}
                  options={[
                    { value: ALL, label: mn.courses.allDifficulties },
                    ...difficultyOrder.map((value) => ({
                      value,
                      label: difficultyLabels[value],
                    })),
                  ]}
                />
              </Appear>
            </FilterGroup>
          </div>
        </div>
      </div>
    </div>
  );
}

function FilterGroup({ id, label, children }: { id: string; label: string; children: ReactNode }) {
  return (
    <div className="space-y-2.5">
      <p id={id} className="text-muted-foreground text-xs font-semibold tracking-wider uppercase">
        {label}
      </p>
      {children}
    </div>
  );
}

/**
 * Панел нээгдэхэд доороос дараалан орж ирнэ. Хөдөлгөөний хоцрогдол зөвхөн
 * энд — товчны өнгө сонгоход шууд солигдоно.
 */
function Appear({ open, index, children }: { open: boolean; index: number; children: ReactNode }) {
  return (
    <div
      style={{ transitionDelay: open ? `${120 + index * 35}ms` : "0ms" }}
      className="translate-y-2 opacity-0 transition-[opacity,translate,scale,rotate] duration-300 ease-out group-data-open/panel:translate-y-0 group-data-open/panel:opacity-100 motion-reduce:transition-none"
    >
      {children}
    </div>
  );
}

function CategoryChip({
  value,
  selected,
  onSelect,
}: {
  value: string;
  selected: boolean;
  onSelect: () => void;
}) {
  const isAll = value === ALL;
  return (
    <button
      type="button"
      aria-pressed={selected}
      onClick={onSelect}
      className={cn(
        "group/chip inline-flex h-10 items-center gap-2 rounded-full border px-4 text-sm font-medium transition-[background-color,border-color,color,box-shadow,translate,scale,rotate] duration-200",
        "focus-visible:ring-ring focus-visible:ring-offset-background focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:outline-none",
        selected
          ? "border-primary bg-primary text-primary-foreground shadow-primary/25 shadow-md"
          : "bg-background/60 hover:border-primary/50 hover:bg-accent motion-safe:hover:-translate-y-0.5",
      )}
    >
      {isAll ? (
        <LayoutGridIcon className="size-4" aria-hidden />
      ) : (
        <CategoryLogo
          category={value as Category}
          className="size-5 transition-transform duration-300 motion-safe:group-hover/chip:scale-110 motion-safe:group-hover/chip:-rotate-6"
        />
      )}
      {isAll ? mn.courses.allCategories : categoryLabels[value as Category]}
    </button>
  );
}

/**
 * Нэгийг сонгох товчнууд — сонгосон товчны шар дэвсгэр шинэ сонголт руу
 * гулсана. Байрлалыг CSS хувьсагчаар (`--seg-*`) тавина; эхний удаа
 * transition-гүй (`data-ready`), эс бөгөөс буланаас «нисэж» ирнэ.
 */
function SegmentedControl({
  labelledBy,
  value,
  options,
  onChange,
}: {
  labelledBy: string;
  value: string;
  options: { value: string; label: string }[];
  onChange: (value: string) => void;
}) {
  const listRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    const list = listRef.current;
    if (!list) return;
    const place = () => {
      const active = list.querySelector<HTMLElement>(`[data-value="${value}"]`);
      if (!active) return;
      list.style.setProperty("--seg-x", `${active.offsetLeft}px`);
      list.style.setProperty("--seg-y", `${active.offsetTop}px`);
      list.style.setProperty("--seg-w", `${active.offsetWidth}px`);
      list.style.setProperty("--seg-h", `${active.offsetHeight}px`);
    };
    place();
    const frame = requestAnimationFrame(() => {
      list.dataset.ready = "";
    });
    const observer = new ResizeObserver(place);
    observer.observe(list);
    return () => {
      cancelAnimationFrame(frame);
      observer.disconnect();
    };
  }, [value]);

  return (
    <div
      ref={listRef}
      role="group"
      aria-labelledby={labelledBy}
      className="group/seg bg-background/60 relative grid grid-cols-2 gap-1 rounded-2xl border p-1 sm:inline-flex sm:rounded-full"
    >
      <span
        aria-hidden
        style={{
          left: "var(--seg-x)",
          top: "var(--seg-y)",
          width: "var(--seg-w)",
          height: "var(--seg-h)",
        }}
        className="bg-primary shadow-primary/25 pointer-events-none absolute rounded-xl shadow-md motion-safe:group-data-[ready]/seg:transition-[left,top,width,height] motion-safe:group-data-[ready]/seg:duration-300 motion-safe:group-data-[ready]/seg:ease-[cubic-bezier(0.2,0.8,0.2,1)] sm:rounded-full"
      />
      {options.map((option) => {
        const selected = option.value === value;
        return (
          <button
            key={option.value}
            type="button"
            data-value={option.value}
            aria-pressed={selected}
            onClick={() => onChange(option.value)}
            className={cn(
              "relative z-10 h-9 rounded-xl px-4 text-sm font-medium whitespace-nowrap transition-colors duration-200 sm:rounded-full",
              "focus-visible:ring-ring focus-visible:ring-2 focus-visible:outline-none",
              selected ? "text-primary-foreground" : "text-muted-foreground hover:text-foreground",
            )}
          >
            {option.label}
          </button>
        );
      })}
    </div>
  );
}
