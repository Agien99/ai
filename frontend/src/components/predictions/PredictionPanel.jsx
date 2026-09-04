function formatGroup(
  value
) {
  if (Array.isArray(value)) {
    return value.join(" · ");
  }

  return value;
}


function formatScore(
  score
) {
  if (
    score === undefined ||
    score === null
  ) {
    return null;
  }

  return Number(
    score
  ).toFixed(2);
}


function getScoreWidth(
  score
) {
  const numericScore =
    Number(score);

  if (
    !Number.isFinite(
      numericScore
    )
  ) {
    return 0;
  }

  return Math.max(
    0,
    Math.min(
      100,
      (numericScore / 3) * 100
    )
  );
}


function ScoreBar({
  score,
}) {
  const formattedScore =
    formatScore(score);

  if (
    formattedScore === null
  ) {
    return null;
  }

  return (
    <div className="prediction-score-block">
      <div className="prediction-score-meta">
        <span>
          Score
        </span>

        <strong>
          {formattedScore}
        </strong>
      </div>

      <div className="prediction-score-track">
        <div
          className="prediction-score-fill"
          style={{
            width:
              `${getScoreWidth(
                score
              )}%`,
          }}
        />
      </div>
    </div>
  );
}


function PrimaryPredictionItem({
  item,
  index,
  valueKey,
  labelPrefix = "",
}) {
  const value =
    formatGroup(
      item[valueKey]
    );

  const isTop =
    index === 0;


  return (
    <div
      className={
        isTop
          ? "primary-prediction-item primary-prediction-item-top"
          : "primary-prediction-item"
      }
    >
      <div className="primary-prediction-rank">
        {isTop ? (
          <span
            className="prediction-trophy"
            aria-label="Top ranked prediction"
            title="Top ranked prediction"
          >
            ★
          </span>
        ) : (
          <span>
            #{index + 1}
          </span>
        )}
      </div>

      <div className="primary-prediction-content">
        <div className="primary-prediction-heading">
          <strong>
            {labelPrefix}
            {value}
          </strong>

          <span>
            {formatScore(
              item.prediction_score
            )}
          </span>
        </div>

        <ScoreBar
          score={
            item.prediction_score
          }
        />
      </div>
    </div>
  );
}


function PrimaryPredictionGroup({
  title,
  items = [],
  valueKey,
  labelPrefix = "",
}) {
  return (
    <article className="primary-prediction-card">
      <div className="prediction-category-header">
        <h3>
          {title}
        </h3>

        <span className="prediction-category-count">
          {items.length}
        </span>
      </div>

      {items.length === 0 ? (
        <div className="prediction-empty">
          No predictions.
        </div>
      ) : (
        <div className="primary-prediction-list">
          {items.map(
            (item, index) => (
              <PrimaryPredictionItem
                key={
                  `${valueKey}-` +
                  `${index}-` +
                  `${JSON.stringify(
                    item[valueKey]
                  )}`
                }
                item={item}
                index={index}
                valueKey={valueKey}
                labelPrefix={
                  labelPrefix
                }
              />
            )
          )}
        </div>
      )}
    </article>
  );
}


function TablePredictionItem({
  item,
  index,
  valueKey,
}) {
  const score =
    formatScore(
      item.prediction_score
    );


  return (
    <div
      className={
        index === 0
          ? "table-prediction-item table-prediction-item-top"
          : "table-prediction-item"
      }
    >
      <div className="table-prediction-top">
        <span className="table-prediction-rank">
          #{index + 1}
        </span>

        {score !== null && (
          <strong>
            {score}
          </strong>
        )}
      </div>

      <div className="table-prediction-value">
        {formatGroup(
          item[valueKey]
        )}
      </div>

      {score !== null && (
        <div className="table-score-track">
          <div
            className="table-score-fill"
            style={{
              width:
                `${getScoreWidth(
                  item.prediction_score
                )}%`,
            }}
          />
        </div>
      )}
    </div>
  );
}


function TablePredictionGroup({
  title,
  items = [],
  valueKey,
}) {
  return (
    <article className="table-prediction-group">
      <div className="prediction-category-header">
        <h3>
          {title}
        </h3>

        <span className="prediction-category-count">
          {items.length}
        </span>
      </div>

      {items.length === 0 ? (
        <div className="prediction-empty">
          No predictions.
        </div>
      ) : (
        <div className="table-prediction-list">
          {items.map(
            (item, index) => (
              <TablePredictionItem
                key={
                  `${valueKey}-` +
                  `${index}-` +
                  `${JSON.stringify(
                    item[valueKey]
                  )}`
                }
                item={item}
                index={index}
                valueKey={valueKey}
              />
            )
          )}
        </div>
      )}
    </article>
  );
}


function PredictionPanel({
  prediction,
  loading = false,
  onRefresh,
}) {
  if (
    loading &&
    !prediction
  ) {
    return (
      <div className="panel prediction-panel">
        <div className="panel-loading">
          Loading prediction...
        </div>
      </div>
    );
  }


  if (!prediction) {
    return (
      <div className="panel prediction-panel">
        <div className="prediction-engine-header">
          <div>
            <span className="panel-eyebrow">
              Prediction Engine V1
            </span>

            <h2>
              Latest Prediction
            </h2>
          </div>
        </div>

        <div className="prediction-no-data">
          <h3>
            No prediction available
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
            {loading
              ? "Loading..."
              : "Generate Prediction"}
          </button>
        </div>
      </div>
    );
  }


  const predictions =
    prediction.predictions || {};


  return (
    <div className="panel prediction-panel prediction-panel-v2">
      <div className="prediction-engine-header">
        <div className="prediction-engine-title">
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


        <div className="prediction-engine-actions">
          <div className="prediction-ready">
            <span />
            Ready
          </div>

          <button
            type="button"
            className="button button-secondary prediction-refresh-button"
            disabled={loading}
            onClick={onRefresh}
          >
            <span
              className={
                loading
                  ? "prediction-refresh-icon prediction-refresh-icon-loading"
                  : "prediction-refresh-icon"
              }
              aria-hidden="true"
            >
              ↻
            </span>

            {loading
              ? "Refreshing..."
              : "Refresh"}
          </button>
        </div>
      </div>


      <section className="prediction-section prediction-primary-section">
        <div className="prediction-section-heading">
          <span>
            Primary Predictions
          </span>

          <p>
            Top ranked broader
            roulette groups.
          </p>
        </div>


        <div className="primary-prediction-grid">
          <PrimaryPredictionGroup
            title="Dozens"
            items={
              predictions.dozens ||
              []
            }
            valueKey="dozen"
            labelPrefix="Dozen "
          />

          <PrimaryPredictionGroup
            title="Columns"
            items={
              predictions.columns ||
              []
            }
            valueKey="column"
            labelPrefix="Column "
          />
        </div>
      </section>


      <section className="prediction-section prediction-table-section">
        <div className="prediction-section-heading">
          <span>
            Table Predictions
          </span>

          <p>
            Ranked combinations from
            the roulette table.
          </p>
        </div>


        <div className="table-prediction-groups">
          <TablePredictionGroup
            title="Streets"
            items={
              predictions.streets ||
              []
            }
            valueKey="street"
          />

          <TablePredictionGroup
            title="Splits"
            items={
              predictions.splits ||
              []
            }
            valueKey="split"
          />

          <TablePredictionGroup
            title="Corners"
            items={
              predictions.corners ||
              []
            }
            valueKey="corner"
          />
        </div>
      </section>
    </div>
  );
}


export default PredictionPanel;