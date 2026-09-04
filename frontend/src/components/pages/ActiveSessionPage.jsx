import {
  useCallback,
  useEffect,
  useState,
} from "react";

import RouletteNumberInput
  from "../components/roulette/RouletteNumberInput";

import SpinHistory
  from "../components/roulette/SpinHistory";

import PredictionPanel
  from "../components/predictions/PredictionPanel";

import EvaluationPanel
  from "../components/predictions/EvaluationPanel";

import StatisticsPanel
  from "../components/statistics/StatisticsPanel";

import {
  addSessionSpin,
  generatePrediction,
  getSessionEvaluation,
  getSessionStatistics,
} from "../services/sessionApi";

function ActiveSessionPage({
  session,
  spins,
  onSpinAdded,
  onNewSession,
}) {
  const [
    submitting,
    setSubmitting,
  ] = useState(false);

  const [
    predictionLoading,
    setPredictionLoading,
  ] = useState(false);

  const [
    prediction,
    setPrediction,
  ] = useState(null);

  const [
    statistics,
    setStatistics,
  ] = useState(null);

  const [
    evaluation,
    setEvaluation,
  ] = useState(null);

  const [
    error,
    setError,
  ] = useState("");

  const loadStatistics =
    useCallback(async () => {
      if (!session) {
        return;
      }

      const data =
        await getSessionStatistics(
          session.session_id
        );

      setStatistics(data);
    }, [session]);

  const loadEvaluation =
    useCallback(async () => {
      if (!session) {
        return;
      }

      const data =
        await getSessionEvaluation(
          session.session_id
        );

      setEvaluation(data);
    }, [session]);

  const createNextPrediction =
    useCallback(async () => {
      if (!session) {
        return;
      }

      setPredictionLoading(true);

      try {
        const data =
          await generatePrediction(
            session.session_id,
            "v1",
            10
          );

        setPrediction(data);
      } catch (requestError) {
        setError(
          requestError.message
        );
      } finally {
        setPredictionLoading(false);
      }
    }, [session]);

  useEffect(() => {
    if (!session) {
      return;
    }

    const loadSessionData =
      async () => {
        try {
          setError("");

          await Promise.all([
            loadStatistics(),
            loadEvaluation(),
          ]);

          await createNextPrediction();
        } catch (requestError) {
          setError(
            requestError.message
          );
        }
      };

    loadSessionData();
  }, [
    session,
    loadStatistics,
    loadEvaluation,
    createNextPrediction,
  ]);

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

      await Promise.all([
        loadStatistics(),
        loadEvaluation(),
      ]);

      await createNextPrediction();
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
            Enter each roulette
            result and review the
            updated prediction.
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

      <div className="live-session-top">
        <RouletteNumberInput
          onSubmit={handleSpin}
          disabled={submitting}
        />

        <SpinHistory
          spins={spins}
        />
      </div>

      <div className="session-section">
        <PredictionPanel
          prediction={prediction}
          loading={
            predictionLoading
          }
          onRefresh={
            createNextPrediction
          }
        />
      </div>

      <div className="session-section">
        <EvaluationPanel
          evaluation={evaluation}
        />
      </div>

      <div className="session-section">
        <StatisticsPanel
          statistics={statistics}
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