function DashboardPage({
  session,
  spins,
  onNewSession,
  onOpenSession,
}) {
  const hasSession =
    session?.status === "ACTIVE";

  const initialCount =
    spins.filter(
      (spin) =>
        spin.spin_type === "INITIAL"
    ).length;

  const observedCount =
    spins.filter(
      (spin) =>
        spin.spin_type === "OBSERVED"
    ).length;

  return (
    <section className="page">
      <div className="dashboard-hero">
        <div>
          <span className="page-eyebrow">
            AI-Powered Analysis
          </span>

          <h1>
            Roulette AI
          </h1>

          <p>
            Analyze session patterns,
            generate ranked predictions
            and evaluate performance
            over time.
          </p>
        </div>

        <button
          type="button"
          className="button button-primary"
          onClick={
            hasSession
              ? onOpenSession
              : onNewSession
          }
        >
          {hasSession
            ? "Open Active Session"
            : "Start New Session"}
        </button>
      </div>

      <div className="dashboard-metrics">
        <article className="metric-card">
          <span>
            Session
          </span>

          <strong
            className={
              hasSession
                ? "metric-green"
                : ""
            }
          >
            {hasSession
              ? "ACTIVE"
              : "NONE"}
          </strong>

          <small>
            Current state
          </small>
        </article>

        <article className="metric-card">
          <span>
            Initial Spins
          </span>

          <strong>
            {initialCount}
          </strong>

          <small>
            Starting history
          </small>
        </article>

        <article className="metric-card">
          <span>
            Live Spins
          </span>

          <strong>
            {observedCount}
          </strong>

          <small>
            Observed results
          </small>
        </article>

        <article className="metric-card">
          <span>
            Total Spins
          </span>

          <strong>
            {spins.length}
          </strong>

          <small>
            Current session
          </small>
        </article>
      </div>

      <div className="dashboard-sections">
        <div className="panel dashboard-main-panel">
          <span className="panel-eyebrow">
            Prediction Engine
          </span>

          <h2>
            AI Predictions
          </h2>

          <p>
            Ranked dozens, columns,
            streets, splits and corners
            will appear here in the
            next batch.
          </p>

          <div className="coming-soon-grid">
            <span>Dozens</span>
            <span>Columns</span>
            <span>Streets</span>
            <span>Splits</span>
            <span>Corners</span>
          </div>
        </div>

        <div className="panel dashboard-side-panel">
          <span className="panel-eyebrow">
            Current Session
          </span>

          <h2>
            Session Status
          </h2>

          {hasSession ? (
            <>
              <div className="dashboard-session-status">
                <span className="status-dot" />
                Active
              </div>

              <p>
                Continue entering live
                roulette results.
              </p>

              <button
                type="button"
                className="button button-secondary"
                onClick={onOpenSession}
              >
                View Session
              </button>
            </>
          ) : (
            <>
              <p>
                Start a session to begin
                collecting roulette data.
              </p>

              <button
                type="button"
                className="button button-secondary"
                onClick={onNewSession}
              >
                New Session
              </button>
            </>
          )}
        </div>
      </div>
    </section>
  );
}

export default DashboardPage;