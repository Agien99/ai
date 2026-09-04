import {
  useEffect,
  useRef,
} from "react";

import RouletteNumber
  from "../common/RouletteNumber";


function SpinHistory({
  spins = [],
}) {
  const historyRef =
    useRef(null);


  useEffect(() => {
    const history =
      historyRef.current;

    if (!history) {
      return;
    }

    history.scrollTo({
      left:
        history.scrollWidth,
      behavior: "smooth",
    });
  }, [spins.length]);


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
            Swipe or scroll horizontally
            to review the session sequence.
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
        <div
          className="spin-history"
          ref={historyRef}
        >
          {spins.map((spin) => (
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
          ))}
        </div>
      )}
    </div>
  );
}


export default SpinHistory;