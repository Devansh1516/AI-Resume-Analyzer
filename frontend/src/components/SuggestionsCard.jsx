import { Lightbulb } from "lucide-react";

function SuggestionsCard({ suggestions = [] }) {
  return (
    <article className="card suggestions-card">
      <div className="card-heading">
        <span className="card-icon purple">
          <Lightbulb size={19} />
        </span>
        <div>
          <p>Improvement Suggestions</p>
          <h3>Recommended edits</h3>
        </div>
      </div>

      <ul className="suggestion-list">
        {suggestions.length ? (
          suggestions.map((suggestion) => <li key={suggestion}>{suggestion}</li>)
        ) : (
          <li>No suggestions returned.</li>
        )}
      </ul>
    </article>
  );
}

export default SuggestionsCard;
