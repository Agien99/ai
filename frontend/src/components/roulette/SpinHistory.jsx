import RouletteNumber
  from "../common/RouletteNumber";


function SpinHistory({
  spins = [],
}) {
  const descendingSpins =
    [...spins].reverse();


  return (
    <div className="panel spin-history-panel">
      <div className="panel-header spin-history-header">
        <div>
          <span className="panel-eyebrow">
            Session
          </span>

          <h2>
            Spin History
          </h2>

          <p>
            Latest spin first. Swipe or
            scroll horizontally to review
            earlier results.
          </p>
        </div>

        <span className="panel-count">
          {spins.length}
          {" "}
          {spins.length === 1
            ? "Spin"
            : "Spins"}
        </span>
      </div>


      {spins.length === 0 ? (
        <div className="empty-state-small">
          No spin data available.
        </div>
      ) : (
        <div className="spin-history">
          {descendingSpins.map(
            (spin) => (
              <div
                className="history-row"
                key={
                  spin.spin_id ||
                  `${spin.spin_index}-${spin.number}`
                }
              >
                <span className="history-index">
                  #{spin.spin_index}
                </span>

                <RouletteNumber
                  number={spin.number}
                />

                <span
                  className={
                    spin.spin_type ===
                    "INITIAL"
                      ? "spin-type initial"
                      : "spin-type observed"
                  }
                >
                  {spin.spin_type}
                </span>
              </div>
            )
          )}
        </div>
      )}
    </div>
  );
}


export default SpinHistory;