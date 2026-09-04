import Brand
  from "./Brand";

import {
  navigationItems,
} from "./navigationConfig";

function MobileNavigation({
  open,
  activePage,
  onNavigate,
  onClose,
}) {
  if (!open) {
    return null;
  }

  return (
    <>
      <button
        type="button"
        className="mobile-nav-backdrop"
        onClick={onClose}
        aria-label="Close navigation"
      />

      <aside className="mobile-nav">
        <div className="mobile-nav-header">
          <Brand />

          <button
            type="button"
            className="mobile-nav-close"
            onClick={onClose}
            aria-label="Close navigation"
          >
            ×
          </button>
        </div>

        <nav className="sidebar-nav">
          {navigationItems.map(
            (item) => (
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
            )
          )}
        </nav>
      </aside>
    </>
  );
}

export default MobileNavigation;