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

Possible statistics include:

* Number frequency
* Recent frequency
* Spins since last appearance
* Hot numbers
* Cold numbers
* Dozen frequency
* Column frequency
* Street activity
* Split activity
* Corner activity
* Different recent-spin windows

Examples:

```text
Last 5 spins
Last 10 spins
Last 20 spins
Entire current session
```

---

### Phase 4 - Prediction Engine V1

Goal:

Generate ranked predictions without machine learning first.

Initial approach:

```text
Session statistics
        +
Recency
        +
Frequency
        +
Bet-group activity
        ↓
Prediction score
```

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

Example:

```text
Prediction generated
        ↓
Next spin occurs
        ↓
Actual number entered
        ↓
Evaluate every predicted bet
        ↓
HIT / MISS
```

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

Possible baselines:

* Random selection
* Frequency-only prediction
* Hot-number prediction
* Cold-number prediction

Example comparison:

```text
Prediction Engine V1
vs
Random Baseline
vs
Frequency Baseline
```

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
