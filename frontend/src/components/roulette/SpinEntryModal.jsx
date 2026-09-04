import RouletteNumberInput
  from "./RouletteNumberInput";


function SpinEntryModal({
  open,
  onClose,
  onSubmit,
  disabled = false,
}) {
  if (!open) {
    return null;
  }


  const handleBackdropClick = (
    event
  ) => {
    if (
      event.target ===
      event.currentTarget &&
      !disabled
    ) {
      onClose();
    }
  };


  return (
    <div
      className="spin-entry-overlay"
      role="presentation"
      onMouseDown={
        handleBackdropClick
      }
    >
      <div
        className="spin-entry-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="spin-entry-title"
      >
        <div className="spin-entry-modal-header">
          <div>
            <span className="panel-eyebrow">
              Live Entry
            </span>

            <h2 id="spin-entry-title">
              Record Spin Result
            </h2>

            <p>
              Select the number that
              just appeared on the
              roulette wheel.
            </p>
          </div>

          <button
            type="button"
            className="spin-entry-close"
            disabled={disabled}
            onClick={onClose}
            aria-label="Close spin entry"
          >
            ×
          </button>
        </div>


        <RouletteNumberInput
          onSubmit={onSubmit}
          disabled={disabled}
        />
      </div>
    </div>
  );
}


export default SpinEntryModal;