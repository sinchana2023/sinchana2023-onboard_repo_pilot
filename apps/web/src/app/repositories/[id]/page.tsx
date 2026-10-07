"use client";

import Link from "next/link";
import {
  FormEvent,
  use,
  useEffect,
  useState,
} from "react";

import {
  askRepository,
  AskResponse,
  getRepository,
  RepositoryDetail,
} from "@/lib/api";

interface RepositoryPageProps {
  params: Promise<{
    id: string;
  }>;
}

export default function RepositoryPage({
  params,
}: RepositoryPageProps) {
  const { id } = use(params);
  const repositoryId = Number(id);

  const [repository, setRepository] =
    useState<RepositoryDetail | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] =
    useState<AskResponse | null>(null);
  const [asking, setAsking] = useState(false);
  const [askError, setAskError] = useState("");

  useEffect(() => {
    async function loadRepository() {
      if (!Number.isInteger(repositoryId)) {
        setError("Invalid repository ID.");
        setLoading(false);
        return;
      }

      try {
        const result = await getRepository(
          repositoryId
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
  }, [repositoryId]);

  async function handleAsk(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    if (!question.trim()) {
      return;
    }

    setAskError("");
    setAnswer(null);
    setAsking(true);

    try {
      const result = await askRepository(
        repositoryId,
        question.trim(),
        5
      );

      setAnswer(result);
    } catch (err) {
      setAskError(
        err instanceof Error
          ? err.message
          : "Failed to get an answer."
      );
    } finally {
      setAsking(false);
    }
  }

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

            <Link
              href="/"
              className="mt-5 inline-block text-sm text-blue-400 transition hover:text-blue-300"
            >
              ← Return to homepage
            </Link>
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

          <Link
            href="/"
            className="text-sm text-slate-400 transition hover:text-white"
          >
            ← Analyze another repository
          </Link>
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
                {repository.owner} / {repository.name}
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
              className="mt-2 block break-all text-blue-400 transition hover:text-blue-300"
            >
              {repository.github_url}
            </a>
          </div>

          <div className="mt-8 rounded-2xl border border-blue-900 bg-slate-900 p-6">
            <div className="mb-5">
              <p className="text-lg font-semibold">
                Ask OnboardAI
              </p>

              <p className="mt-2 text-sm text-slate-400">
                Ask questions about the architecture,
                implementation, and behavior of this
                repository.
              </p>
            </div>

            <form onSubmit={handleAsk}>
              <label
                htmlFor="repository-question"
                className="sr-only"
              >
                Repository question
              </label>

              <textarea
                id="repository-question"
                value={question}
                onChange={(event) =>
                  setQuestion(event.target.value)
                }
                placeholder="Where is authentication implemented?"
                rows={4}
                className="w-full resize-none rounded-xl border border-slate-700 bg-slate-950 p-4 text-sm text-white outline-none transition focus:border-blue-500"
              />

              <div className="mt-3 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <p className="text-xs text-slate-500">
                  Answers are grounded in indexed repository
                  content.
                </p>

                <button
                  type="submit"
                  disabled={
                    asking || !question.trim()
                  }
                  className="rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-semibold transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {asking ? "Thinking..." : "Ask"}
                </button>
              </div>
            </form>

            {askError && (
              <div className="mt-5 rounded-xl border border-red-900 bg-red-950/30 p-4 text-sm text-red-300">
                {askError}
              </div>
            )}
          </div>

          {answer && (
            <div className="mt-6 space-y-6">
              <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
                <p className="text-sm font-medium text-slate-400">
                  OnboardAI
                </p>

                <div className="mt-3 whitespace-pre-wrap text-sm leading-7 text-slate-200">
                  {answer.answer}
                </div>
              </div>

              {answer.sources.length > 0 && (
                <div>
                  <p className="text-sm font-semibold text-white">
                    Sources
                  </p>

                  <div className="mt-3 space-y-3">
                    {answer.sources.map(
                      (source, index) => (
                        <div
                          key={`${source.path}-${source.start_line}-${index}`}
                          className="rounded-xl border border-slate-800 bg-slate-900 p-4"
                        >
                          <div className="flex items-center justify-between gap-4">
                            <p className="truncate text-sm font-medium text-blue-400">
                              {source.path}
                            </p>

                            <span className="shrink-0 text-xs text-slate-500">
                              {source.score.toFixed(2)}
                            </span>
                          </div>

                          <p className="mt-1 text-xs text-slate-500">
                            Lines {source.start_line}–
                            {source.end_line}
                          </p>
                        </div>
                      )
                    )}
                  </div>
                </div>
              )}
            </div>
          )}
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