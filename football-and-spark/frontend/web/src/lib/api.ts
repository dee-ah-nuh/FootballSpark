const BASE = process.env.NEXT_PUBLIC_API_BASE!;

export type League = { id: number; league_name: string; country_name?: string | null };
export type LeagueResponse = { total: number; items: League[] };

export async function getLeagues(params?: {
  q?: string;
  country?: string;
  limit?: number;
  offset?: number;
  sort?: string;
}): Promise<LeagueResponse> {
  const url = new URL("/leagues", BASE);
  if (params?.q) url.searchParams.set("q", params.q);
  if (params?.country) url.searchParams.set("country", params.country);
  if (params?.limit) url.searchParams.set("limit", String(params.limit));
  if (params?.offset) url.searchParams.set("offset", String(params.offset));
  if (params?.sort) url.searchParams.set("sort", params.sort);
  const res = await fetch(url.toString(), { cache: "no-store" });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getLeagueById(id: number): Promise<League> {
  const res = await fetch(`${BASE}/leagues/${id}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Not found");
  return res.json();
}

export async function getCountries(): Promise<string[]> {
  const res = await fetch(`${BASE}/leagues/countries`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load countries");
  return res.json();
}
