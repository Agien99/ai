import { useState } from "react";

import AppHeader from "./components/layout/AppHeader";
import Sidebar from "./components/layout/Sidebar";
import MobileNavigation from "./components/layout/MobileNavigation";
import DashboardPage from "./pages/DashboardPage";

function App() {
  const [mobileMenuOpen, setMobileMenuOpen] =
    useState(false);

  const [activePage, setActivePage] =
    useState("dashboard");

  const handleNavigation = (page) => {
    setActivePage(page);
    setMobileMenuOpen(false);
  };

  return (
    <div className="app">
      <Sidebar
        activePage={activePage}
        onNavigate={handleNavigation}
      />

      <MobileNavigation
        open={mobileMenuOpen}
        activePage={activePage}
        onNavigate={handleNavigation}
        onClose={() =>
          setMobileMenuOpen(false)
        }
      />

      <div className="app-main">
        <AppHeader
          onMenuClick={() =>
            setMobileMenuOpen(true)
          }
        />

        <main className="app-content">
          <DashboardPage
            activePage={activePage}
          />
        </main>
      </div>
    </div>
  );
}

export default App;