import { useState } from "react";

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
    {
      length: 36,
    },
    (_, index) => index + 1
  );


function RouletteNumberInput({
  onSubmit,
  disabled = false,
}) {
  const [selected, setSelected] =
    useState(null);


  const submitNumber = async (
    number
  ) => {
    if (disabled) {
      return;
    }

    setSelected(number);

    try {
      await onSubmit(number);
    } finally {
      setSelected(null);
    }
  };


  const getButtonClass = (
    number
  ) => {
    const type =
      getNumberType(number);

    return [
      "roulette-table-number",
      `roulette-table-${type}`,
      selected === number
        ? "roulette-table-selected"
        : "",
    ]
      .filter(Boolean)
      .join(" ");
  };


  const renderNumber = (
    number
  ) => (
    <button
      key={number}
      type="button"
      disabled={disabled}
      className={
        getButtonClass(number)
      }
      onClick={() =>
        submitNumber(number)
      }
      aria-label={
        `Submit roulette number ${number}`
      }
    >
      {number}
    </button>
  );


  return (
    <div className="panel live-spin-panel">
      <div className="panel-header">
        <div>
          <span className="panel-eyebrow">
            Live Entry
          </span>

          <h2>
            Enter Observed Spin
          </h2>

          <p>
            Tap the latest roulette
            result to record the
            observed spin.
          </p>
        </div>

        {disabled && (
          <span className="spin-counter">
            Processing...
          </span>
        )}
      </div>


      <div className="roulette-table-shell">
        <div
          className={
            "roulette-table " +
            "roulette-table-desktop"
          }
        >
          <button
            type="button"
            disabled={disabled}
            className={
              getButtonClass(0) +
              " roulette-table-zero"
            }
            onClick={() =>
              submitNumber(0)
            }
            aria-label={
              "Submit roulette number 0"
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
            disabled={disabled}
            className={
              getButtonClass(0) +
              " roulette-table-zero"
            }
            onClick={() =>
              submitNumber(0)
            }
            aria-label={
              "Submit roulette number 0"
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


      <div className="live-spin-help">
        {disabled ? (
          <span>
            Recording spin and
            updating analysis...
          </span>
        ) : (
          <span>
            Select the number that
            just appeared on the
            roulette wheel.
          </span>
        )}
      </div>
    </div>
  );
}


export default RouletteNumberInput;