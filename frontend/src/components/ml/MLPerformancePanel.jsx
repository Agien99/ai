function formatModelName(
  name
) {
  if (!name) {
    return "Unknown Model";
  }

  return name
    .replace(/^ml_/, "")
    .replaceAll("_", " ")
    .replace(
      /\b\w/g,
      (letter) =>
        letter.toUpperCase()
    );
}

function formatMetricName(
  name
) {
  if (!name) {
    return "Metric";
  }

  return name
    .replaceAll("_", " ")
    .replace(
      /\b\w/g,
      (letter) =>
        letter.toUpperCase()
    );
}

function formatMetricValue(
  value
) {
  const number =
    Number(value);

  if (
    Number.isNaN(number)
  ) {
    return value;
  }

  if (
    number >= 0 &&
    number <= 1
  ) {
    return `${(
      number * 100
    ).toFixed(1)}%`;
  }

  return number.toFixed(3);
}

function MLPerformancePanel({
  performance,
}) {
  const models =
    performance?.models || [];

  const activeModel =
    models.find(
      (item) =>
        item.model_version
          ?.is_active
    );

  if (models.length === 0) {
    return (
      <div className="panel">
        <div className="panel-header">
          <div>
            <span className="panel-eyebrow">
              Machine Learning
            </span>

            <h2>
              ML Performance
            </h2>
          </div>
        </div>

        <div className="empty-state-small">
          No trained model versions
          are available yet.
        </div>
      </div>
    );
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <div>
          <span className="panel-eyebrow">
            Machine Learning
          </span>

          <h2>
            ML Performance
          </h2>

          <p>
            Stored performance metrics
            for trained model versions.
          </p>
        </div>

        <span className="panel-count">
          {performance.model_count}
          {" "}
          models
        </span>
      </div>

      {activeModel && (
        <div className="best-model-card">
          <div>
            <span>
              CURRENT ACTIVE MODEL
            </span>

            <h3>
              {formatModelName(
                activeModel
                  .model_version
                  .model_name
              )}
            </h3>

            <p>
              Version{" "}
              {
                activeModel
                  .model_version
                  .version_number
              }
            </p>
          </div>

          <span className="best-model-badge">
            ACTIVE
          </span>
        </div>
      )}

      <div className="ml-model-grid">
        {models.map(
          (model) => {
            const version =
              model.model_version;

            const metrics =
              model.metrics || [];

            return (
              <article
                className={
                  version.is_active
                    ? "ml-model-card active"
                    : "ml-model-card"
                }
                key={
                  version
                    .model_version_id
                }
              >
                <div className="ml-model-header">
                  <div>
                    <h3>
                      {formatModelName(
                        version
                          .model_name
                      )}
                    </h3>

                    <span>
                      Version{" "}
                      {
                        version
                          .version_number
                      }
                    </span>
                  </div>

                  {version.is_active && (
                    <span className="ml-active-dot">
                      ACTIVE
                    </span>
                  )}
                </div>

                <div className="ml-model-meta">
                  <div>
                    <span>
                      Training Rows
                    </span>

                    <strong>
                      {
                        version
                          .training_row_count
                      }
                    </strong>
                  </div>

                  <div>
                    <span>
                      Sessions
                    </span>

                    <strong>
                      {
                        version
                          .training_session_count ??
                        "—"
                      }
                    </strong>
                  </div>
                </div>

                <div className="ml-metrics">
                  {metrics.length === 0 ? (
                    <span className="stats-empty">
                      No metrics
                    </span>
                  ) : (
                    metrics.map(
                      (metric) => (
                        <div
                          className="ml-metric-row"
                          key={
                            metric
                              .model_metric_id ||
                            `${
                              metric
                                .metric_scope
                            }-${
                              metric
                                .metric_name
                            }`
                          }
                        >
                          <div>
                            <span>
                              {formatMetricName(
                                metric
                                  .metric_name
                              )}
                            </span>

                            <small>
                              {
                                metric
                                  .metric_scope
                              }
                            </small>
                          </div>

                          <strong>
                            {formatMetricValue(
                              metric
                                .metric_value
                            )}
                          </strong>
                        </div>
                      )
                    )
                  )}
                </div>
              </article>
            );
          }
        )}
      </div>
    </div>
  );
}

export default MLPerformancePanel;