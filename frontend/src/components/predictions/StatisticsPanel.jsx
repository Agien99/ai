import RouletteNumber
  from "../common/RouletteNumber";

function NumberList({
  title,
  numbers = [],
}) {
  return (
    <div className="stats-number-section">
      <h3>{title}</h3>

      <div className="stats-number-list">
        {numbers.length === 0 ? (
          <span className="stats-empty">
            No data
          </span>
        ) : (
          numbers.map(
            (item) => (
              <div
                className="stats-number-item"
                key={item.number}
              >
                <RouletteNumber
                  number={item.number}
                />

                <span>
                  {item.frequency}×
                </span>
              </div>
            )
          )
        )}
      </div>
    </div>
  );
}

function FrequencyBars({
  data = {},
  prefix,
}) {
  const entries =
    Object.entries(data);

  const max =
    Math.max(
      1,
      ...entries.map(
        ([, value]) => value
      )
    );

  return (
    <div className="frequency-bars">
      {entries.map(
        ([key, value]) => {
          const label =
            key.replace(
              `${prefix}_`,
              ""
            );

          const width =
            (value / max) * 100;

          return (
            <div
              className="frequency-row"
              key={key}
            >
              <span>
                {prefix === "dozen"
                  ? `Dozen ${label}`
                  : `Column ${label}`}
              </span>

              <div className="frequency-track">
                <div
                  className="frequency-fill"
                  style={{
                    width:
                      `${width}%`,
                  }}
                />
              </div>

              <strong>
                {value}
              </strong>
            </div>
          );
        }
      )}
    </div>
  );
}

function NumberFrequency({
  frequency = {},
}) {
  const entries =
    Object.entries(frequency)
      .map(
        ([number, count]) => ({
          number: Number(number),
          count,
        })
      )
      .filter(
        (item) => item.count > 0
      )
      .sort(
        (a, b) =>
          b.count - a.count ||
          a.number - b.number
      );

  const max =
    Math.max(
      1,
      ...entries.map(
        (item) => item.count
      )
    );

  return (
    <div className="number-frequency">
      {entries.length === 0 ? (
        <div className="stats-empty">
          No frequency data.
        </div>
      ) : (
        entries.map((item) => (
          <div
            className="number-frequency-row"
            key={item.number}
          >
            <RouletteNumber
              number={item.number}
            />

            <div className="number-frequency-track">
              <div
                className="number-frequency-fill"
                style={{
                  width:
                    `${
                      (
                        item.count /
                        max
                      ) * 100
                    }%`,
                }}
              />
            </div>

            <strong>
              {item.count}
            </strong>
          </div>
        ))
      )}
    </div>
  );
}

function StatisticsPanel({
  statistics,
}) {
  const stats =
    statistics?.statistics;

  if (!stats) {
    return (
      <div className="panel">
        <div className="panel-header">
          <div>
            <span className="panel-eyebrow">
              Statistics
            </span>

            <h2>
              Session Statistics
            </h2>
          </div>
        </div>

        <div className="empty-state-small">
          Statistics are not
          available yet.
        </div>
      </div>
    );
  }

  return (
    <div className="statistics-layout">
      <div className="panel">
        <div className="panel-header">
          <div>
            <span className="panel-eyebrow">
              Current Session
            </span>

            <h2>
              Hot / Cold Numbers
            </h2>
          </div>

          <span className="panel-count">
            {statistics.spin_count} spins
          </span>
        </div>

        <div className="hot-cold-grid">
          <NumberList
            title="Hot Numbers"
            numbers={
              stats.hot_numbers
            }
          />

          <NumberList
            title="Cold Numbers"
            numbers={
              stats.cold_numbers
            }
          />
        </div>
      </div>

      <div className="panel">
        <div className="panel-header">
          <div>
            <span className="panel-eyebrow">
              Groups
            </span>

            <h2>
              Dozen / Column
            </h2>
          </div>
        </div>

        <div className="group-frequency-grid">
          <div>
            <h3>
              Dozens
            </h3>

            <FrequencyBars
              data={
                stats.dozen_frequency
              }
              prefix="dozen"
            />
          </div>

          <div>
            <h3>
              Columns
            </h3>

            <FrequencyBars
              data={
                stats.column_frequency
              }
              prefix="column"
            />
          </div>
        </div>
      </div>

      <div className="panel stats-frequency-panel">
        <div className="panel-header">
          <div>
            <span className="panel-eyebrow">
              Distribution
            </span>

            <h2>
              Number Frequency
            </h2>

            <p>
              Number appearances
              during the current
              session.
            </p>
          </div>
        </div>

        <NumberFrequency
          frequency={
            stats.number_frequency
          }
        />
      </div>
    </div>
  );
}

export default StatisticsPanel;