import RouletteNumber
  from "../common/RouletteNumber";

import {
  getNumberType,
} from "../../utils/roulette";


const rouletteRows = [
  [
    3, 6, 9, 12,
    15, 18, 21, 24,
    27, 30, 33, 36,
  ],
  [
    2, 5, 8, 11,
    14, 17, 20, 23,
    26, 29, 32, 35,
  ],
  [
    1, 4, 7, 10,
    13, 16, 19, 22,
    25, 28, 31, 34,
  ],
];

const mobileRouletteNumbers =
  Array.from(
    { length: 36 },
    (_, index) => index + 1
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


  const renderNumber = (
    number
  ) => {
    const type =
      getNumberType(number);

    return (
      <button
        type="button"
        key={number}
        className={
          "roulette-table-number " +
          `roulette-table-${type}`
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
  };


  return (
    <div className="panel initial-spin-panel">
      <div className="panel-header">
        <div>
          <span className="panel-eyebrow">
            Starting Data
          </span>

          <h2>
            Initial Spin History
          </h2>

          <p>
            Click the numbers below in
            chronological order from
            oldest to newest. A minimum
            of 10 spins is required.
          </p>
        </div>

        <div
          className={
            spins.length >= 10
              ? "spin-counter valid"
              : "spin-counter"
          }
        >
          {spins.length}{" "}
          {spins.length === 1
            ? "spin"
            : "spins"}{" "}
          selected
        </div>
      </div>


      <div className="roulette-table-shell">
        <div className="roulette-table roulette-table-desktop">
          <button
            type="button"
            className={
              "roulette-table-number " +
              "roulette-table-zero"
            }
            disabled={disabled}
            onClick={() =>
              addNumber(0)
            }
          >
            0
          </button>

          <div className="roulette-table-main">
            {rouletteRows.map(
              (row, rowIndex) => (
                <div
                  className="roulette-table-row"
                  key={rowIndex}
                >
                  {row.map(
                    renderNumber
                  )}
                </div>
              )
            )}
          </div>
        </div>


        <div className="roulette-table-mobile">
          <button
            type="button"
            className={
              "roulette-table-number " +
              "roulette-table-zero"
            }
            disabled={disabled}
            onClick={() =>
              addNumber(0)
            }
          >
            0
          </button>

          <div className="roulette-mobile-numbers">
            {mobileRouletteNumbers.map(
              renderNumber
            )}
          </div>
        </div>
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
            <strong>
              No spins selected yet.
            </strong>

            <span>
              Click numbers on the
              roulette table above.
            </span>
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