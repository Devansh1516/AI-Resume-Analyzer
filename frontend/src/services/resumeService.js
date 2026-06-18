const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "hhttps://ai-resume-analyzer-backend-40ue.onrender.com";

export async function analyzeResume(
  file,
  jobDescription
) {
  const formData = new FormData();

  formData.append("file", file);

  formData.append(
    "job_description",
    jobDescription
  );

  const response = await fetch(
    `${API_BASE_URL}/api/resume/analyze`,
    {
      method: "POST",
      body: formData,
    }
  );

  const payload = await response
    .json()
    .catch(() => ({}));

  if (!response.ok) {
    throw new Error(
      payload.detail ||
        "Resume analysis failed. Please try again."
    );
  }

  return payload;
}
