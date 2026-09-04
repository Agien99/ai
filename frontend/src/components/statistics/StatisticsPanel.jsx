import RouletteNumber
  from "../common/RouletteNumber";


function NumberGroup({
  title,
  numbers = [],
}) {
  return (
    <div className="stats-card">
      <span className="stats-card-label">
        {title}
      </span>

      {numbers.length === 0 ? (
        <div className="stats-empty">
          No data
        </div>
      ) : (
        <div className="stats-number-grid">
          {numbers.map(
            (item) => (
              <div
                className="stats-number-chip"
                key={item.number}
              >
                <RouletteNumber
                  number={item.number}
                  size="small"
                />

                <span className="stats-number-count">
                  {item.frequency}x
                </span>
              </div>
            )
          )}
        </div>
      )}
    </div>
  );
}


function FrequencyCard({
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
    <div className="stats-card">
      <span className="stats-card-label">
        {title}
      </span>

      {entries.length === 0 ? (
        <div className="stats-empty">
          No data
        </div>
      ) : (
        <div className="stats-frequency-list">
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
                  className="stats-frequency-row"
                  key={key}
                >
                  <div className="stats-frequency-header">
                    <span>
                      {key}
                    </span>

                    <strong>
                      {numericValue}
                    </strong>
                  </div>

                  <div className="stats-frequency-track">
                    <div
                      className="stats-frequency-fill"
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
          a.number -
          b.number
      );

  return (
    <div className="stats-card stats-number-frequency-card">
      <span className="stats-card-label">
        Number Frequency
      </span>

      {entries.length === 0 ? (
        <div className="stats-empty">
          No data
        </div>
      ) : (
        <div className="stats-frequency-grid">
          {entries.map(
            (item) => (
              <div
                className="stats-frequency-number"
                key={item.number}
              >
                <RouletteNumber
                  number={item.number}
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

  const spinCount =
    statistics?.spin_count ??
    data.spin_count ??
    0;

  if (!statistics) {
    return (
      <div className="panel">
        <div className="panel-header">
          <div>
            <span className="panel-eyebrow">
              SESSION ANALYSIS
            </span>

            <h2>
              Statistics
            </h2>
          </div>
        </div>

        <div className="stats-empty-panel">
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
            SESSION ANALYSIS
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
          {spinCount} spins
        </span>
      </div>


      <div className="stats-grid stats-grid-two">
        <NumberGroup
          title="Hot Numbers"
          numbers={
            data.hot_numbers ||
            []
          }
        />

        <NumberGroup
          title="Cold Numbers"
          numbers={
            data.cold_numbers ||
            []
          }
        />
      </div>


      <div className="stats-grid stats-grid-two">
        <FrequencyCard
          title="Dozen Frequency"
          data={
            data.dozen_frequency ||
            {}
          }
        />

        <FrequencyCard
          title="Column Frequency"
          data={
            data.column_frequency ||
            {}
          }
        />
      </div>


      <NumberFrequency
        frequency={
          data.number_frequency ||
          {}
        }
      />
    </div>
  );
}


export default StatisticsPanel;