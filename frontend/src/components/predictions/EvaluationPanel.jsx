const categories = [
  {
    key: "DOZENS",
    label: "Dozen",
  },
  {
    key: "COLUMNS",
    label: "Column",
  },
  {
    key: "STREETS",
    label: "Street",
  },
  {
    key: "SPLITS",
    label: "Split",
  },
  {
    key: "CORNERS",
    label: "Corner",
  },
];

function EvaluationPanel({
  evaluation,
}) {
  const evaluations =
    evaluation?.evaluations || [];

  const latest =
    evaluations.length > 0
      ? evaluations[
          evaluations.length - 1
        ]
      : null;

  if (!latest) {
    return (
      <div className="panel">
        <div className="panel-header">
          <div>
            <span className="panel-eyebrow">
              Prediction Accuracy
            </span>

            <h2>
              HIT / MISS
            </h2>
          </div>
        </div>

        <div className="empty-state-small">
          Enter a new spin after a
          prediction to receive an
          evaluation.
        </div>
      </div>
    );
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <div>
          <span className="panel-eyebrow">
            Prediction Accuracy
          </span>

          <h2>
            HIT / MISS
          </h2>

          <p>
            Result for predicted spin{" "}
            #
            {
              latest
                .prediction_for_spin_index
            }
          </p>
        </div>

        <span className="panel-count">
          {
            evaluation
              .evaluation_count
          }{" "}
          evaluated
        </span>
      </div>

      <div className="evaluation-grid">
        {categories.map(
          (category) => {
            const result =
              latest.categories?.[
                category.key
              ];

            if (!result) {
              return null;
            }

            return (
              <div
                className={
                  result.is_hit
                    ? "evaluation-card hit"
                    : "evaluation-card miss"
                }
                key={category.key}
              >
                <span>
                  {category.label}
                </span>

                <strong>
                  {result.is_hit
                    ? "HIT"
                    : "MISS"}
                </strong>
              </div>
            );
          }
        )}
      </div>
    </div>
  );
}

export default EvaluationPanel;