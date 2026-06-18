import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { BrainCircuit, ChartNoAxesColumnIncreasing, ShieldCheck, WandSparkles } from "lucide-react";

import ResumeUpload from "../components/ResumeUpload.jsx";
import { analyzeResume } from "../services/resumeService.js";

function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [toast, setToast] = useState(null);
  const navigate = useNavigate();

  const showToast = (message, type = "error") => {
    setToast({ message, type });
    window.setTimeout(() => setToast(null), 3600);
  };

  const handleAnalyze = async (file, jobDescription, validationError) => {
    if (validationError) {
      showToast(validationError);
      return;
    }

    if (!file) {
      showToast("Choose a PDF resume before analyzing.");
      return;
    }

    setIsLoading(true);
    try {
      const analysis = await analyzeResume(file,jobDescription);

      // Persist the latest analysis so a browser refresh on /result still has data.
      sessionStorage.setItem("resumeAnalysis", JSON.stringify(analysis));
      showToast("Analysis complete.", "success");
      navigate("/result", { state: { analysis } });
    } catch (error) {
      showToast(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main>
      {toast && <div className={`toast ${toast.type}`}>{toast.message}</div>}

      <section className="hero">
        <div className="hero-copy">
          
          <h1>AI Resume Analyzer</h1>
          <p>
            Upload a resume with a job description and receive a structured ATS score,
            selection probability, resume skills, matching job skills, missing keywords,
            and targeted suggestions.
          </p>
          <div className="hero-stats" aria-label="Application highlights">
            <span>
              <strong>0-100</strong>
              ATS score
            </span>
            <span>
              <strong>PDF</strong>
              text extraction
            </span>
            <span>
              <strong>JSON</strong>
              AI response
            </span>
          </div>
        </div>

        <ResumeUpload onAnalyze={handleAnalyze} isLoading={isLoading} />
      </section>

      <section id="features" className="features-grid" aria-label="Feature highlights">
        <article className="feature-card">
          <ChartNoAxesColumnIncreasing size={24} />
          <h3>Score visualization</h3>
          <p>Clear score cards make resume readiness easy to scan after each analysis.</p>
        </article>
        <article className="feature-card">
          <WandSparkles size={24} />
          <h3>Actionable edits</h3>
          <p>Suggestions focus on quantified impact, role alignment, and ATS keyword coverage.</p>
        </article>
        <article className="feature-card">
          <ShieldCheck size={24} />
          <h3>Typed API output</h3>
          <p>FastAPI validates OpenAI output before the frontend renders the result dashboard.</p>
        </article>
      </section>
    </main>
  );
}

export default Home;
