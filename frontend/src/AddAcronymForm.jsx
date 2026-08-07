import { useState } from "react";

/**
 * Form for adding a new acronym. The UI works, but the backend endpoint
 * (POST /api/acronyms) returns 501 until it is implemented - see TASKS.md
 * milestone 2. Milestone 3 turns this into a "suggest a change" workflow.
 */
export default function AddAcronymForm() {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({ acronym: "", expansion: "", description: "" });
  const [status, setStatus] = useState(null);

  const update = (field) => (e) =>
    setForm({ ...form, [field]: e.target.value });

  async function handleSubmit(e) {
    e.preventDefault();
    setStatus(null);
    const res = await fetch("/api/acronyms", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    if (res.ok) {
      setStatus({ ok: true, message: `Added ${form.acronym}` });
      setForm({ acronym: "", expansion: "", description: "" });
    } else {
      const body = await res.json().catch(() => ({}));
      setStatus({ ok: false, message: body.detail ?? `Error ${res.status}` });
    }
  }

  return (
    <section className="add-section">
      <button className="toggle-add" onClick={() => setOpen(!open)}>
        {open ? "Cancel" : "Add a new acronym"}
      </button>

      {open && (
        <form onSubmit={handleSubmit} className="add-form">
          <input
            required
            maxLength={20}
            placeholder="Acronym (e.g. ED)"
            value={form.acronym}
            onChange={update("acronym")}
          />
          <input
            required
            placeholder="Expansion (e.g. Emergency Department)"
            value={form.expansion}
            onChange={update("expansion")}
          />
          <input
            placeholder="Description (optional)"
            value={form.description}
            onChange={update("description")}
          />
          <button type="submit">Submit</button>
          {status && (
            <p className={status.ok ? "status-ok" : "status-error"}>
              {status.message}
            </p>
          )}
        </form>
      )}
    </section>
  );
}
