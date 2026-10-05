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
