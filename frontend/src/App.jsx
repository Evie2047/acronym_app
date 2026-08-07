import { useEffect, useState } from "react";
import SearchResults from "./SearchResults.jsx";
import AddAcronymForm from "./AddAcronymForm.jsx";

export default function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [searched, setSearched] = useState(false);

  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      setSuggestions([]);
      setSearched(false);
      return;
    }

    // Debounce so we don't hit the API on every keystroke.
    const timer = setTimeout(async () => {
      const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
      const matches = await res.json();
      setResults(matches);
      setSearched(true);

      // No exact matches: ask the backend for "did you mean?" suggestions.
      // This endpoint returns 501 until fuzzy_search() is implemented
      // (TASKS.md milestone 1), so we treat any error as "no suggestions".
      if (matches.length === 0) {
        try {
          const sug = await fetch(`/api/suggest?q=${encodeURIComponent(query)}`);
          setSuggestions(sug.ok ? await sug.json() : []);
        } catch {
          setSuggestions([]);
        }
      } else {
        setSuggestions([]);
      }
    }, 250);

    return () => clearTimeout(timer);
  }, [query]);

  return (
    <div className="container">
      <header>
        <h1>Acronym Searcher</h1>
        <p className="tagline">
          Look up what an acronym means, e.g. <strong>ED</strong> or{" "}
          <strong>OP</strong>
        </p>
      </header>

      <input
        className="search-box"
        type="search"
        placeholder="Type an acronym…"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        autoFocus
      />

      <SearchResults
        results={results}
        suggestions={suggestions}
        searched={searched}
        onPickSuggestion={setQuery}
      />

      <AddAcronymForm />
    </div>
  );
}
