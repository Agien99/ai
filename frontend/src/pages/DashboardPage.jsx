const pageDetails = {
  dashboard: {
    eyebrow: "Roulette AI",
    title: "Dashboard",
    description:
      "Session overview, predictions, statistics and model performance.",
  },

  "new-session": {
    eyebrow: "Session",
    title: "New Session",
    description:
      "Create a roulette observation session and enter the initial spin history.",
  },

  "active-session": {
    eyebrow: "Live Analysis",
    title: "Active Session",
    description:
      "Enter roulette results and review predictions as the session progresses.",
  },

  history: {
    eyebrow: "Historical Data",
    title: "Session History",
    description:
      "Review previous roulette sessions and their prediction performance.",
  },

  models: {
    eyebrow: "Machine Learning",
    title: "Models",
    description:
      "Compare trained models, evaluation results and the current best model.",
  },
};

function DashboardPage({
  activePage,
}) {
  const page =
    pageDetails[activePage] ||
    pageDetails.dashboard;

  return (
    <section className="page">
      <div className="page-heading">
        <div>
          <span className="page-eyebrow">
            {page.eyebrow}
          </span>

          <h1>{page.title}</h1>

          <p>{page.description}</p>
        </div>

        <span className="development-badge">
          Phase 10
        </span>
      </div>

      <div className="dashboard-placeholder">
        <div className="placeholder-content">
          <span className="placeholder-label">
            UI FOUNDATION
          </span>

          <h2>
            {page.title} interface
          </h2>

          <p>
            This area is ready for the
            Phase 10 components.
          </p>
        </div>
      </div>
    </section>
  );
}

export default DashboardPage;