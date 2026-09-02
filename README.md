# Roulette AI Experiment

A learning project focused on building a session-based AI/ML system for analyzing European Roulette results and generating ranked betting predictions.

The main goal of this project is not to guarantee roulette outcomes, but to learn and experiment with:

* Python
* Data processing
* Statistical analysis
* Feature engineering
* Machine learning
* Model evaluation
* API development
* Supabase integration
* React frontend integration

## Roulette Type

This project currently targets:

* European Roulette
* Numbers: `0-36`
* Single zero

## Prediction Targets

For every next spin, the system is planned to generate:

* 2 possible Dozens
* 2 possible Columns
* 5 possible Corner bets
* 12 possible Split bets
* 6 possible Street bets

Predictions will eventually be ranked using statistical features and machine learning models.

## Session-Based Design

Roulette observations are handled as separate sessions.

Example:

```text
Session A
5:00 PM - 9:00 PM

Session B
11:00 PM - 1:00 AM
```

A new session is started when there is a gap where roulette spins were not observed.

Each session begins with approximately 10-15 recent roulette results.

The system will then:

```text
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

Previous sessions will eventually remain stored for evaluation and long-term ML experimentation, but each new session will have its own short-term state.

## Planned Architecture

```text
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

The project will be developed locally first before deployment is considered.

## Development Phases

### Phase 1 - Roulette Domain Engine

Goal:

Make Python understand the European Roulette table and its betting structures.

Planned steps:

1. Create Python repository and project structure (COMPLETED)
2. Define valid roulette numbers (COMPLETED)
3. Implement Dozens (COMPLETED)
4. Implement Columns (COMPLETED)
5. Implement Streets (COMPLETED)
6. Implement Splits (COMPLETED)
7. Implement Corners (COMPLETED)
8. Add validation (COMPLETED)
9. Add basic tests (COMPLETED)

---

### Phase 2 - Session Engine

Goal:
Create isolated roulette observation sessions.

Steps:

1. Define RouletteSession model (COMPLETED)
2. Start session with 10-15 initial spins (COMPLETED)
3. Add new spins sequentially (COMPLETED)
4. Maintain spin sequence/order (COMPLETED)
5. Track session state and metadata (COMPLETED)
6. End/close session (COMPLETED)
7. Start fresh independent session (COMPLETED)
8. Session validation and edge cases (COMPLETED)
9. Automated session tests (COMPLETED)

---

### Phase 3 - Statistical Analysis

Goal:

Extract useful features from the current roulette session.

1. Create Statistics Engine (COMPLETED)
2. Number Frequency (COMPLETED)
3. Recent-Window Frequency (COMPLETED)
4. Spins Since Last Appearance (COMPLETED)
5. Hot & Cold Numbers (COMPLETED)
6. Dozen Frequency (COMPLETED)
7. Column Frequency (COMPLETED)
8. Street Activity (COMPLETED)
9. Split Activity (COMPLETED)
10. Corner Activity (COMPLETED)
11. Combined Session Statistics (COMPLETED)
12. Validation & Edge Cases (COMPLETED)
13. Automated Statistical Tests (COMPLETED)

---

### Phase 4 - Prediction Engine V1

Goal:

Generate ranked predictions without machine learning first.

1. Create Prediction Engine (COMPLETED)
2. Define Scoring Components (COMPLETED)
3. Score Dozens (COMPLETED)
4. Score Columns (COMPLETED)
5. Score Streets (COMPLETED)
6. Score Splits (COMPLETED)
7. Score Corners (COMPLETED)
8. Rank Predictions (COMPLETED)
9. Generate Final Prediction Set (COMPLETED)
10. Prediction Output Structure (COMPLETED)
11. Validation & Edge Cases (COMPLETED)
12. Automated Prediction Tests (COMPLETED)
13. Baseline Evaluation Preparation (COMPLETED)

Expected output:

```text
2 Dozens
2 Columns
5 Corners
12 Splits
6 Streets
```

This phase will create the baseline prediction engine.

---

### Phase 5 - Prediction Evaluation

Goal:

Measure whether previous predictions hit the next roulette result.

1. Create Evaluation Engine (COMPLETED)
2. Define Prediction Evaluation Record (COMPLETED)
3. Evaluate Dozen Predictions (COMPLETED)
4. Evaluate Column Predictions (COMPLETED)
5. Evaluate Street Predictions (COMPLETED)
6. Evaluate Split Predictions (COMPLETED)
7. Evaluate Corner Predictions (COMPLETED)
8. Evaluate Complete Prediction Set (COMPLETED)
9. Track HIT / MISS Counts (COMPLETED)
10. Calculate Hit Rates (COMPLETED)
11. Session Evaluation Summary (COMPLETED)
12. Validation & Edge Cases (COMPLETED)
13. Automated Evaluation Tests (COMPLETED)

Performance will be tracked separately for:

* Dozens
* Columns
* Corners
* Splits
* Streets

---

### Phase 6 - Baseline Comparison

Goal:

Determine whether the prediction engine performs differently from simple strategies.

1. Create Baseline Engine (COMPLETED)
2. Implement Random Baseline (COMPLETED)
3. Implement Frequency-Only Baseline (COMPLETED)
4. Implement Hot Baseline (COMPLETED)
5. Implement Cold Baseline (COMPLETED)
6. Standardize Baseline Prediction Output (COMPLETED)
7. Add Strategy Labels (COMPLETED)
8. Evaluate All Strategies on the Same Next Spin (COMPLETED)
9. Track HIT / MISS Counts per Strategy (COMPLETED)
10. Calculate Hit Rates per Strategy (COMPLETED)
11. Create Baseline Comparison Summary (COMPLETED)
12. Calculate V1 Improvement vs Baselines (COMPLETED)
13. Validation & Edge Cases (COMPLETED)
14. Automated Baseline Tests (COMPLETED)

This is important for determining whether improvements are meaningful or only random variation.

---

### Phase 7 - Machine Learning

Goal:

Introduce actual ML models after sufficient data and evaluation infrastructure exist.

1. Create ML Module Structure (COMPLETED)
2. Define ML Prediction Target (COMPLETED)
3. Build ML Training Dataset (COMPLETED)
4. Feature Engineering (COMPLETED)
5. Create Chronological Training / Testing Split (COMPLETED)
6. Implement Logistic Regression (COMPLETED)
7. Implement Random Forest (COMPLETED)
8. Implement Gradient Boosting (COMPLETED)
9. Implement XGBoost (COMPLETED)
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

The ML model may rank individual roulette numbers or betting combinations.

---

### Phase 8 - Supabase Integration

Goal:

Persist roulette sessions and model performance.

Possible database entities:

1. Define Persistence Requirements
2. Finalize Database Entity Responsibilities
3. Design sessions Table
4. Design spins Table
5. Design prediction_runs Table
6. Design prediction_items Table
7. Design model_versions Table
8. Design model_metrics Table
9. Define Table Relationships and Foreign Keys
10. Define Status Fields and Constraints
11. Define Timestamps and Audit Fields
12. Define Supabase Schema and Naming Convention
13. Create Tables in Supabase
14. Configure Primary Keys and UUID Strategy
15. Configure Indexes for Common Queries
16. Configure Row Level Security Policies
17. Create Python Supabase Configuration
18. Create Supabase Database Service Module
19. Implement Session Persistence
20. Implement Spin Persistence
21. Implement Prediction Run Persistence
22. Implement Prediction Item Persistence
23. Implement Model Version Persistence
24. Implement Model Metrics Persistence
25. Load Existing Session Data from Supabase
26. Reconstruct Roulette Sessions from Stored Spins
27. Store Evaluation Results after Each Spin
28. Connect ML Training Data to Historical Supabase Data
29. Connect Retraining Flow to Stored Sessions
30. Add Database Validation and Error Handling
31. Prevent Duplicate Records
32. Add Supabase Integration Tests
33. Test Full Session → Prediction → Evaluation → Database Flow
34. Verify Historical Data Can Be Used for ML Benchmarking
35. Final Phase 8 Integration Test

The database schema will be finalized only after the local Python system is understood properly.

---

### Phase 9 - Python API

Goal:

Expose the prediction system through an API.

Planned framework:

```text
FastAPI
```

Possible endpoints:

```text
POST /sessions

POST /sessions/{id}/spins

GET /sessions/{id}/prediction

GET /sessions/{id}/stats

POST /sessions/{id}/end
```

---

### Phase 10 - React Frontend

Goal:

Create an interface accessible through:

```text
https://agien99.github.io/ai/
```

The React frontend will allow the user to:

* Start a roulette session
* Enter historical spins
* Enter new spin results
* View predictions
* View hit/miss results
* View session statistics
* View model performance

## Current Project Structure

```text
ai/
├── app/
│   ├── __init__.py
│   ├── roulette.py
│   └── session.py
├── tests/
│   └── test_roulette.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Current Progress

Phase:

```text
Phase 1 - Roulette Domain Engine
```

Completed:

```text
Phase 1
└── Step 1 - Project setup
```

Next:

```text
Phase 1
└── Step 2 - Define European Roulette numbers and basic table structure
```

## Development Principle

This project will be developed incrementally.

```text
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

Roulette outcomes on a fair wheel are designed to be independent and random.

This project is intended primarily as an AI/ML, statistics, software engineering, and experimentation project. Historical hot/cold patterns should not be assumed to guarantee future outcomes.
