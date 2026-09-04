function EmptyState({
  title = "No Data",
  message =
    "There is currently nothing to display.",
  actionLabel,
  onAction,
}) {
  return (
    <div className="ui-state ui-state-empty">
      <div className="ui-state-icon">
        —
      </div>

      <strong>
        {title}
      </strong>

      <span>
        {message}
      </span>

      {actionLabel &&
        onAction && (
          <button
            type="button"
            className="button button-primary"
            onClick={onAction}
          >
            {actionLabel}
          </button>
        )}
    </div>
  );
}

export default EmptyState;