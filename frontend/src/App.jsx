import {
  useState,
} from "react";

import AppHeader
  from "./components/layout/AppHeader";

import Sidebar
  from "./components/layout/Sidebar";

import MobileNavigation
  from "./components/layout/MobileNavigation";

import DashboardPage
  from "./pages/DashboardPage";

import NewSessionPage
  from "./pages/NewSessionPage";

import ActiveSessionPage
  from "./pages/ActiveSessionPage";

import SessionHistoryPage
  from "./pages/SessionHistoryPage";

import SessionHistoryDetailPage
  from "./pages/SessionHistoryDetailPage";

import {
  getSession,
  getSessionSpins,
  getSessions,
} from "./services/sessionApi";


function App() {
  const [
    mobileMenuOpen,
    setMobileMenuOpen,
  ] = useState(false);

  const [
    activePage,
    setActivePage,
  ] = useState("dashboard");

  const [
    currentSession,
    setCurrentSession,
  ] = useState(null);

  const [
    spins,
    setSpins,
  ] = useState([]);

  const [
    selectedHistorySessionId,
    setSelectedHistorySessionId,
  ] = useState(null);

  const [
    resumeLoading,
    setResumeLoading,
  ] = useState(false);


  const recoverLatestActiveSession =
    async () => {
      const sessions =
        await getSessions();


      const activeSessions =
        (sessions || [])
          .filter(
            (session) =>
              session.status ===
              "ACTIVE"
          );


      if (
        activeSessions.length === 0
      ) {
        setCurrentSession(
          null
        );

        setSpins([]);

        return false;
      }


      /*
       * getSessions() should normally
       * return sessions in the backend's
       * normal ordering.
       *
       * We still explicitly sort the
       * ACTIVE sessions so the most
       * recently started session wins.
       */
      const sortedActiveSessions =
        [...activeSessions].sort(
          (a, b) => {
            const aTime =
              new Date(
                a.started_at ||
                a.created_at ||
                0
              ).getTime();

            const bTime =
              new Date(
                b.started_at ||
                b.created_at ||
                0
              ).getTime();

            return bTime - aTime;
          }
        );


      const latestActiveSession =
        sortedActiveSessions[0];


      const [
        sessionData,
        spinData,
      ] = await Promise.all([
        getSession(
          latestActiveSession
            .session_id
        ),

        getSessionSpins(
          latestActiveSession
            .session_id
        ),
      ]);


      setCurrentSession(
        sessionData
      );

      setSpins(
        spinData
      );

      setSelectedHistorySessionId(
        null
      );


      return true;
    };


  const handleNavigation =
    async (page) => {
      setMobileMenuOpen(
        false
      );


      /*
       * Active Session is special:
       *
       * If React already knows about an
       * ACTIVE session, simply open it.
       *
       * Otherwise ask the backend for
       * the latest ACTIVE session.
       */
      if (
        page ===
        "active-session"
      ) {
        if (
          currentSession?.status ===
          "ACTIVE"
        ) {
          setActivePage(
            "active-session"
          );

          return;
        }


        if (resumeLoading) {
          return;
        }


        setResumeLoading(
          true
        );


        try {
          await recoverLatestActiveSession();
        } catch (requestError) {
          console.error(
            "Unable to recover active session:",
            requestError
          );

          setCurrentSession(
            null
          );

          setSpins([]);
        } finally {
          setResumeLoading(
            false
          );
        }


        setActivePage(
          "active-session"
        );

        return;
      }


      setActivePage(page);
    };


  const handleSessionStarted = (
    session,
    initialSpins
  ) => {
    setCurrentSession(
      session
    );

    setSpins(
      initialSpins
    );

    setSelectedHistorySessionId(
      null
    );

    setActivePage(
      "active-session"
    );
  };


  const handleSpinAdded = (
    spin
  ) => {
    setSpins(
      (current) => [
        ...current,
        spin,
      ]
    );
  };


  const handleSessionEnded = (
    endedSession
  ) => {
    setCurrentSession(
      endedSession
    );

    setSelectedHistorySessionId(
      endedSession.session_id
    );

    setActivePage(
      "history-detail"
    );
  };


  const handleOpenHistorySession = (
    sessionId
  ) => {
    setSelectedHistorySessionId(
      sessionId
    );

    setActivePage(
      "history-detail"
    );
  };


  const handleContinueSession =
    async (sessionId) => {
      if (resumeLoading) {
        return;
      }

      setResumeLoading(
        true
      );

      try {
        const [
          sessionData,
          spinData,
        ] = await Promise.all([
          getSession(
            sessionId
          ),

          getSessionSpins(
            sessionId
          ),
        ]);

        setCurrentSession(
          sessionData
        );

        setSpins(
          spinData
        );

        setSelectedHistorySessionId(
          null
        );

        setActivePage(
          "active-session"
        );
      } finally {
        setResumeLoading(
          false
        );
      }
    };


  const renderPage = () => {
    switch (activePage) {
      case "new-session":
        return (
          <NewSessionPage
            onSessionStarted={
              handleSessionStarted
            }
          />
        );


      case "active-session":
        return (
          <ActiveSessionPage
            session={
              currentSession?.status ===
              "ACTIVE"
                ? currentSession
                : null
            }
            spins={
              currentSession?.status ===
              "ACTIVE"
                ? spins
                : []
            }
            onSpinAdded={
              handleSpinAdded
            }
            onNewSession={() =>
              handleNavigation(
                "new-session"
              )
            }
            onSessionEnded={
              handleSessionEnded
            }
          />
        );


      case "history":
        return (
          <SessionHistoryPage
            onOpenSession={
              handleOpenHistorySession
            }
          />
        );


      case "history-detail":
        if (
          !selectedHistorySessionId
        ) {
          return (
            <SessionHistoryPage
              onOpenSession={
                handleOpenHistorySession
              }
            />
          );
        }

        return (
          <SessionHistoryDetailPage
            sessionId={
              selectedHistorySessionId
            }
            onBack={() =>
              handleNavigation(
                "history"
              )
            }
            onContinueSession={
              handleContinueSession
            }
            resumeLoading={
              resumeLoading
            }
          />
        );


      case "models":
        return (
          <ComingSoonPage
            eyebrow="Machine Learning"
            title="Models"
          />
        );


      default:
        return (
          <DashboardPage
            session={
              currentSession
            }
            spins={
              spins
            }
            onNewSession={() =>
              handleNavigation(
                "new-session"
              )
            }
            onOpenSession={() =>
              handleNavigation(
                "active-session"
              )
            }
          />
        );
    }
  };


  return (
    <div className="app">
      <Sidebar
        activePage={
          activePage
        }
        onNavigate={
          handleNavigation
        }
      />

      <MobileNavigation
        open={
          mobileMenuOpen
        }
        activePage={
          activePage
        }
        onNavigate={
          handleNavigation
        }
        onClose={() =>
          setMobileMenuOpen(
            false
          )
        }
      />

      <div className="app-main">
        <AppHeader
          onMenuClick={() =>
            setMobileMenuOpen(
              true
            )
          }
        />

        <main className="app-content">
          {renderPage()}
        </main>
      </div>
    </div>
  );
}


function ComingSoonPage({
  eyebrow,
  title,
}) {
  return (
    <section className="page">
      <div className="page-heading">
        <div>
          <span className="page-eyebrow">
            {eyebrow}
          </span>

          <h1>
            {title}
          </h1>

          <p>
            This interface will be
            implemented in a later
            Phase 10 batch.
          </p>
        </div>
      </div>

      <div className="dashboard-placeholder">
        <div className="placeholder-content">
          <span className="placeholder-label">
            COMING SOON
          </span>

          <h2>
            {title}
          </h2>
        </div>
      </div>
    </section>
  );
}


export default App;