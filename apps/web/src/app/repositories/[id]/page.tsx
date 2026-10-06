"use client";

import { useEffect, useState } from "react";
import { getRepository, RepositoryDetail } from "@/lib/api";

interface RepositoryPageProps {
  params: Promise<{
    id: string;
  }>;
}

export default function RepositoryPage({
  params,
}: RepositoryPageProps) {
  const [repository, setRepository] =
    useState<RepositoryDetail | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadRepository() {
      try {
        const { id } = await params;

        const result = await getRepository(
          Number(id)
        );

        setRepository(result);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load repository."
        );
      } finally {
        setLoading(false);
      }
    }

    loadRepository();
  }, [params]);

  if (loading) {
    return (
      <main className="min-h-screen bg-slate-950 text-white">
        <div className="mx-auto max-w-6xl px-6 py-16">
          <p className="text-slate-400">
            Loading repository...
          </p>
        </div>
      </main>
    );
  }

  if (error || !repository) {
    return (
      <main className="min-h-screen bg-slate-950 text-white">
        <div className="mx-auto max-w-6xl px-6 py-16">
          <div className="rounded-2xl border border-red-900 bg-red-950/30 p-6">
            <h1 className="text-xl font-semibold">
              Unable to load repository
            </h1>

            <p className="mt-2 text-sm text-red-300">
              {error || "Repository not found."}
            </p>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="mx-auto max-w-6xl px-6 py-8">
        <header className="flex items-center justify-between">
          <div className="text-xl font-semibold">
            OnboardAI
          </div>

          <a
            href="/"
            className="text-sm text-slate-400 transition hover:text-white"
          >
            ← Analyze another repository
          </a>
        </header>

        <section className="mt-12">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <p className="text-sm text-blue-400">
                Repository Workspace
              </p>

              <h1 className="mt-2 text-4xl font-bold">
                {repository.name}
              </h1>

              <p className="mt-2 text-slate-400">
                {repository.owner} /{" "}
                {repository.name}
              </p>
            </div>

            <span className="rounded-full bg-emerald-900/50 px-4 py-2 text-sm text-emerald-300">
              ● {repository.status}
            </span>
          </div>

          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <StatCard
              label="Language"
              value={
                repository.primary_language ??
                "Unknown"
              }
            />

            <StatCard
              label="Repository Files"
              value={repository.file_count.toString()}
            />

            <StatCard
              label="Indexed Files"
              value={repository.source_file_count.toString()}
            />

            <StatCard
              label="Code Chunks"
              value={repository.chunk_count.toString()}
            />
          </div>

          <div className="mt-8 rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <p className="text-sm text-slate-400">
              GitHub repository
            </p>

            <a
              href={repository.github_url}
              target="_blank"
              rel="noreferrer"
              className="mt-2 block break-all text-blue-400 hover:text-blue-300"
            >
              {repository.github_url}
            </a>
          </div>

          <div className="mt-8 grid gap-4 md:grid-cols-2">
            <button
              className="rounded-2xl border border-blue-800 bg-blue-950/30 p-6 text-left transition hover:border-blue-500"
            >
              <p className="text-lg font-semibold">
                Ask OnboardAI
              </p>

              <p className="mt-2 text-sm text-slate-400">
                Ask questions about the architecture,
                code, and implementation.
              </p>
            </button>

            <button
              className="rounded-2xl border border-slate-800 bg-slate-900 p-6 text-left transition hover:border-slate-600"
            >
              <p className="text-lg font-semibold">
                Search Code
              </p>

              <p className="mt-2 text-sm text-slate-400">
                Search the repository using semantic
                retrieval.
              </p>
            </button>
          </div>
        </section>
      </div>
    </main>
  );
}

function StatCard({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
      <p className="text-sm text-slate-400">
        {label}
      </p>

      <p className="mt-2 text-2xl font-semibold">
        {value}
      </p>
    </div>
  );
}
