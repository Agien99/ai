import {
  useEffect,
  useState,
} from "react";

import SpinHistory
  from "../components/roulette/SpinHistory";

import SessionSummary
  from "../components/sessions/SessionSummary";

import EvaluationPanel
  from "../components/predictions/EvaluationPanel";

import StrategyComparisonPanel
  from "../components/comparison/StrategyComparisonPanel";

import StatisticsPanel
  from "../components/statistics/StatisticsPanel";

import ConfirmDialog
  from "../components/common/ConfirmDialog";

import {
  endSession,
  getSession,
  getSessionSpins,
  getSessionStatistics,
  getSessionEvaluation,
  getStrategyComparison,
} from "../services/sessionApi";


function SessionHistoryDetailPage({
  sessionId,
  onBack,
  onContinueSession,
  resumeLoading = false,
}) {
  const [
    session,
    setSession,
  ] = useState(null);

  const [
    spins,
    setSpins,
  ] = useState([]);

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
    loading,
    setLoading,
  ] = useState(true);

  const [
    ending,
    setEnding,
  ] = useState(false);

  const [
    endConfirmationOpen,
    setEndConfirmationOpen,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState("");


  useEffect(() => {
    const load = async () => {
      try {
        setError("");

        const [
          sessionData,
          spinData,
          statsData,
          evaluationData,
          comparisonData,
        ] = await Promise.all([
          getSession(sessionId),

          getSessionSpins(
            sessionId
          ),

          getSessionStatistics(
            sessionId
          ),

          getSessionEvaluation(
            sessionId
          ),

          getStrategyComparison(
            sessionId
          ),
        ]);

        setSession(
          sessionData
        );

        setSpins(
          spinData
        );

        setStatistics(
          statsData
        );

        setEvaluation(
          evaluationData
        );

        setComparison(
          comparisonData
        );
      } catch (requestError) {
        setError(
          requestError.message
        );
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [sessionId]);


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
        const endedSession =
          await endSession(
            session.session_id
          );

        setSession(
          endedSession
        );

        setEndConfirmationOpen(
          false
        );
      } catch (requestError) {
        setError(
          requestError.message
        );
      } finally {
        setEnding(false);
      }
    };


  const isActive =
    session?.status === "ACTIVE";


  if (loading) {
    return (
      <div className="panel panel-loading">
        Loading session...
      </div>
    );
  }


  return (
    <section className="page">
      <button
        type="button"
        className="back-button"
        onClick={onBack}
      >
        ← Session History
      </button>


      <div className="page-heading">
        <div>
          <span className="page-eyebrow">
            Historical Session
          </span>

          <h1>
            Session Detail
          </h1>

          <p>
            Review stored spins,
            statistics and prediction
            performance.
          </p>
        </div>


        {isActive && (
          <div className="history-detail-actions">
            <button
              type="button"
              className="button button-primary"
              disabled={
                resumeLoading ||
                ending
              }
              onClick={() =>
                onContinueSession(
                  session.session_id
                )
              }
            >
              {resumeLoading
                ? "Opening..."
                : "Continue Session"}
            </button>

            <button
              type="button"
              className="button button-danger-ghost"
              disabled={
                resumeLoading ||
                ending
              }
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
        )}
      </div>


      {error && (
        <div className="error-message">
          {error}
        </div>
      )}


      {session && (
        <>
          <SessionSummary
            session={session}
            spins={spins}
            evaluation={
              evaluation
            }
          />


          <div className="session-section">
            <SpinHistory
              spins={spins}
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
            <StrategyComparisonPanel
              comparison={
                comparison
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
        </>
      )}


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


export default SessionHistoryDetailPage;