import {
  useEffect,
  useState,
} from "react";

import {
  getSessions,
} from "../services/sessionApi";

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

function SessionHistoryPage({
  onOpenSession,
}) {
  const [
    sessions,
    setSessions,
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
    const load = async () => {
      try {
        setError("");

        const data =
          await getSessions();

        setSessions(data);
      } catch (requestError) {
        setError(
          requestError.message
        );
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  return (
    <section className="page">
      <div className="page-heading">
        <div>
          <span className="page-eyebrow">
            Historical Data
          </span>

          <h1>
            Session History
          </h1>

          <p>
            Review active and
            completed roulette
            sessions stored in Neon.
          </p>
        </div>

        <span className="development-badge">
          {sessions.length}
          {" "}
          Sessions
        </span>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {loading ? (
        <div className="panel panel-loading">
          Loading sessions...
        </div>
      ) : sessions.length === 0 ? (
        <div className="panel no-session-panel">
          <h2>
            No Session History
          </h2>

          <p>
            Sessions will appear
            here after they have
            been created.
          </p>
        </div>
      ) : (
        <div className="history-session-grid">
          {sessions.map(
            (session) => (
              <article
                className="history-session-card"
                key={
                  session.session_id
                }
              >
                <div className="history-session-top">
                  <span
                    className={
                      session.status ===
                      "ACTIVE"
                        ? "history-status active"
                        : "history-status ended"
                    }
                  >
                    {session.status}
                  </span>

                  <span className="history-session-date">
                    {formatDate(
                      session.started_at
                    )}
                  </span>
                </div>

                <h2>
                  Session
                </h2>

                <code>
                  {session.session_id}
                </code>

                <div className="history-session-meta">
                  <div>
                    <span>
                      Initial Spins
                    </span>

                    <strong>
                      {
                        session
                          .initial_spin_count
                      }
                    </strong>
                  </div>

                  <div>
                    <span>
                      Ended
                    </span>

                    <strong>
                      {session.ended_at
                        ? "Yes"
                        : "No"}
                    </strong>
                  </div>
                </div>

                <button
                  type="button"
                  className="button button-secondary"
                  onClick={() =>
                    onOpenSession(
                      session
                        .session_id
                    )
                  }
                >
                  View Details
                </button>
              </article>
            )
          )}
        </div>
      )}
    </section>
  );
}

export default SessionHistoryPage;