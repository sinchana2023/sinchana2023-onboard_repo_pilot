const API_URL =
  process.env.NEXT_PUBLIC_API_URL ??
  "http://localhost:8000";

export interface RepositoryCreateResponse {
  id: number;
  name: string;
  github_url: string;
  owner: string;
  default_branch: string | null;
  primary_language: string | null;
  status: string;
  created_at: string;
}

export async function createRepository(
  githubUrl: string
): Promise<RepositoryCreateResponse> {
  const response = await fetch(
    `${API_URL}/api/v1/repositories`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({
        github_url: githubUrl,
      }),
    }
  );

  if (!response.ok) {
    let message = "Failed to ingest repository.";

    try {
      const data = await response.json();

      if (typeof data?.detail === "string") {
        message = data.detail;
      }
    } catch {
      // Keep the default message if the response is not JSON.
    }

    throw new Error(message);
  }

  return response.json();
}
export interface RepositoryDetail {
  id: number;
  name: string;
  github_url: string;
  owner: string;
  default_branch: string | null;
  primary_language: string | null;
  status: string;
  file_count: number;
  source_file_count: number;
  chunk_count: number;
  created_at: string;
}
export async function getRepository(
  repositoryId: number
): Promise<RepositoryDetail> {
  const response = await fetch(
    `${API_URL}/api/v1/repositories/${repositoryId}`
  );

  if (!response.ok) {
    let message = "Failed to load repository.";

    try {
      const data = await response.json();

      if (typeof data?.detail === "string") {
        message = data.detail;
      }
    } catch {
      // Keep default error message.
    }

    throw new Error(message);
  }

  return response.json();
}
export interface AskSource {
  path: string;
  start_line: number;
  end_line: number;
  score: number;
}

export interface AskResponse {
  answer: string;
  sources: AskSource[];
}

export async function askRepository(
  repositoryId: number,
  question: string,
  topK = 5
): Promise<AskResponse> {
  const response = await fetch(
    `${API_URL}/api/v1/repositories/${repositoryId}/ask`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({
        question,
        top_k: topK,
      }),
    }
  );

  if (!response.ok) {
    let message = "Failed to ask about this repository.";

    try {
      const data = await response.json();

      if (typeof data?.detail === "string") {
        message = data.detail;
      }
    } catch {
      // Keep the default message.
    }

    throw new Error(message);
  }

  return response.json();
}