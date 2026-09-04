import { useState } from "react";

import RouletteNumber
  from "../common/RouletteNumber";

function InitialSpinInput({
  spins,
  onChange,
  disabled = false,
}) {
  const [value, setValue] =
    useState("");

  const addNumber = () => {
    const number = Number(value);

    if (
      value === "" ||
      !Number.isInteger(number) ||
      number < 0 ||
      number > 36 ||
      spins.length >= 15
    ) {
      return;
    }

    onChange([
      ...spins,
      number,
    ]);

    setValue("");
  };

  const removeLast = () => {
    onChange(
      spins.slice(0, -1)
    );
  };

  const clearAll = () => {
    onChange([]);
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      addNumber();
    }
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
            Enter 10–15 recent
            roulette results in
            chronological order.
          </p>
        </div>

        <div
          className={
            spins.length >= 10
              ? "spin-counter valid"
              : "spin-counter"
          }
        >
          {spins.length} / 15
        </div>
      </div>

      <div className="initial-entry-row">
        <input
          className="number-input"
          type="number"
          min="0"
          max="36"
          value={value}
          disabled={disabled}
          placeholder="0 - 36"
          onChange={(event) =>
            setValue(
              event.target.value
            )
          }
          onKeyDown={handleKeyDown}
        />

        <button
          type="button"
          className="button button-primary"
          disabled={
            disabled ||
            spins.length >= 15
          }
          onClick={addNumber}
        >
          Add Spin
        </button>
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
            You may add up to{" "}
            {15 - spins.length} more.
          </span>
        )}
      </div>

      <div className="initial-spin-list">
        {spins.length === 0 ? (
          <div className="empty-inline">
            No spins entered yet.
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

      {spins.length > 0 && (
        <div className="initial-actions">
          <button
            type="button"
            className="button button-secondary"
            disabled={disabled}
            onClick={removeLast}
          >
            Remove Last
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
  );
}

export default InitialSpinInput;