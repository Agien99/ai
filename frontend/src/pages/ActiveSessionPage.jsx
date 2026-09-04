import {
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";

import SpinHistory
  from "../components/roulette/SpinHistory";

import SpinEntryModal
  from "../components/roulette/SpinEntryModal";

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

import ConfirmDialog
  from "../components/common/ConfirmDialog";

import {
  addSessionSpin,
  generatePrediction,
  getLatestPrediction,
  getSessionEvaluation,
  getSessionStatistics,
  getStrategyComparison,
  getMLPerformance,
  endSession,
} from "../services/sessionApi";


const predictionCategoryMap = {
  DOZENS: "dozens",
  COLUMNS: "columns",
  STREETS: "streets",
  SPLITS: "splits",
  CORNERS: "corners",
};


function normalizeStoredPrediction(
  storedPrediction
) {
  if (
    !storedPrediction
      ?.prediction_run
  ) {
    return null;
  }


  const run =
    storedPrediction
      .prediction_run;


  const predictions = {
    dozens: [],
    columns: [],
    streets: [],
    splits: [],
    corners: [],
  };


  let numberProbabilities =
    null;


  for (
    const item of
    storedPrediction
      .prediction_items || []
  ) {
    if (
      item.category ===
      "NUMBER_PROBABILITIES"
    ) {
      numberProbabilities =
        item.payload;

      continue;
    }


    const predictionKey =
      predictionCategoryMap[
        item.category
      ];


    if (!predictionKey) {
      continue;
    }


    predictions[
      predictionKey
    ] =
      item.payload || [];
  }


  return {
    prediction_run_id:
      run.prediction_run_id,

    session_id:
      run.session_id,

    strategy:
      run.strategy_key,

    prediction_for_spin_index:
      run.prediction_for_spin_index,

    input_spin_count:
      run.input_spin_count,

    recent_window:
      run.recent_window,

    model_version_id:
      run.model_version_id,

    predictions,

    number_probabilities:
      numberProbabilities,
  };
}


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
    spinModalOpen,
    setSpinModalOpen,
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


  /*
   * Keep the latest spin count available
   * without making session initialization
   * depend on every spins.length change.
   */
  const spinCountRef =
    useRef(spins.length);


  useEffect(() => {
    spinCountRef.current =
      spins.length;
  }, [spins.length]);


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

      setPredictionLoading(
        true
      );

      try {
        const data =
          await generatePrediction(
            session.session_id,
            "v1",
            10
          );

        setPrediction(
          data
        );
      } catch (requestError) {
        setError(
          requestError.message
        );
      } finally {
        setPredictionLoading(
          false
        );
      }
    }, [session]);


  const loadOrCreatePrediction =
    useCallback(async () => {
      if (!session) {
        return;
      }

      setPredictionLoading(
        true
      );

      try {
        let storedPrediction =
          null;

        try {
          storedPrediction =
            await getLatestPrediction(
              session.session_id
            );
        } catch {
          storedPrediction =
            null;
        }


        const normalized =
          normalizeStoredPrediction(
            storedPrediction
          );


        const nextSpinIndex =
          spinCountRef.current + 1;


        if (
          normalized &&
          normalized
            .prediction_for_spin_index ===
            nextSpinIndex
        ) {
          setPrediction(
            normalized
          );

          return;
        }


        const generated =
          await generatePrediction(
            session.session_id,
            "v1",
            10
          );

        setPrediction(
          generated
        );
      } catch (requestError) {
        setError(
          requestError.message
        );
      } finally {
        setPredictionLoading(
          false
        );
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

          await loadOrCreatePrediction();
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
    loadOrCreatePrediction,
  ]);


  const handleRefreshPrediction =
    async () => {
      setError("");

      await loadOrCreatePrediction();
    };


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


        /*
         * Update the ref immediately.
         * We do not need to wait for the
         * parent React state update.
         */
        spinCountRef.current += 1;


        onSpinAdded(
          storedSpin
        );


        setSpinModalOpen(
          false
        );


        await Promise.all([
          loadStatistics(),
          loadEvaluation(),
          loadComparison(),
          loadMLPerformance(),
        ]);


        /*
         * This is now the ONLY automatic
         * prediction creation path after
         * recording a new observed spin.
         */
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

        setSpinModalOpen(
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
            enter at least 10 initial
            spins to begin.
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
            Review the current prediction
            and record each new roulette
            result as it appears.
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


      <div className="live-session-history">
        <SpinHistory
          spins={spins}
        />
      </div>


      <div className="live-session-actions">
        <button
          type="button"
          className="button button-primary"
          disabled={
            submitting ||
            ending
          }
          onClick={() =>
            setSpinModalOpen(
              true
            )
          }
        >
          + Record Spin Result
        </button>


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


      <div className="session-section live-prediction-section">
        <PredictionPanel
          prediction={
            prediction
          }
          loading={
            predictionLoading
          }
          onRefresh={
            handleRefreshPrediction
          }
        />
      </div>


      <div className="session-section">
        <EvaluationPanel
          evaluation={
            evaluation
          }
        />
      </div>


      <div className="session-section">
        <StatisticsPanel
          statistics={
            statistics
          }
        />
      </div>


      <div className="session-section">
        <StrategyComparisonPanel
          comparison={
            comparison
          }
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
          session={
            session
          }
          spins={
            spins
          }
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


      <SpinEntryModal
        open={
          spinModalOpen
        }
        onClose={() =>
          setSpinModalOpen(
            false
          )
        }
        onSubmit={
          handleSpin
        }
        disabled={
          submitting ||
          ending
        }
      />


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
        loading={
          ending
        }
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