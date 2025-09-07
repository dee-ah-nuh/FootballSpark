"use client";

import { useEffect, useMemo, useState } from "react";
import { getLeagues, getCountries } from "@/lib/api";
// import { Input } from "@/components/ui/input";
import { Input } from "@/components/ui/input"; // Update this path to the correct location of your Input component
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { ChevronLeft, ChevronRight, RefreshCcw } from "lucide-react";

const PAGE_SIZE = 20;

export default function LeaguesPage() {
  const [q, setQ] = useState("");
  const [country, setCountry] = useState<string>("");
  const [countries, setCountries] = useState<string[]>([]);
  const [page, setPage] = useState(1);
  const [sort, setSort] = useState("league_name.asc");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<{ total: number; items: any[] } | null>(null);

  const offset = useMemo(() => (page - 1) * PAGE_SIZE, [page]);

  // load country list once
  useEffect(() => {
    getCountries().then(setCountries).catch(() => setCountries([]));
  }, []);

  // load leagues whenever filters change
  useEffect(() => {
    const t = setTimeout(async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await getLeagues({
          q,
          country: country || undefined,
          limit: PAGE_SIZE,
          offset,
          sort,
        });
        setData(res);
      } catch (e: any) {
        setError(e?.message ?? "Failed to load");
      } finally {
        setLoading(false);
      }
    }, 250);
    return () => clearTimeout(t);
  }, [q, country, offset, sort]);

  const total = data?.total ?? 0;
  const maxPage = Math.max(1, Math.ceil(total / PAGE_SIZE));

  return (
    <section className="space-y-4">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-2xl font-semibold">Leagues</h1>
        <div className="flex items-center gap-2">
          <Input
            placeholder="Search leagues or countries…"
            value={q}
            onChange={(e) => {
              setPage(1);
              setQ(e.target.value);
            }}
            className="w-64"
          />

          <select
            className="h-9 rounded-md border px-2 text-sm"
            value={country}
            onChange={(e) => {
              setCountry(e.target.value);
              setPage(1);
            }}
          >
            <option value="">All countries</option>
            {countries.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>

          <select
            className="h-9 rounded-md border px-2 text-sm"
            value={sort}
            onChange={(e) => {
              setSort(e.target.value);
              setPage(1);
            }}
          >
            <option value="league_name.asc">League ↑</option>
            <option value="league_name.desc">League ↓</option>
            <option value="country_name.asc">Country ↑</option>
            <option value="country_name.desc">Country ↓</option>
          </select>

          <Button
            variant="ghost"
            size="icon"
            onClick={() => {
              setQ("");
              setCountry("");
              setSort("league_name.asc");
              setPage(1);
            }}
          >
            <RefreshCcw className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {loading ? (
        <ListSkeleton />
      ) : error ? (
        <div className="rounded-md border p-6 text-sm text-red-600">{error}</div>
      ) : data && data.items.length ? (
        <ul className="grid grid-cols-1 gap-2 sm:grid-cols-2">
          {data.items.map((l) => (
            <li
              key={l.id}
              className="rounded-lg border bg-white p-4 shadow-sm transition hover:shadow"
            >
              <div className="font-medium">{l.league_name}</div>
              <div className="text-sm text-muted-foreground">
                {l.country_name ?? ""}
              </div>
              {/* you can expand details right here if needed */}
            </li>
          ))}
        </ul>
      ) : (
        <div className="rounded-md border p-8 text-center text-sm text-muted-foreground">
          No matches found.
        </div>
      )}

      <div className="flex items-center gap-2">
        <Button
          variant="outline"
          size="icon"
          onClick={() => setPage((p) => Math.max(1, p - 1))}
          disabled={page <= 1}
        >
          <ChevronLeft className="h-4 w-4" />
        </Button>
        <span className="px-2 text-sm">
          {page} / {maxPage}
        </span>
        <Button
          variant="outline"
          size="icon"
          onClick={() => setPage((p) => Math.min(maxPage, p + 1))}
          disabled={page >= maxPage}
        >
          <ChevronRight className="h-4 w-4" />
        </Button>
        <span className="ml-auto text-xs text-muted-foreground">
          Total: {total}
        </span>
      </div>
    </section>
  );
}

function ListSkeleton() {
  return (
    <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
      {Array.from({ length: 8 }).map((_, i) => (
        <div key={i} className="rounded-lg border p-4">
          <Skeleton className="h-5 w-2/3" />
          <Skeleton className="mt-2 h-4 w-1/3" />
        </div>
      ))}
    </div>
  );
}
