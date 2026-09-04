function AppHeader({
  onMenuClick,
}) {
  return (
    <header className="app-header">
      <button
        type="button"
        className="mobile-menu-button"
        onClick={onMenuClick}
        aria-label="Open navigation"
      >
        ☰
      </button>

      <div className="mobile-brand">
        <div className="mobile-brand-mark">
          ●
        </div>

        <div>
          <strong>Roulette AI</strong>

          <small>
            Predict · Analyze · Improve
          </small>
        </div>
      </div>

      <div className="header-status">
        <span className="status-dot" />
        <span>API</span>
      </div>
    </header>
  );
}

export default AppHeader;