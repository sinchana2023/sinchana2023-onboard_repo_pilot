"use client";

import { FormEvent, useState } from "react";

import {
  createRepository,
  RepositoryCreateResponse,
} from "@/lib/api";

export default function Home() {
  const [githubUrl, setGithubUrl] = useState("");
  const [repository, setRepository] =
    useState<RepositoryCreateResponse | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    setError("");
    setRepository(null);

    if (!githubUrl.trim()) {
      setError("Enter a GitHub repository URL.");
      return;
    }

    setLoading(true);

    try {
      const result = await createRepository(
        githubUrl.trim()
      );

      setRepository(result);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="mx-auto flex min-h-screen max-w-5xl flex-col px-6 py-8">
        <header className="flex items-center justify-between">
          <div className="text-xl font-semibold">
            OnboardAI
          </div>

          <div className="text-sm text-slate-400">
            AI Codebase Intelligence
          </div>
        </header>

        <section className="flex flex-1 items-center justify-center">
          <div className="w-full max-w-3xl">
            <div className="mb-8 text-center">
              <p className="mb-3 text-sm font-medium uppercase tracking-[0.2em] text-blue-400">
                Repository Intelligence
              </p>

              <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">
                Understand any codebase faster.
              </h1>

              <p className="mx-auto mt-5 max-w-2xl text-base leading-7 text-slate-400 sm:text-lg">
                Connect a GitHub repository and ask
                questions about its architecture, code,
                and implementation.
              </p>
            </div>

            <form
              onSubmit={handleSubmit}
              className="rounded-2xl border border-slate-800 bg-slate-900 p-4 shadow-2xl"
            >
              <label
                htmlFor="github-url"
                className="mb-2 block text-sm font-medium text-slate-300"
              >
                GitHub repository
              </label>

              <div className="flex flex-col gap-3 sm:flex-row">
                <input
                  id="github-url"
                  type="url"
                  value={githubUrl}
                  onChange={(event) =>
                    setGithubUrl(event.target.value)
                  }
                  placeholder="https://github.com/owner/repository"
                  className="min-w-0 flex-1 rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm outline-none transition focus:border-blue-500"
                />

                <button
                  type="submit"
                  disabled={loading}
                  className="rounded-xl bg-blue-600 px-6 py-3 text-sm font-semibold transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {loading
                    ? "Analyzing..."
                    : "Analyze Repository"}
                </button>
              </div>

              {error && (
                <div className="mt-4 rounded-xl border border-red-900 bg-red-950/40 px-4 py-3 text-sm text-red-300">
                  {error}
                </div>
              )}
            </form>

            {repository && (
              <div className="mt-6 rounded-2xl border border-emerald-900 bg-emerald-950/30 p-6">
                <div className="mb-4 flex items-center justify-between">
                  <div>
                    <p className="text-sm text-slate-400">
                      Repository ready
                    </p>

                    <h2 className="mt-1 text-2xl font-semibold">
                      {repository.name}
                    </h2>
                  </div>

                  <span className="rounded-full bg-emerald-900/60 px-3 py-1 text-xs font-medium text-emerald-300">
                    {repository.status}
                  </span>
                </div>

                <p className="text-sm text-slate-400">
                  {repository.owner}
                </p>

                <p className="mt-4 break-all text-sm text-slate-300">
                  {repository.github_url}
                </p>
              </div>
            )}
          </div>
        </section>

        <footer className="py-6 text-center text-xs text-slate-500">
          Semantic search • Grounded RAG • Source citations
        </footer>
      </div>
    </main>
  );
}