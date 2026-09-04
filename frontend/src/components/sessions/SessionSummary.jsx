function formatDate(
  value
) {
  if (!value) {
    return "—";
  }

  return new Date(
    value
  ).toLocaleString();
}

function SessionSummary({
  session,
  spins = [],
  evaluation,
}) {
  const initial =
    spins.filter(
      (spin) =>
        spin.spin_type ===
        "INITIAL"
    ).length;

  const observed =
    spins.filter(
      (spin) =>
        spin.spin_type ===
        "OBSERVED"
    ).length;

  return (
    <div className="panel">
      <div className="panel-header">
        <div>
          <span className="panel-eyebrow">
            Session
          </span>

          <h2>
            Session Summary
          </h2>
        </div>

        <span
          className={
            session?.status ===
            "ACTIVE"
              ? "summary-status active"
              : "summary-status ended"
          }
        >
          {session?.status}
        </span>
      </div>

      <div className="summary-grid">
        <div>
          <span>
            Total Spins
          </span>

          <strong>
            {spins.length}
          </strong>
        </div>

        <div>
          <span>
            Initial Spins
          </span>

          <strong>
            {initial}
          </strong>
        </div>

        <div>
          <span>
            Observed Spins
          </span>

          <strong>
            {observed}
          </strong>
        </div>

        <div>
          <span>
            Evaluations
          </span>

          <strong>
            {
              evaluation
                ?.evaluation_count ??
              0
            }
          </strong>
        </div>

        <div>
          <span>
            Started
          </span>

          <strong>
            {formatDate(
              session?.started_at
            )}
          </strong>
        </div>

        <div>
          <span>
            Ended
          </span>

          <strong>
            {formatDate(
              session?.ended_at
            )}
          </strong>
        </div>
      </div>
    </div>
  );
}

export default SessionSummary;