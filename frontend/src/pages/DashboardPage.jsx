import {
  useEffect,
  useState,
} from "react";

import {
  getSessionSpins,
  getSessions,
} from "../services/sessionApi";


function DashboardPage({
  onNewSession,
  onOpenSession,
  onOpenHistory,
}) {
  const [
    sessions,
    setSessions,
  ] = useState([]);

  const [
    latestActiveSession,
    setLatestActiveSession,
  ] = useState(null);

  const [
    latestActiveSpins,
    setLatestActiveSpins,
  ] = useState([]);

  const [
    loading,
    setLoading,
  ] = useState(true);

  const [
    error,
    setError,
  ] = useState("");


  useEffect(() => {
    let cancelled = false;


    const loadDashboard =
      async () => {
        try {
          const sessionData =
            await getSessions();


          if (cancelled) {
            return;
          }


          const allSessions =
            Array.isArray(
              sessionData
            )
              ? sessionData
              : [];


          setSessions(
            allSessions
          );


          const activeSessions =
            allSessions
              .filter(
                (item) =>
                  item.status ===
                  "ACTIVE"
              )
              .sort(
                (a, b) => {
                  const aTime =
                    new Date(
                      a.started_at ||
                      a.created_at ||
                      0
                    ).getTime();

                  const bTime =
                    new Date(
                      b.started_at ||
                      b.created_at ||
                      0
                    ).getTime();

                  return (
                    bTime -
                    aTime
                  );
                }
              );


          if (
            activeSessions.length === 0
          ) {
            setLatestActiveSession(
              null
            );

            setLatestActiveSpins(
              []
            );

            return;
          }


          const latest =
            activeSessions[0];


          const spinData =
            await getSessionSpins(
              latest.session_id
            );


          if (cancelled) {
            return;
          }


          setLatestActiveSession(
            latest
          );

          setLatestActiveSpins(
            Array.isArray(spinData)
              ? spinData
              : []
          );
        } catch (requestError) {
          if (!cancelled) {
            setError(
              requestError.message
            );
          }
        } finally {
          if (!cancelled) {
            setLoading(false);
          }
        }
      };


    loadDashboard();


    return () => {
      cancelled = true;
    };
  }, []);


  const activeSessions =
    sessions.filter(
      (item) =>
        item.status === "ACTIVE"
    );


  const endedSessions =
    sessions.filter(
      (item) =>
        item.status === "ENDED"
    );


  const initialCount =
    latestActiveSpins.filter(
      (spin) =>
        spin.spin_type ===
        "INITIAL"
    ).length;


  const observedCount =
    latestActiveSpins.filter(
      (spin) =>
        spin.spin_type ===
        "OBSERVED"
    ).length;


  const formatDate = (
    value
  ) => {
    if (!value) {
      return "Not available";
    }


    const date =
      new Date(value);


    if (
      Number.isNaN(
        date.getTime()
      )
    ) {
      return "Not available";
    }


    return date.toLocaleString();
  };


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
            Monitor roulette sessions,
            continue unfinished analysis
            and review prediction activity
            across your recorded data.
          </p>
        </div>


        <div className="dashboard-hero-actions">
          {latestActiveSession && (
            <button
              type="button"
              className="button button-secondary"
              onClick={
                onOpenSession
              }
            >
              Open Latest Active
            </button>
          )}


          <button
            type="button"
            className="button button-primary"
            onClick={
              onNewSession
            }
          >
            + Start New Session
          </button>
        </div>
      </div>


      {error && (
        <div className="error-message">
          {error}
        </div>
      )}


      <div className="dashboard-metrics">
        <article className="metric-card">
          <span>
            Active Sessions
          </span>

          <strong
            className={
              activeSessions.length > 0
                ? "metric-green"
                : ""
            }
          >
            {loading
              ? "..."
              : activeSessions.length}
          </strong>

          <small>
            Unfinished sessions
          </small>
        </article>


        <article className="metric-card">
          <span>
            Total Sessions
          </span>

          <strong>
            {loading
              ? "..."
              : sessions.length}
          </strong>

          <small>
            Recorded sessions
          </small>
        </article>


        <article className="metric-card">
          <span>
            Ended Sessions
          </span>

          <strong>
            {loading
              ? "..."
              : endedSessions.length}
          </strong>

          <small>
            Completed sessions
          </small>
        </article>


        <article className="metric-card">
          <span>
            Latest Spins
          </span>

          <strong>
            {loading
              ? "..."
              : latestActiveSpins.length}
          </strong>

          <small>
            Latest active session
          </small>
        </article>
      </div>


      <div className="dashboard-sections">
        <div className="panel dashboard-main-panel">
          <div className="dashboard-panel-heading">
            <div>
              <span className="panel-eyebrow">
                Latest Active Session
              </span>

              <h2>
                Session Activity
              </h2>
            </div>


            {latestActiveSession && (
              <span className="summary-status active">
                ACTIVE
              </span>
            )}
          </div>


          {loading ? (
            <div className="dashboard-loading">
              Loading session data...
            </div>
          ) : latestActiveSession ? (
            <>
              <p className="dashboard-session-description">
                The most recently started
                active session is ready to
                continue.
              </p>


              <div className="dashboard-session-metrics">
                <div>
                  <span>
                    Initial Spins
                  </span>

                  <strong>
                    {initialCount}
                  </strong>
                </div>


                <div>
                  <span>
                    Observed Spins
                  </span>

                  <strong>
                    {observedCount}
                  </strong>
                </div>


                <div>
                  <span>
                    Total Spins
                  </span>

                  <strong>
                    {
                      latestActiveSpins
                        .length
                    }
                  </strong>
                </div>
              </div>


              <div className="dashboard-session-info">
                <div>
                  <span>
                    Started
                  </span>

                  <strong>
                    {formatDate(
                      latestActiveSession
                        .started_at
                    )}
                  </strong>
                </div>


                <div>
                  <span>
                    Session ID
                  </span>

                  <code>
                    {
                      latestActiveSession
                        .session_id
                    }
                  </code>
                </div>
              </div>


              <button
                type="button"
                className="button button-primary dashboard-continue-button"
                onClick={
                  onOpenSession
                }
              >
                Continue Latest Session
              </button>
            </>
          ) : (
            <div className="dashboard-empty-session">
              <div className="no-session-icon">
                +
              </div>

              <h3>
                No Active Sessions
              </h3>

              <p>
                There are currently no
                unfinished roulette
                sessions.
              </p>

              <button
                type="button"
                className="button button-primary"
                onClick={
                  onNewSession
                }
              >
                Start New Session
              </button>
            </div>
          )}
        </div>


        <div className="panel dashboard-side-panel">
          <span className="panel-eyebrow">
            Session Overview
          </span>

          <h2>
            Stored Sessions
          </h2>

          <p>
            Overview of the sessions
            currently stored by the
            backend.
          </p>


          <div className="dashboard-overview-list">
            <div>
              <span>
                Active
              </span>

              <strong
                className={
                  activeSessions.length > 0
                    ? "metric-green"
                    : ""
                }
              >
                {loading
                  ? "..."
                  : activeSessions.length}
              </strong>
            </div>


            <div>
              <span>
                Ended
              </span>

              <strong>
                {loading
                  ? "..."
                  : endedSessions.length}
              </strong>
            </div>


            <div>
              <span>
                Total
              </span>

              <strong>
                {loading
                  ? "..."
                  : sessions.length}
              </strong>
            </div>
          </div>


          <button
            type="button"
            className="button button-secondary dashboard-history-button"
            onClick={
              onOpenHistory
            }
          >
            View Session History
          </button>
        </div>
      </div>
    </section>
  );
}


export default DashboardPage;