function LoadingState({
  message = "Loading...",
}) {
  return (
    <div className="ui-state ui-state-loading">
      <div className="loading-spinner" />

      <strong>
        {message}
      </strong>

      <span>
        Please wait while the data
        is being prepared.
      </span>
    </div>
  );
}

export default LoadingState;