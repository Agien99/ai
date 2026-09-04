import apiConfig from "../config/api";

async function apiRequest(
  path,
  options = {}
) {
  const response = await fetch(
    `${apiConfig.baseUrl}${path}`,
    {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    }
  );

  const data = await response.json();

  if (!response.ok) {
    const message =
      data?.message ||
      data?.detail ||
      "API request failed.";

    throw new Error(
      typeof message === "string"
        ? message
        : "API request failed."
    );
  }

  return data;
}

export async function createSession() {
  return apiRequest(
    "/sessions",
    {
      method: "POST",
    }
  );
}

export async function submitInitialSpins(
  sessionId,
  spins
) {
  return apiRequest(
    `/sessions/${sessionId}/initial-spins`,
    {
      method: "POST",
      body: JSON.stringify({
        spins,
      }),
    }
  );
}

export async function addSessionSpin(
  sessionId,
  number
) {
  return apiRequest(
    `/sessions/${sessionId}/spins`,
    {
      method: "POST",
      body: JSON.stringify({
        number,
      }),
    }
  );
}

export async function getSessionSpins(
  sessionId
) {
  return apiRequest(
    `/sessions/${sessionId}/spins`
  );
}