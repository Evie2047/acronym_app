export default function SearchResults({
  results,
  suggestions,
  searched,
  onPickSuggestion,
}) {
  if (!searched) return null;

  if (results.length > 0) {
    return (
      <ul className="results">
        {results.map((r) => (
          <li key={r.id} className="result-card">
            <span className="acronym">{r.acronym}</span>
            <div>
              <div className="expansion">{r.expansion}</div>
              {r.description && (
                <div className="description">{r.description}</div>
              )}
            </div>
          </li>
        ))}
      </ul>
    );
  }

  return (
    <div className="no-results">
      <p>No matches found.</p>
      {/* "Did you mean?" - populated once fuzzy_search() is implemented
          on the backend (TASKS.md milestone 1). Until then this list is
          always empty. */}
      {suggestions.length > 0 && (
        <div className="did-you-mean">
          <p>Did you mean:</p>
          <ul>
            {suggestions.map((s) => (
              <li key={`${s.acronym}-${s.expansion}`}>
                <button onClick={() => onPickSuggestion(s.acronym)}>
                  {s.acronym}
                </button>{" "}
                — {s.expansion}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
