import { useState } from "react";

import {
  getNumberType,
} from "../common/RouletteNumber";

const numbers = Array.from(
  {
    length: 37,
  },
  (_, index) => index
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
    setSelected(number);

    try {
      await onSubmit(number);
    } finally {
      setSelected(null);
    }
  };

  return (
    <div className="panel">
      <div className="panel-header">
        <div>
          <span className="panel-eyebrow">
            Live Entry
          </span>

          <h2>
            Enter Spin Result
          </h2>

          <p>
            Tap the latest roulette
            result.
          </p>
        </div>
      </div>

      <div className="roulette-grid">
        {numbers.map((number) => {
          const type =
            getNumberType(number);

          return (
            <button
              key={number}
              type="button"
              disabled={disabled}
              className={
                `roulette-grid-number ` +
                `roulette-grid-${type} ` +
                (
                  selected === number
                    ? "roulette-grid-selected"
                    : ""
                )
              }
              onClick={() =>
                submitNumber(number)
              }
            >
              {number}
            </button>
          );
        })}
      </div>
    </div>
  );
}

export default RouletteNumberInput;