import RouletteNumber
  from "../common/RouletteNumber";

import {
  getNumberType,
} from "../../utils/roulette";


const rouletteNumbers =
  Array.from(
    { length: 37 },
    (_, index) => index
  );


function InitialSpinInput({
  spins,
  onChange,
  disabled = false,
}) {
  const addNumber = (
    number
  ) => {
    if (disabled) {
      return;
    }

    onChange([
      ...spins,
      number,
    ]);
  };


  const removeLast = () => {
    if (
      disabled ||
      spins.length === 0
    ) {
      return;
    }

    onChange(
      spins.slice(0, -1)
    );
  };


  const clearAll = () => {
    if (
      disabled ||
      spins.length === 0
    ) {
      return;
    }

    onChange([]);
  };


  return (
    <div className="panel">
      <div className="panel-header">
        <div>
          <span className="panel-eyebrow">
            Starting Data
          </span>

          <h2>
            Initial Spin History
          </h2>

          <p>
            Click the recent roulette
            results in chronological
            order. A minimum of 10
            spins is required.
          </p>
        </div>

        <div
          className={
            spins.length >= 10
              ? "spin-counter valid"
              : "spin-counter"
          }
        >
          {spins.length} spins
        </div>
      </div>


      <div className="initial-number-grid">
        {rouletteNumbers.map(
          (number) => {
            const type =
              getNumberType(number);

            return (
              <button
                type="button"
                key={number}
                className={
                  `roulette-grid-number ` +
                  `roulette-grid-${type}`
                }
                disabled={disabled}
                onClick={() =>
                  addNumber(number)
                }
                aria-label={
                  `Add roulette number ${number}`
                }
              >
                {number}
              </button>
            );
          }
        )}
      </div>


      <div className="initial-help">
        {spins.length < 10 ? (
          <span>
            Add{" "}
            <strong>
              {10 - spins.length}
            </strong>{" "}
            more spin
            {10 - spins.length === 1
              ? ""
              : "s"}{" "}
            to continue.
          </span>
        ) : (
          <span className="valid-text">
            Ready to start session.
            You may continue adding
            more history if available.
          </span>
        )}
      </div>


      <div className="initial-history-header">
        <div>
          <span className="stats-card-label">
            Selected History
          </span>

          <p>
            Oldest to newest
          </p>
        </div>

        {spins.length > 0 && (
          <div className="initial-actions">
            <button
              type="button"
              className="button button-secondary"
              disabled={disabled}
              onClick={removeLast}
            >
              Undo Last
            </button>

            <button
              type="button"
              className="button button-danger-ghost"
              disabled={disabled}
              onClick={clearAll}
            >
              Clear All
            </button>
          </div>
        )}
      </div>


      <div className="initial-spin-list">
        {spins.length === 0 ? (
          <div className="empty-inline">
            No spins selected yet.
          </div>
        ) : (
          spins.map(
            (number, index) => (
              <div
                className="initial-spin-item"
                key={`${index}-${number}`}
              >
                <span className="spin-position">
                  {index + 1}
                </span>

                <RouletteNumber
                  number={number}
                />
              </div>
            )
          )
        )}
      </div>
    </div>
  );
}


export default InitialSpinInput;