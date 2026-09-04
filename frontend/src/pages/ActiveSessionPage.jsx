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

import StrategyComparisonPanel
  from "../components/comparison/StrategyComparisonPanel";

import MLPerformancePanel
  from "../components/ml/MLPerformancePanel";

import SessionSummary
  from "../components/sessions/SessionSummary";

import {
  addSessionSpin,
  generatePrediction,
  getSessionEvaluation,
  getSessionStatistics,
  getStrategyComparison,
  getMLPerformance,
  endSession,
} from "../services/sessionApi";

import ConfirmDialog
  from "../components/common/ConfirmDialog";


function ActiveSessionPage({
  session,
  spins,
  onSpinAdded,
  onNewSession,
  onSessionEnded,
}) {

  const [
    endConfirmationOpen,
    setEndConfirmationOpen,
  ] = useState(false);

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
    comparison,
    setComparison,
  ] = useState(null);

  const [
    mlPerformance,
    setMLPerformance,
  ] = useState(null);

  const [
    ending,
    setEnding,
  ] = useState(false);

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


  const loadComparison =
    useCallback(async () => {
      if (!session) {
        return;
      }

      const data =
        await getStrategyComparison(
          session.session_id
        );

      setComparison(data);
    }, [session]);


  const loadMLPerformance =
    useCallback(async () => {
      if (!session) {
        return;
      }

      const data =
        await getMLPerformance(
          session.session_id
        );

      setMLPerformance(data);
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
            loadComparison(),
            loadMLPerformance(),
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
    loadComparison,
    loadMLPerformance,
    createNextPrediction,
  ]);


  const handleSpin =
    async (number) => {
      if (
        submitting ||
        !session
      ) {
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

        onSpinAdded(
          storedSpin
        );

        await Promise.all([
          loadStatistics(),
          loadEvaluation(),
          loadComparison(),
          loadMLPerformance(),
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


  const handleEndSession =
    async () => {
      if (
        ending ||
        !session
      ) {
        return;
      }

      setEnding(true);
      setError("");

      try {
        const ended =
          await endSession(
            session.session_id
          );

        setEndConfirmationOpen(
          false
        );

        onSessionEnded(
          ended
        );
      } catch (requestError) {
        setError(
          requestError.message
        );
      } finally {
        setEnding(false);
      }
    };


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


      <div className="active-session-actions">
        <button
          type="button"
          className="button button-danger-ghost"
          disabled={ending}
          onClick={() =>
          setEndConfirmationOpen(
            true
          )
        }
        >
          {ending
            ? "Ending..."
            : "End Session"}
        </button>
      </div>


      <div className="live-session-top">
        <RouletteNumberInput
          onSubmit={handleSpin}
          disabled={
            submitting ||
            ending
          }
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


      <div className="session-section">
        <StrategyComparisonPanel
          comparison={comparison}
        />
      </div>


      <div className="session-section">
        <MLPerformancePanel
          performance={
            mlPerformance
          }
        />
      </div>


      <div className="session-section">
        <SessionSummary
          session={session}
          spins={spins}
          evaluation={
            evaluation
          }
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
      
      <ConfirmDialog
        open={
          endConfirmationOpen
        }
        title="End Session?"
        message={
          "This roulette session will be marked " +
          "as ended. New spins cannot be added " +
          "afterward."
        }
        confirmLabel="End Session"
        loading={ending}
        danger
        onCancel={() =>
          setEndConfirmationOpen(
            false
          )
        }
        onConfirm={
          handleEndSession
        }
      />
    </section>
  );
}


export default ActiveSessionPage;