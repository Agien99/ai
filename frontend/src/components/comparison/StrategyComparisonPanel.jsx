const categoryLabels = {
  DOZENS: "Dozen",
  COLUMNS: "Column",
  STREETS: "Street",
  SPLITS: "Split",
  CORNERS: "Corner",
};

function formatStrategy(
  strategy
) {
  const names = {
    v1: "Prediction V1",

    baseline_random:
      "Random Baseline",

    baseline_frequency:
      "Frequency Baseline",

    baseline_hot:
      "Hot Baseline",

    baseline_cold:
      "Cold Baseline",

    ml_logistic_regression:
      "Logistic Regression",

    ml_random_forest:
      "Random Forest",

    ml_gradient_boosting:
      "Gradient Boosting",

    ml_xgboost:
      "XGBoost",
  };

  return (
    names[strategy] ||
    strategy
  );
}

function Percentage({
  value,
}) {
  const percentage =
    Math.round(
      (value || 0) * 100
    );

  return (
    <span className="comparison-rate">
      {percentage}%
    </span>
  );
}

function StrategyComparisonPanel({
  comparison,
}) {
  const strategies =
    comparison?.strategies || {};

  const entries =
    Object.entries(strategies);

  if (entries.length === 0) {
    return (
      <div className="panel">
        <div className="panel-header">
          <div>
            <span className="panel-eyebrow">
              Strategy Analysis
            </span>

            <h2>
              Strategy Comparison
            </h2>

            <p>
              Performance will appear
              after predictions have
              been evaluated.
            </p>
          </div>
        </div>

        <div className="empty-state-small">
          No evaluated strategy
          data yet.
        </div>
      </div>
    );
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <div>
          <span className="panel-eyebrow">
            Strategy Analysis
          </span>

          <h2>
            Strategy Comparison
          </h2>

          <p>
            Compare category hit
            rates across evaluated
            prediction strategies.
          </p>
        </div>

        <span className="panel-count">
          {comparison.strategy_count}
          {" "}
          strategies
        </span>
      </div>

      <div className="comparison-table-wrapper">
        <table className="comparison-table">
          <thead>
            <tr>
              <th>
                Strategy
              </th>

              <th>
                Evaluations
              </th>

              {Object.values(
                categoryLabels
              ).map(
                (label) => (
                  <th key={label}>
                    {label}
                  </th>
                )
              )}
            </tr>
          </thead>

          <tbody>
            {entries.map(
              ([
                strategyKey,
                strategy,
              ]) => (
                <tr key={strategyKey}>
                  <td>
                    <strong>
                      {formatStrategy(
                        strategyKey
                      )}
                    </strong>
                  </td>

                  <td>
                    {
                      strategy
                        .evaluation_count
                    }
                  </td>

                  {Object.keys(
                    categoryLabels
                  ).map(
                    (category) => {
                      const stats =
                        strategy
                          .categories?.[
                          category
                        ];

                      return (
                        <td
                          key={
                            category
                          }
                        >
                          <Percentage
                            value={
                              stats
                                ?.hit_rate
                            }
                          />
                        </td>
                      );
                    }
                  )}
                </tr>
              )
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default StrategyComparisonPanel;