const configuredBaseUrl =
  import.meta.env
    .VITE_API_BASE_URL
    ?.trim();

const developmentBaseUrl =
  "http://localhost:8000";

const API_BASE_URL =
  configuredBaseUrl ||
  (
    import.meta.env.DEV
      ? developmentBaseUrl
      : ""
  );

export const apiConfig = {
  baseUrl:
    API_BASE_URL.replace(
      /\/$/,
      ""
    ),

  configured:
    Boolean(
      API_BASE_URL
    ),

  environment:
    import.meta.env.MODE,
};

export default apiConfig;