import { BadgeCheck } from "lucide-react";

function SkillsCard({
  resumeSkills = [],
  matchedSkills = [],
  title = "Skills Found",
}) {
  const resumeSkillCount = resumeSkills.length;
  const matchedSkillCount = matchedSkills.length;

  return (
    <article className="card">
      <div className="card-heading">
        <span className="card-icon success">
          <BadgeCheck size={19} />
        </span>
        <div>
          <p>{title}</p>
          <h3>{matchedSkillCount}/{resumeSkillCount || matchedSkillCount} matched</h3>
        </div>
      </div>

      <div className="skill-groups">
        <div>
          <h4>Present in Resume</h4>
          <div className="pill-list">
            {resumeSkills.length ? (
              resumeSkills.map((skill) => <span key={skill}>{skill}</span>)
            ) : (
              <span>No resume skills detected</span>
            )}
          </div>
        </div>

        <div>
          <h4>Matching Job Skills</h4>
          <div className="pill-list match-list">
            {matchedSkills.length ? (
              matchedSkills.map((skill) => <span key={skill}>{skill}</span>)
            ) : (
              <span>No job skills matched</span>
            )}
          </div>
        </div>
      </div>
    </article>
  );
}

export default SkillsCard;
