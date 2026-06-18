import { SearchX } from "lucide-react";

function KeywordCard({ keywords = [] }) {
  return (
    <article className="card">
      <div className="card-heading">
        <span className="card-icon warning">
          <SearchX size={19} />
        </span>
        <div>
          <p>Missing Keywords</p>
          <h3>{keywords.length} gaps</h3>
        </div>
      </div>

      <div className="pill-list warning-list">
        {keywords.length
          ? keywords.map((keyword) => <span key={keyword}>{keyword}</span>)
          : <span>No major keyword gaps found</span>}
      </div>
    </article>
  );
}

export default KeywordCard;
