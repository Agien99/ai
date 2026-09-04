import RouletteNumber
  from "../common/RouletteNumber";

function NumberList({
  title,
  numbers = [],
}) {
  return (
    <div className="statistics-list-card">
      <span className="statistics-label">
        {title}
      </span>

      {numbers.length === 0 ? (
        <span className="stats-empty">
          No data
        </span>
      ) : (
        <div className="statistics-number-list">
          {numbers.map(
            (item) => (
              <div
                className="statistics-number-item"
                key={item.number}
              >
                <RouletteNumber
                  number={
                    item.number
                  }
                  size="small"
                />

                <span>
                  {item.frequency}
                </span>
              </div>
            )
          )}
        </div>
      )}
    </div>
  );
}


function FrequencyBars({
  title,
  data = {},
}) {
  const entries =
    Object.entries(data);

  const maxValue =
    Math.max(
      1,
      ...entries.map(
        ([, value]) =>
          Number(value) || 0
      )
    );

  return (
    <div className="statistics-list-card">
      <span className="statistics-label">
        {title}
      </span>

      {entries.length === 0 ? (
        <span className="stats-empty">
          No data
        </span>
      ) : (
        <div className="frequency-bars">
          {entries.map(
            ([key, value]) => {
              const numericValue =
                Number(value) || 0;

              const width =
                Math.round(
                  (
                    numericValue /
                    maxValue
                  ) *
                  100
                );

              return (
                <div
                  className="frequency-row"
                  key={key}
                >
                  <div className="frequency-row-header">
                    <span>
                      {key}
                    </span>

                    <strong>
                      {numericValue}
                    </strong>
                  </div>

                  <div className="frequency-track">
                    <div
                      className="frequency-fill"
                      style={{
                        width:
                          `${width}%`,
                      }}
                    />
                  </div>
                </div>
              );
            }
          )}
        </div>
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
          number:
            Number(number),

          count:
            Number(count),
        })
      )
      .sort(
        (a, b) =>
          b.count -
          a.count
      );

  return (
    <div className="statistics-list-card">
      <span className="statistics-label">
        Number Frequency
      </span>

      {entries.length === 0 ? (
        <span className="stats-empty">
          No data
        </span>
      ) : (
        <div className="number-frequency-grid">
          {entries.map(
            (item) => (
              <div
                className="number-frequency-item"
                key={item.number}
              >
                <RouletteNumber
                  number={
                    item.number
                  }
                  size="small"
                />

                <strong>
                  {item.count}
                </strong>
              </div>
            )
          )}
        </div>
      )}
    </div>
  );
}


function StatisticsPanel({
  statistics,
}) {
  const data =
    statistics?.statistics ||
    {};

  if (!statistics) {
    return (
      <div className="panel">
        <div className="panel-header">
          <div>
            <span className="panel-eyebrow">
              Session Analysis
            </span>

            <h2>
              Statistics
            </h2>
          </div>
        </div>

        <div className="empty-state-small">
          No statistics available.
        </div>
      </div>
    );
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <div>
          <span className="panel-eyebrow">
            Session Analysis
          </span>

          <h2>
            Statistics
          </h2>

          <p>
            Frequency and activity
            analysis for the current
            session.
          </p>
        </div>

        <span className="panel-count">
          {
            data.spin_count ??
            statistics.spin_count ??
            0
          }
          {" "}
          spins
        </span>
      </div>


      <div className="statistics-top-grid">
        <NumberList
          title="Hot Numbers"
          numbers={
            data.hot_numbers ||
            []
          }
        />

        <NumberList
          title="Cold Numbers"
          numbers={
            data.cold_numbers ||
            []
          }
        />
      </div>


      <div className="statistics-group-grid">
        <FrequencyBars
          title="Dozen Frequency"
          data={
            data.dozen_frequency ||
            {}
          }
        />

        <FrequencyBars
          title="Column Frequency"
          data={
            data.column_frequency ||
            {}
          }
        />
      </div>


      <div className="statistics-number-section">
        <NumberFrequency
          frequency={
            data.number_frequency ||
            {}
          }
        />
      </div>
    </div>
  );
}


export default StatisticsPanel;