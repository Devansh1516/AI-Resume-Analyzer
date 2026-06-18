import { Gauge, Target } from "lucide-react";

function ScoreCard({
  score = 0,
  title = "Match Percentage",
  description,
  variant = "match",
}) {
  const normalizedScore = Math.min(100, Math.max(0, Number(score) || 0));
  const rotation = normalizedScore * 3.6;
  const Icon = variant === "probability" ? Target : Gauge;
  const ringColor = variant === "probability" ? "#126bff" : "#18b27f";
  const defaultDescription =
    normalizedScore >= 80
      ? "Strong alignment for this job description."
      : "Improve missing job-description keywords to raise this score.";

  return (
    <article className="card score-card">
      <div className="card-heading">
        <span className={`card-icon ${variant === "probability" ? "blue" : ""}`}>
          <Icon size={19} />
        </span>
        <div>
          <p>{title}</p>
          <h3>{normalizedScore}/100</h3>
        </div>
      </div>

      <div
        className="score-ring"
        style={{ background: `conic-gradient(${ringColor} ${rotation}deg, #e6edf5 ${rotation}deg)` }}
        aria-label={`${title} ${normalizedScore} out of 100`}
      >
        <span>{normalizedScore}%</span>
      </div>

      <p className="muted">{description || defaultDescription}</p>
    </article>
  );
}

export default ScoreCard;
