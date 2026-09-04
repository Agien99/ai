function ErrorState({
  message =
    "Something went wrong.",
  onRetry,
}) {
  return (
    <div className="ui-state ui-state-error">
      <div className="ui-state-icon">
        !
      </div>

      <strong>
        Unable to Load Data
      </strong>

      <span>
        {message}
      </span>

      {onRetry && (
        <button
          type="button"
          className="button button-secondary"
          onClick={onRetry}
        >
          Try Again
        </button>
      )}
    </div>
  );
}

export default ErrorState;