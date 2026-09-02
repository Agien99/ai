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

Step 1  — Create Statistics Engine (COMPLETED)
Step 2  — Number Frequency (COMPLETED)
Step 3  — Recent-Window Frequency (COMPLETED)
Step 4  — Spins Since Last Appearance (COMPLETED)
Step 5  — Hot & Cold Numbers (COMPLETED)
Step 6  — Dozen Frequency (COMPLETED)
Step 7  — Column Frequency (COMPLETED)
Step 8  — Street Activity (COMPLETED)
Step 9  — Split Activity (COMPLETED)
Step 10 — Corner Activity (COMPLETED)
Step 11 — Combined Session Statistics (COMPLETED)
Step 12 — Validation & Edge Cases (COMPLETED)
Step 13 — Automated Statistical Tests (COMPLETED)

---

### Phase 4 - Prediction Engine V1

Goal:

Generate ranked predictions without machine learning first.

Step 1  — Create Prediction Engine (COMPLETED)
Step 2  — Define Scoring Components (COMPLETED)
Step 3  — Score Dozens (COMPLETED)
Step 4  — Score Columns (COMPLETED)
Step 5  — Score Streets (COMPLETED)
Step 6  — Score Splits (COMPLETED)
Step 7  — Score Corners (COMPLETED)
Step 8  — Rank Predictions (COMPLETED)
Step 9  — Generate Final Prediction Set (COMPLETED)
Step 10 — Prediction Output Structure (COMPLETED)
Step 11 — Validation & Edge Cases (COMPLETED)
Step 12 — Automated Prediction Tests (COMPLETED)
Step 13 — Baseline Evaluation Preparation (COMPLETED)

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

Step 1  Create Evaluation Engine (COMPLETED)
Step 2  Define Prediction Evaluation Record (COMPLETED)
Step 3  Evaluate Dozen Predictions (COMPLETED)
Step 4  Evaluate Column Predictions (COMPLETED)
Step 5  Evaluate Street Predictions (COMPLETED)
Step 6  Evaluate Split Predictions (COMPLETED)
Step 7  Evaluate Corner Predictions (COMPLETED)
Step 8  Evaluate Complete Prediction Set (COMPLETED)
Step 9  Track HIT / MISS Counts (COMPLETED)
Step 10 Calculate Hit Rates (COMPLETED)
Step 11 Session Evaluation Summary (COMPLETED)
Step 12 Validation & Edge Cases (COMPLETED)
Step 13 Automated Evaluation Tests (COMPLETED)

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

Step 1 - Create Baseline Engine (COMPLETED)
Step 2 - Implement Random Baseline (COMPLETED)
Step 3 - Implement Frequency-Only Baseline (COMPLETED)
Step 4 - Implement Hot Baseline (COMPLETED)
Step 5 - Implement Cold Baseline (COMPLETED)
Step 6 - Standardize Baseline Prediction Output
Step 7 - Add Strategy Labels
Step 8 - Evaluate All Strategies on the Same Next Spin
Step 9 - Track HIT / MISS Counts per Strategy
Step 10 - Calculate Hit Rates per Strategy
Step 11 - Create Baseline Comparison Summary
Step 12 - Calculate V1 Improvement vs Baselines
Step 13 - Validation & Edge Cases
Step 14 - Automated Baseline Tests

This is important for determining whether improvements are meaningful or only random variation.

---

### Phase 7 - Machine Learning

Goal:

Introduce actual ML models after sufficient data and evaluation infrastructure exist.

Possible models:

* Logistic Regression
* Random Forest
* Gradient Boosting
* XGBoost
* Neural Networks later if useful

The ML model may rank individual roulette numbers or betting combinations.

---

### Phase 8 - Supabase Integration

Goal:

Persist roulette sessions and model performance.

Possible database entities:

```text
sessions
spins
prediction_runs
prediction_items
model_versions
model_metrics
```

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
