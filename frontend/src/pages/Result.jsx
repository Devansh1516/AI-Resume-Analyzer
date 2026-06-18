import { ArrowLeft, FileText } from "lucide-react";
import { Link, Navigate, useLocation } from "react-router-dom";

import KeywordCard from "../components/KeywordCard.jsx";
import ScoreCard from "../components/ScoreCard.jsx";
import SkillsCard from "../components/SkillsCard.jsx";
import SuggestionsCard from "../components/SuggestionsCard.jsx";

function Result() {
  const location = useLocation();
  const storedAnalysis = sessionStorage.getItem("resumeAnalysis");
  const analysis = location.state?.analysis || (storedAnalysis ? JSON.parse(storedAnalysis) : null);

  if (!analysis) {
    return <Navigate to="/" replace />;
  }

  return (
    <main className="result-page">
      <div className="result-header">
        <Link className="back-link" to="/">
          <ArrowLeft size={18} />
          Analyze another resume
        </Link>
        <div>
          <span className="section-kicker">
            <FileText size={16} />
            Resume report
          </span>
          <h1>Job Match Result</h1>
          <p>{analysis.summary}</p>
        </div>
      </div>

      <section className="result-grid">
        <ScoreCard
          score={analysis.ats_score ?? analysis.match_percentage}
          title="ATS Score"
          description="ATS score for this resume against the pasted job description."
        />
        <ScoreCard
          score={analysis.selection_probability}
          title="Selection Probability"
          description="Estimated chance this resume passes ATS screening for this role."
          variant="probability"
        />
        <SkillsCard
          resumeSkills={analysis.resume_skills ?? []}
          matchedSkills={analysis.matched_skills ?? analysis.skills ?? []}
          title="Skills Found"
        />
        <KeywordCard keywords={analysis.missing_keywords} />
        <SuggestionsCard suggestions={analysis.suggestions} />
      </section>

      <section className="summary-panel">
        <h2>Resume Summary</h2>
        <p>{analysis.summary}</p>
      </section>
    </main>
  );
}

export default Result;
