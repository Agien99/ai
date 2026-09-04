function ConfirmDialog({
  open,
  title,
  message,
  confirmLabel = "Confirm",
  cancelLabel = "Cancel",
  loading = false,
  danger = false,
  onConfirm,
  onCancel,
}) {
  if (!open) {
    return null;
  }

  return (
    <div
      className="confirm-overlay"
      role="presentation"
      onMouseDown={onCancel}
    >
      <div
        className="confirm-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="confirm-title"
        onMouseDown={(
          event
        ) =>
          event.stopPropagation()
        }
      >
        <div
          className={
            danger
              ? "confirm-icon danger"
              : "confirm-icon"
          }
        >
          !
        </div>

        <div className="confirm-content">
          <h2 id="confirm-title">
            {title}
          </h2>

          <p>
            {message}
          </p>
        </div>

        <div className="confirm-actions">
          <button
            type="button"
            className="button button-secondary"
            disabled={loading}
            onClick={onCancel}
          >
            {cancelLabel}
          </button>

          <button
            type="button"
            className={
              danger
                ? "button button-danger"
                : "button button-primary"
            }
            disabled={loading}
            onClick={onConfirm}
          >
            {loading
              ? "Processing..."
              : confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}

export default ConfirmDialog;