const navigationItems = [
  {
    key: "dashboard",
    label: "Dashboard",
    icon: "⌂",
  },
  {
    key: "new-session",
    label: "New Session",
    icon: "+",
  },
  {
    key: "active-session",
    label: "Active Session",
    icon: "◆",
  },
  {
    key: "history",
    label: "Session History",
    icon: "◷",
  },
  {
    key: "models",
    label: "Models",
    icon: "◈",
  },
];

function Brand() {
  return (
    <div className="brand">
      <div className="brand-mark">
        <span className="brand-wheel">
          ●
        </span>
      </div>

      <div>
        <div className="brand-title">
          Roulette AI
        </div>

        <div className="brand-tagline">
          Predict · Analyze · Improve
        </div>
      </div>
    </div>
  );
}

function Sidebar({
  activePage,
  onNavigate,
}) {
  return (
    <aside className="sidebar">
      <Brand />

      <nav className="sidebar-nav">
        {navigationItems.map((item) => (
          <button
            key={item.key}
            type="button"
            className={
              activePage === item.key
                ? "nav-item nav-item-active"
                : "nav-item"
            }
            onClick={() =>
              onNavigate(item.key)
            }
          >
            <span className="nav-icon">
              {item.icon}
            </span>

            <span>{item.label}</span>
          </button>
        ))}
      </nav>
    </aside>
  );
}

export {
  Brand,
  navigationItems,
};

export default Sidebar;