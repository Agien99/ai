function formatGroup(
  value
) {
  if (Array.isArray(value)) {
    return value.join(" · ");
  }

  return value;
}

function scorePercentage(
  score
) {
  if (
    score === undefined ||
    score === null
  ) {
    return null;
  }

  return Math.round(
    score * 100
  );
}

function PredictionGroup({
  title,
  items = [],
  valueKey,
  labelPrefix = "",
}) {
  return (
    <div className="prediction-group">
      <div className="prediction-group-header">
        <h3>{title}</h3>

        <span>
          {items.length}
        </span>
      </div>

      {items.length === 0 ? (
        <div className="prediction-empty">
          No predictions.
        </div>
      ) : (
        <div className="prediction-items">
          {items.map(
            (item, index) => {
              const score =
                scorePercentage(
                  item.prediction_score
                );

              return (
                <div
                  className="prediction-item"
                  key={
                    `${valueKey}-` +
                    `${index}-` +
                    `${JSON.stringify(
                      item[valueKey]
                    )}`
                  }
                >
                  <div className="prediction-rank">
                    #{index + 1}
                  </div>

                  <div className="prediction-value">
                    {labelPrefix}
                    {formatGroup(
                      item[valueKey]
                    )}
                  </div>

                  {score !== null && (
                    <div className="prediction-score">
                      {score}
                    </div>
                  )}
                </div>
              );
            }
          )}
        </div>
      )}
    </div>
  );
}

function PredictionPanel({
  prediction,
  loading = false,
  onRefresh,
}) {
  if (loading && !prediction) {
    return (
      <div className="panel">
        <div className="panel-loading">
          Generating prediction...
        </div>
      </div>
    );
  }

  if (!prediction) {
    return (
      <div className="panel">
        <div className="panel-header">
          <div>
            <span className="panel-eyebrow">
              Prediction Engine
            </span>

            <h2>
              Latest Prediction
            </h2>
          </div>
        </div>

        <div className="prediction-no-data">
          <h3>
            No prediction generated
          </h3>

          <p>
            Generate the prediction
            for the next roulette
            result.
          </p>

          <button
            type="button"
            className="button button-primary"
            disabled={loading}
            onClick={onRefresh}
          >
            Generate Prediction
          </button>
        </div>
      </div>
    );
  }

  const predictions =
    prediction.predictions || {};

  return (
    <div className="panel prediction-panel">
      <div className="panel-header">
        <div>
          <span className="panel-eyebrow">
            Prediction Engine V1
          </span>

          <h2>
            Latest Prediction
          </h2>

          <p>
            Prediction for spin{" "}
            <strong>
              #
              {
                prediction
                  .prediction_for_spin_index
              }
            </strong>
          </p>
        </div>

        <button
          type="button"
          className="button button-secondary"
          disabled={loading}
          onClick={onRefresh}
        >
          {loading
            ? "Generating..."
            : "Regenerate"}
        </button>
      </div>

      <div className="prediction-grid">
        <PredictionGroup
          title="Dozens"
          items={
            predictions.dozens
          }
          valueKey="dozen"
          labelPrefix="Dozen "
        />

        <PredictionGroup
          title="Columns"
          items={
            predictions.columns
          }
          valueKey="column"
          labelPrefix="Column "
        />

        <PredictionGroup
          title="Streets"
          items={
            predictions.streets
          }
          valueKey="street"
        />

        <PredictionGroup
          title="Splits"
          items={
            predictions.splits
          }
          valueKey="split"
        />

        <PredictionGroup
          title="Corners"
          items={
            predictions.corners
          }
          valueKey="corner"
        />
      </div>
    </div>
  );
}

export default PredictionPanel;