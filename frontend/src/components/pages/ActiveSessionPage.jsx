import { useState } from "react";

import RouletteNumberInput
  from "../components/roulette/RouletteNumberInput";

import SpinHistory
  from "../components/roulette/SpinHistory";

import {
  addSessionSpin,
} from "../services/sessionApi";

function ActiveSessionPage({
  session,
  spins,
  onSpinAdded,
  onNewSession,
}) {
  const [submitting, setSubmitting] =
    useState(false);

  const [error, setError] =
    useState("");

  if (!session) {
    return (
      <section className="page">
        <div className="page-heading">
          <div>
            <span className="page-eyebrow">
              Live Analysis
            </span>

            <h1>
              Active Session
            </h1>

            <p>
              There is currently no
              active roulette session.
            </p>
          </div>
        </div>

        <div className="panel no-session-panel">
          <div className="no-session-icon">
            +
          </div>

          <h2>
            No Active Session
          </h2>

          <p>
            Create a new session and
            enter 10–15 initial spins
            to begin.
          </p>

          <button
            type="button"
            className="button button-primary"
            onClick={onNewSession}
          >
            Start New Session
          </button>
        </div>
      </section>
    );
  }

  const handleSpin = async (
    number
  ) => {
    if (submitting) {
      return;
    }

    setSubmitting(true);
    setError("");

    try {
      const storedSpin =
        await addSessionSpin(
          session.session_id,
          number
        );

      onSpinAdded(storedSpin);
    } catch (requestError) {
      setError(
        requestError.message
      );
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <section className="page">
      <div className="page-heading active-heading">
        <div>
          <span className="page-eyebrow">
            Live Analysis
          </span>

          <h1>
            Active Session
          </h1>

          <p>
            Enter each new roulette
            result as it occurs.
          </p>
        </div>

        <div className="session-status-card">
          <span className="status-dot" />

          <div>
            <small>
              SESSION
            </small>

            <strong>
              ACTIVE
            </strong>
          </div>
        </div>
      </div>

      {error && (
        <div className="error-message page-error">
          {error}
        </div>
      )}

      <div className="active-session-grid">
        <RouletteNumberInput
          onSubmit={handleSpin}
          disabled={submitting}
        />

        <SpinHistory
          spins={spins}
        />
      </div>

      <div className="session-meta">
        <span>
          Session ID
        </span>

        <code>
          {session.session_id}
        </code>

        <span className="session-spin-total">
          {spins.length} total spins
        </span>
      </div>
    </section>
  );
}

export default ActiveSessionPage;