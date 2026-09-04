import Brand
  from "./Brand";

import {
  navigationItems,
} from "./navigationConfig";

function Sidebar({
  activePage,
  onNavigate,
}) {
  return (
    <aside className="sidebar">
      <Brand />

      <nav className="sidebar-nav">
        {navigationItems.map(
          (item) => (
            <button
              key={item.key}
              type="button"
              className={
                activePage ===
                item.key
                  ? "nav-item nav-item-active"
                  : "nav-item"
              }
              onClick={() =>
                onNavigate(
                  item.key
                )
              }
            >
              <span className="nav-icon">
                {item.icon}
              </span>

              <span>
                {item.label}
              </span>
            </button>
          )
        )}
      </nav>
    </aside>
  );
}

export default Sidebar;