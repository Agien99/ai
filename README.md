# Roulette AI Experiment

A learning project focused on building a session-based AI/ML system for
analyzing European Roulette results and generating ranked betting
predictions.

The main goal of this project is not to guarantee roulette outcomes, but
to learn and experiment with:

-   Python
-   Data processing
-   Statistical analysis
-   Feature engineering
-   Machine learning
-   Model evaluation
-   API development
-   Supabase integration
-   React frontend integration

## Roulette Type

This project currently targets:

-   European Roulette
-   Numbers: `0-36`
-   Single zero

## Prediction Targets

For every next spin, the system is planned to generate:

-   2 possible Dozens
-   2 possible Columns
-   5 possible Corner bets
-   12 possible Split bets
-   6 possible Street bets

Predictions can be ranked using the statistical Prediction Engine V1 and
the implemented machine-learning models.

## Session-Based Design

Roulette observations are handled as separate sessions.

Example:

``` text
Session A
5:00 PM - 9:00 PM

Session B
11:00 PM - 1:00 AM
```

A new session is started when there is a gap where roulette spins were
not observed.

Each session begins with approximately 10-15 recent roulette results.

The system will then:

``` text
Initial spin history
        ↓
Analyze current session
        ↓
Generate prediction
        ↓
Next actual spin entered
        ↓
Evaluate previous prediction
        ↓
Update session statistics
        ↓
Generate next prediction
```

Previous sessions are planned to remain stored in Supabase for
evaluation and long-term ML experimentation, while each new session
keeps its own short-term state.

## Planned Architecture

``` text
React Frontend
agien99.github.io/ai/
        │
        │ REST API
        ▼
Python Backend
FastAPI
        │
        ├── Roulette Engine
        ├── Session Engine
        ├── Statistics
        ├── Feature Engineering
        ├── Prediction Engine
        └── Machine Learning
        │
        ▼
Supabase
        ├── Sessions
        ├── Spins
        ├── Predictions
        └── Model Evaluation
```

The project will be developed locally first before deployment is
considered.

## Development Phases

### Phase 1 - Roulette Domain Engine

Goal:

Make Python understand the European Roulette table and its betting
structures.

Planned steps:

1.  Create Python repository and project structure (COMPLETED)
2.  Define valid roulette numbers (COMPLETED)
3.  Implement Dozens (COMPLETED)
4.  Implement Columns (COMPLETED)
5.  Implement Streets (COMPLETED)
6.  Implement Splits (COMPLETED)
7.  Implement Corners (COMPLETED)
8.  Add validation (COMPLETED)
9.  Add basic tests (COMPLETED)

------------------------------------------------------------------------

### Phase 2 - Session Engine

Goal: Create isolated roulette observation sessions.

Steps:

1.  Define RouletteSession model (COMPLETED)
2.  Start session with 10-15 initial spins (COMPLETED)
3.  Add new spins sequentially (COMPLETED)
4.  Maintain spin sequence/order (COMPLETED)
5.  Track session state and metadata (COMPLETED)
6.  End/close session (COMPLETED)
7.  Start fresh independent session (COMPLETED)
8.  Session validation and edge cases (COMPLETED)
9.  Automated session tests (COMPLETED)

------------------------------------------------------------------------

### Phase 3 - Statistical Analysis

Goal:

Extract useful features from the current roulette session.

1.  Create Statistics Engine (COMPLETED)
2.  Number Frequency (COMPLETED)
3.  Recent-Window Frequency (COMPLETED)
4.  Spins Since Last Appearance (COMPLETED)
5.  Hot & Cold Numbers (COMPLETED)
6.  Dozen Frequency (COMPLETED)
7.  Column Frequency (COMPLETED)
8.  Street Activity (COMPLETED)
9.  Split Activity (COMPLETED)
10. Corner Activity (COMPLETED)
11. Combined Session Statistics (COMPLETED)
12. Validation & Edge Cases (COMPLETED)
13. Automated Statistical Tests (COMPLETED)

------------------------------------------------------------------------

### Phase 4 - Prediction Engine V1

Goal:

Generate ranked predictions without machine learning first.

1.  Create Prediction Engine (COMPLETED)
2.  Define Scoring Components (COMPLETED)
3.  Score Dozens (COMPLETED)
4.  Score Columns (COMPLETED)
5.  Score Streets (COMPLETED)
6.  Score Splits (COMPLETED)
7.  Score Corners (COMPLETED)
8.  Rank Predictions (COMPLETED)
9.  Generate Final Prediction Set (COMPLETED)
10. Prediction Output Structure (COMPLETED)
11. Validation & Edge Cases (COMPLETED)
12. Automated Prediction Tests (COMPLETED)
13. Baseline Evaluation Preparation (COMPLETED)

Expected output:

``` text
2 Dozens
2 Columns
5 Corners
12 Splits
6 Streets
```

This phase will create the baseline prediction engine.

------------------------------------------------------------------------

### Phase 5 - Prediction Evaluation

Goal:

Measure whether previous predictions hit the next roulette result.

1.  Create Evaluation Engine (COMPLETED)
2.  Define Prediction Evaluation Record (COMPLETED)
3.  Evaluate Dozen Predictions (COMPLETED)
4.  Evaluate Column Predictions (COMPLETED)
5.  Evaluate Street Predictions (COMPLETED)
6.  Evaluate Split Predictions (COMPLETED)
7.  Evaluate Corner Predictions (COMPLETED)
8.  Evaluate Complete Prediction Set (COMPLETED)
9.  Track HIT / MISS Counts (COMPLETED)
10. Calculate Hit Rates (COMPLETED)
11. Session Evaluation Summary (COMPLETED)
12. Validation & Edge Cases (COMPLETED)
13. Automated Evaluation Tests (COMPLETED)

Performance will be tracked separately for:

-   Dozens
-   Columns
-   Corners
-   Splits
-   Streets

------------------------------------------------------------------------

### Phase 6 - Baseline Comparison

Goal:

Determine whether the prediction engine performs differently from simple
strategies.

1.  Create Baseline Engine (COMPLETED)
2.  Implement Random Baseline (COMPLETED)
3.  Implement Frequency-Only Baseline (COMPLETED)
4.  Implement Hot Baseline (COMPLETED)
5.  Implement Cold Baseline (COMPLETED)
6.  Standardize Baseline Prediction Output (COMPLETED)
7.  Add Strategy Labels (COMPLETED)
8.  Evaluate All Strategies on the Same Next Spin (COMPLETED)
9.  Track HIT / MISS Counts per Strategy (COMPLETED)
10. Calculate Hit Rates per Strategy (COMPLETED)
11. Create Baseline Comparison Summary (COMPLETED)
12. Calculate V1 Improvement vs Baselines (COMPLETED)
13. Validation & Edge Cases (COMPLETED)
14. Automated Baseline Tests (COMPLETED)

This is important for determining whether improvements are meaningful or
only random variation.

------------------------------------------------------------------------

### Phase 7 - Machine Learning

Goal:

Introduce actual ML models after sufficient data and evaluation
infrastructure exist.

1.  Create ML Module Structure (COMPLETED)
2.  Define ML Prediction Target (COMPLETED)
3.  Build ML Training Dataset (COMPLETED)
4.  Feature Engineering (COMPLETED)
5.  Create Chronological Training / Testing Split (COMPLETED)
6.  Implement Logistic Regression (COMPLETED)
7.  Implement Random Forest (COMPLETED)
8.  Implement Gradient Boosting (COMPLETED)
9.  Implement XGBoost (COMPLETED)
10. Standardize ML Prediction Output (COMPLETED)
11. Convert Number Probabilities to Bet Rankings (COMPLETED)
12. Evaluate ML Predictions (COMPLETED)
13. Compare ML vs V1 vs Baselines (COMPLETED)
14. Add ML Performance Metrics (COMPLETED)
15. Select Best ML Model (COMPLETED)
16. Create Training & Retraining Flow (COMPLETED)
17. Add Model Persistence (COMPLETED)
18. Validation & Edge Cases (COMPLETED)
19. Automated ML Tests (COMPLETED)
20. Final ML Benchmark (COMPLETED)

The ML model may rank individual roulette numbers or betting
combinations.

------------------------------------------------------------------------

### Phase 8 - Neon PostgreSQL Integration

Goal:

Persist roulette sessions, spins, prediction results, evaluation results, model versions, and model performance using Neon PostgreSQL.

Database configuration:

Platform: Neon
Database: roulette_ai
Schema: public

Planned steps:

1. Define Persistence Requirements — COMPLETED
2. Finalize Database Entity Responsibilities — COMPLETED
3. Design sessions Table — COMPLETED
4. Design spins Table — COMPLETED
5. Design prediction_runs Table — COMPLETED
6. Design prediction_items Table — COMPLETED
7. Design model_versions Table — COMPLETED
8. Design model_metrics Table — COMPLETED
9. Define Table Relationships and Foreign Keys — COMPLETED
10. Define Status Fields and Constraints — COMPLETED
11. Define Timestamps and Audit Fields — COMPLETED
12. Define PostgreSQL Schema and Naming Convention — COMPLETED
13. Create Tables in Neon — COMPLETED
14. Configure Primary Keys and UUID Strategy — COMPLETED
15. Configure Indexes for Common Queries — COMPLETED
16. Configure Database Security Strategy — COMPLETED
17. Create Python Neon Database Configuration — COMPLETED
18. Create PostgreSQL Database Service Module — COMPLETED
19. Implement Session Persistence — COMPLETED
20. Implement Spin Persistence — COMPLETED
21. Implement Prediction Run Persistence — COMPLETED
22. Implement Prediction Item Persistence — COMPLETED
23. Implement Model Version Persistence — COMPLETED
24. Implement Model Metrics Persistence — COMPLETED
25. Load Existing Session Data from Neon — COMPLETED
26. Reconstruct Roulette Sessions from Stored Spins — COMPLETED
27. Store Evaluation Results after Each Spin — COMPLETED
28. Connect ML Training Data to Historical Neon Data — COMPLETED
29. Connect Retraining Flow to Stored Sessions — COMPLETED
30. Add Database Validation and Error Handling — COMPLETED
31. Prevent Duplicate Records — COMPLETED
32. Add Neon PostgreSQL Integration Tests — COMPLETED
33. Test Full Session → Prediction → Evaluation → Database Flow — COMPLETED
34. Verify Historical Data Can Be Used for ML Benchmarking — COMPLETED
35. Final Phase 8 Integration Test — COMPLETED

The database schema will be finalized only after the local Python system
is understood properly.

------------------------------------------------------------------------

### Phase 9 - Python API

Goal:

Expose the completed Python engines, Neon PostgreSQL persistence layer, statistics, predictions, evaluation, and machine-learning functionality through a REST API.

Planned framework:

FastAPI

Planned architecture:

React Frontend
      │
      │ REST API / JSON
      ▼
FastAPI
      │
      ├── Session Engine
      ├── Statistics Engine
      ├── Prediction Engine V1
      ├── Baseline Engines
      ├── Evaluation Engine
      ├── Machine Learning Engine
      │
      ▼
Persistence / Repository Layer
      │
      ▼
Neon PostgreSQL

Planned steps:

1. Create FastAPI Module Structure — COMPLETED
2. Create Application Entry Point — COMPLETED
3. Configure Environment Variables — COMPLETED
4. Configure Neon PostgreSQL Database Dependency — COMPLETED
5. Define API Request / Response Schemas — COMPLETED
6. Create API Error Handling — COMPLETED
7. Create Health Check Endpoint — COMPLETED
8. Implement Create Session Endpoint — COMPLETED
9. Implement Get Session Endpoint — COMPLETED
10. Implement Add Initial Spins Endpoint — COMPLETED
11. Implement Add New Spin Endpoint — COMPLETED
12. Implement Get Session Spins Endpoint — COMPLETED
13. Connect Session Statistics Engine — COMPLETED
14. Implement Get Session Statistics Endpoint — COMPLETED
15. Connect Prediction Engine V1 — COMPLETED
16. Connect Baseline Prediction Engines — COMPLETED
17. Connect Machine Learning Prediction Engine — COMPLETED
18. Implement Generate Prediction Endpoint — COMPLETED
19. Implement Get Latest Prediction Endpoint — COMPLETED
20. Connect Prediction Evaluation Flow — COMPLETED
21. Automatically Evaluate Previous Prediction on New Spin — COMPLETED
22. Implement Get Session Evaluation Endpoint — COMPLETED
23. Implement Get Strategy Comparison Endpoint — COMPLETED
24. Implement Get ML Performance Endpoint — COMPLETED
25. Implement End Session Endpoint — COMPLETED
26. Implement Historical Sessions Endpoint — COMPLETED
27. Implement Model Information Endpoint — COMPLETED
28. Add API Input Validation — COMPLETED
29. Add API Response Standardization — COMPLETED
30. Configure CORS for React Frontend — COMPLETED
31. Add API Logging
32. Add API Integration Tests
33. Test Complete Session API Flow
34. Prepare Production Configuration
35. Final Phase 9 API Test

Expected API flow:

React / API Client
       ↓
POST /sessions
       ↓
Create Session
       ↓
POST Initial Spins
       ↓
Persist Session + Spins
       ↓
Generate Prediction
       ↓
Store Prediction
       ↓
Enter Next Spin
       ↓
Evaluate Previous Prediction
       ↓
Store Actual Spin
       ↓
Store HIT / MISS Evaluation
       ↓
Update Statistics
       ↓
Generate New Prediction
       ↓
Return Updated Results

Possible endpoint structure:

GET    /health

POST   /sessions
GET    /sessions
GET    /sessions/{id}

POST   /sessions/{id}/initial-spins
POST   /sessions/{id}/spins
GET    /sessions/{id}/spins

GET    /sessions/{id}/stats

POST   /sessions/{id}/predictions
GET    /sessions/{id}/predictions/latest

GET    /sessions/{id}/evaluation
GET    /sessions/{id}/comparison
GET    /sessions/{id}/ml-performance

POST   /sessions/{id}/end

GET    /models

Phase 9 responsibility:

Phase 1–7
Python Business Logic / AI / ML
          │
          ▼
Phase 8
Neon PostgreSQL Persistence
          │
          ▼
Phase 9
FastAPI REST Interface
          │
          ▼
Phase 10
React Frontend

The FastAPI layer should not duplicate the existing roulette, statistics, prediction, evaluation, ML, or persistence logic.

Its main responsibility is to:

Receive Request
      ↓
Validate Input
      ↓
Call Existing Python Service / Engine
      ↓
Read / Write Neon PostgreSQL
      ↓
Return Standard JSON Response

Status: PLANNED

------------------------------------------------------------------------

### Phase 10 - React Frontend

Goal:

Create the user interface for interacting with the roulette system
through the FastAPI backend.

Planned URL:

``` text
https://agien99.github.io/ai/
```

Planned steps:

1.  Create React + Vite Frontend
2.  Define Frontend Folder Structure
3.  Configure GitHub Pages Base Path
4.  Configure API Base URL
5.  Create Application Layout
6.  Create Navigation / Header
7.  Create Dashboard Page
8.  Create New Session Interface
9.  Create Initial Spin Input Component
10. Validate 10-15 Initial Spins
11. Connect Session Creation API
12. Create Active Session Interface
13. Create Roulette Number Input Component
14. Implement Quick Number Entry 0-36
15. Connect Add Spin API
16. Display Current Spin History
17. Create Prediction Panel
18. Display Dozen Predictions
19. Display Column Predictions
20. Display Street Predictions
21. Display Split Predictions
22. Display Corner Predictions
23. Display Prediction HIT / MISS Results
24. Create Session Statistics Panel
25. Display Number Frequency
26. Display Hot / Cold Numbers
27. Display Dozen / Column Statistics
28. Create Strategy Comparison Panel
29. Display V1 vs Baseline Performance
30. Create Machine Learning Performance Panel
31. Display ML Model Comparison
32. Display Current Best ML Model
33. Create Session Summary View
34. Implement End Session Action
35. Create Historical Sessions View
36. Create Session History Detail View
37. Add Loading States
38. Add API Error Handling
39. Add Empty States
40. Add Responsive Mobile Layout
41. Add Desktop Layout Optimization
42. Add User Confirmation for Destructive Actions
43. Configure Production API Connection
44. Configure GitHub Actions Deployment
45. Deploy React Frontend to GitHub Pages
46. Test Frontend ↔ FastAPI ↔ Supabase Integration
47. Test Complete User Workflow
48. Final UI / UX Review
49. Production Smoke Test
50. Final Phase 10 Integration Test

The completed frontend is planned to allow the user to:

-   Start a roulette session
-   Enter 10-15 initial historical spins
-   Enter new spin results
-   View ranked predictions
-   View HIT / MISS results
-   View current-session statistics
-   Compare prediction strategies
-   View machine-learning model performance
-   End the current session
-   Review historical sessions

Status: PLANNED

## Current Project Structure

``` text
ai/
├── .github/
│   └── workflows/
│       └── python-tests.yml
├── app/
│   ├── __init__.py
│   ├── roulette.py
│   ├── session.py
│   ├── statistics.py
│   ├── prediction.py
│   ├── evaluation.py
│   ├── baseline.py
│   ├── comparison.py
│   └── ml/
│       ├── __init__.py
│       ├── features.py
│       ├── dataset.py
│       ├── models.py
│       ├── engine.py
│       ├── ranking.py
│       ├── metrics.py
│       ├── training.py
│       ├── persistence.py
│       └── benchmark.py
├── tests/
│   ├── test_roulette.py
│   ├── test_session.py
│   ├── test_statistics.py
│   ├── test_prediction.py
│   ├── test_evaluation.py
│   ├── test_baseline.py
│   ├── test_comparison.py
│   ├── test_ml_features.py
│   ├── test_ml_dataset.py
│   ├── test_ml_models.py
│   ├── test_ml_ranking.py
│   ├── test_ml_metrics.py
│   ├── test_ml_training.py
│   └── test_ml_benchmark.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Current Progress

``` text
Phase 1 - Roulette Domain Engine       COMPLETED
Phase 2 - Session Engine               COMPLETED
Phase 3 - Statistical Analysis         COMPLETED
Phase 4 - Prediction Engine V1         COMPLETED
Phase 5 - Prediction Evaluation        COMPLETED
Phase 6 - Baseline Comparison          COMPLETED
Phase 7 - Machine Learning             COMPLETED

Phase 8 - Supabase Integration         NEXT
Phase 9 - Python API                   PLANNED
Phase 10 - React Frontend              PLANNED
```

Current milestone:

``` text
Core Python Engine          ✅
Statistical Prediction      ✅
Prediction Evaluation       ✅
Baseline Comparison         ✅
Machine Learning            ✅
Database Persistence        ⏭ NEXT
REST API                    ○
React Frontend              ○
```

## Development Principle

This project will be developed incrementally.

``` text
Build
  ↓
Test
  ↓
Understand
  ↓
Verify
  ↓
Proceed
```

Each phase should work properly before moving to the next phase.

## Disclaimer

Roulette outcomes on a fair wheel are designed to be independent and
random.

This project is intended primarily as an AI/ML, statistics, software
engineering, and experimentation project. Historical hot/cold patterns
should not be assumed to guarantee future outcomes.