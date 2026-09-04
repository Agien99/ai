import { useState } from "react";

import InitialSpinInput
  from "../components/roulette/InitialSpinInput";

import {
  createSession,
  submitInitialSpins,
} from "../services/sessionApi";

function NewSessionPage({
  onSessionStarted,
}) {
  const [spins, setSpins] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const isValid =
    spins.length >= 10 &&
    spins.length <= 15;

  const startSession = async () => {
    if (!isValid || loading) {
      return;
    }

    setLoading(true);
    setError("");

    try {
      const created =
        await createSession();

      const activeSession =
        await submitInitialSpins(
          created.session_id,
          spins
        );

      const initialSpinRecords =
        spins.map(
          (number, index) => ({
            spin_id:
              `initial-${index + 1}`,
            session_id:
              activeSession.session_id,
            spin_index:
              index + 1,
            number,
            spin_type: "INITIAL",
          })
        );

      onSessionStarted(
        activeSession,
        initialSpinRecords
      );
    } catch (requestError) {
      setError(
        requestError.message
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="page">
      <div className="page-heading">
        <div>
          <span className="page-eyebrow">
            Session Setup
          </span>

          <h1>
            Start New Session
          </h1>

          <p>
            Enter the most recent
            roulette results before
            starting live analysis.
          </p>
        </div>

        <span className="development-badge">
          10–15 Spins
        </span>
      </div>

      <div className="new-session-layout">
        <InitialSpinInput
          spins={spins}
          onChange={setSpins}
          disabled={loading}
        />

        <aside className="session-guide panel">
          <span className="panel-eyebrow">
            How it works
          </span>

          <h2>
            Session Setup
          </h2>

          <div className="setup-steps">
            <div className="setup-step">
              <span>1</span>

              <div>
                <strong>
                  Enter history
                </strong>

                <p>
                  Add the latest
                  10–15 results.
                </p>
              </div>
            </div>

            <div className="setup-step">
              <span>2</span>

              <div>
                <strong>
                  Start analysis
                </strong>

                <p>
                  The backend creates
                  an isolated session.
                </p>
              </div>
            </div>

            <div className="setup-step">
              <span>3</span>

              <div>
                <strong>
                  Enter live spins
                </strong>

                <p>
                  New results update
                  the session.
                </p>
              </div>
            </div>
          </div>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <button
            type="button"
            className="button button-primary start-session-button"
            disabled={
              !isValid ||
              loading
            }
            onClick={startSession}
          >
            {loading
              ? "Starting..."
              : "Start Session"}
          </button>
        </aside>
      </div>
    </section>
  );
}

export default NewSessionPage;