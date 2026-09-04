# RouletteIQ

**Session-Based Roulette Analytics & Prediction Engine**

RouletteIQ is a full-stack software engineering and AI/ML experimentation project for analyzing **European Roulette** sessions, generating ranked predictions, evaluating prediction performance, and preserving historical session data for statistical and machine-learning research.

The project is designed as an analytical and educational system. It does **not** claim to predict random roulette outcomes with certainty or guarantee gambling results.

## Live Application

- **Frontend:** https://agien99.github.io/rouletteiq/
- **Source Repository:** https://github.com/Agien99/rouletteiq
- **Backend:** FastAPI deployed on Render
- **Database:** Neon PostgreSQL

> The backend is hosted on Render's free service tier and may require a short warm-up period after inactivity.

## Technology Stack

### Frontend

- React
- Vite
- JavaScript
- Responsive CSS
- GitHub Pages
- GitHub Actions

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

### Data & Analytics

- Statistical analysis
- Feature engineering
- Prediction Engine V1
- Prediction evaluation
- Baseline strategy comparison
- Machine-learning infrastructure

### Persistence & Deployment

- Neon PostgreSQL
- Render
- GitHub Pages
- GitHub Actions

## System Architecture

```text
User
 │
 ▼
RouletteIQ Frontend
React + Vite
GitHub Pages
 │
 │ REST API / JSON
 ▼
FastAPI Backend
Render
 │
 ├── Session Engine
 ├── Roulette Domain Engine
 ├── Statistics Engine
 ├── Prediction Engine V1
 ├── Evaluation Engine
 ├── Baseline Comparison
 └── Machine Learning
 │
 ▼
Persistence / Repository Layer
 │
 ▼
Neon PostgreSQL
```

The frontend, API, and database are deployed independently. The frontend communicates with the FastAPI service over HTTP, while the backend is responsible for domain logic and persistence.

## Roulette Model

RouletteIQ currently targets **European Roulette**:

- Single-zero wheel
- Valid numbers: `0-36`
- Dozens
- Columns
- Streets
- Splits
- Corners

The roulette domain layer validates numbers and maps results to the supported betting structures.

## Session-Based Analysis

RouletteIQ treats observations as independent sessions rather than one continuous global sequence.

A session begins with a historical sample of **at least 10 spins**. There is currently no application-defined maximum for the initial history.

After initialization, the normal workflow is:

```text
Initial Spin History
        │
        ▼
Analyze Session
        │
        ▼
Generate Prediction
        │
        ▼
Record Next Observed Spin
        │
        ▼
Evaluate Previous Prediction
        │
        ▼
Persist Result
        │
        ▼
Update Statistics
        │
        ▼
Generate Prediction for Next Spin
```

Sessions remain persisted in PostgreSQL so they can later be reviewed, evaluated, compared, and used as historical data.

A browser refresh or closing the application does not automatically end an active session. Active sessions can be recovered from persisted data and continued later.

## Prediction Engine V1

Prediction Engine V1 is the primary statistical ranking engine.

For each target spin it ranks:

| Category | Predictions |
| --- | ---: |
| Dozens | 2 |
| Columns | 2 |
| Streets | 6 |
| Splits | 12 |
| Corners | 5 |

The engine combines statistical signals such as frequency, recency, and roulette-structure activity.

### Prediction Scores

Prediction scores are **ranking scores, not probabilities**.

A higher score means that a candidate ranked more strongly according to the engine's scoring components. A displayed score must not be interpreted as a percentage chance that the prediction will win.

## Prediction Evaluation

When a new observed spin is recorded, RouletteIQ evaluates the prediction that targeted that spin.

Performance is tracked separately for:

- Dozens
- Columns
- Streets
- Splits
- Corners

Each category can therefore produce its own `HIT` or `MISS` result.

This makes it possible to evaluate the prediction engine using actual subsequent observations instead of judging predictions only by their ranking score.

## Statistics

The application provides current-session statistical analysis including:

- Number frequency
- Recent-window frequency
- Spins since last appearance
- Hot numbers
- Cold numbers
- Dozen frequency
- Column frequency
- Street activity
- Split activity
- Corner activity

Statistics are recalculated as new observations are added to the session.

## Baseline Comparison

RouletteIQ includes baseline strategy infrastructure for comparing Prediction Engine V1 against simpler approaches such as:

- Random selection
- Frequency-based selection
- Hot-number strategies
- Cold-number strategies

The purpose of baseline comparison is to determine whether an analytical strategy performs differently from simpler alternatives rather than assuming that a prediction method is meaningful by itself.

The frontend only displays comparison data that is actually available from persisted/evaluated strategy runs; it does not fabricate missing baseline results.

## Machine Learning

The project also contains machine-learning infrastructure for experimentation with historical roulette-session data.

Implemented work includes:

- Feature engineering
- Training dataset construction
- Chronological train/test separation
- Logistic Regression
- Random Forest
- Gradient Boosting
- XGBoost
- Number-probability ranking
- Model evaluation
- Model comparison
- Model persistence
- Training and retraining flow
- Performance metrics

ML information is displayed only when trained model versions and performance data are available. An absence of trained models is treated as a valid application state.

The statistical Prediction Engine V1 remains usable independently of ML model availability.

## Session Persistence

Production data is stored in **Neon PostgreSQL**.

Persistence covers data such as:

- Sessions
- Spins
- Prediction runs
- Prediction items
- Evaluation information
- Model versions
- Model metrics

The persistence layer allows RouletteIQ to reconstruct sessions from stored spins and maintain history independently of frontend browser state.

## Main API Flow

The FastAPI backend exposes the application engines through REST endpoints.

Representative session endpoints include:

```text
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
```

The API layer is intentionally kept separate from the underlying domain and analytical engines.

Conceptually:

```text
Request
   │
   ▼
Validate Input
   │
   ▼
Application / Domain Service
   │
   ├── Analyze
   ├── Predict
   ├── Evaluate
   └── Persist
   │
   ▼
JSON Response
```

## Frontend Features

The production React frontend provides:

- Dashboard overview
- New-session creation
- Interactive European Roulette number table
- Initial-spin history entry
- Active-session recovery
- Observed-spin recording
- Horizontal spin history
- Ranked Prediction Engine V1 results
- Prediction HIT/MISS evaluation
- Session statistics
- Strategy comparison
- ML performance display
- Session summary
- Historical-session browser
- Continue-active-session workflow
- End-session workflow
- Loading, empty, error, and confirmation states
- Responsive desktop, tablet, and phone layouts

## Repository Structure

The project is organized broadly as:

```text
rouletteiq/
├── .github/
│   └── workflows/
├── app/
│   ├── api/
│   ├── ml/
│   ├── roulette.py
│   ├── session.py
│   ├── statistics.py
│   ├── prediction.py
│   ├── evaluation.py
│   ├── baseline.py
│   └── comparison.py
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/
│       ├── config/
│       ├── pages/
│       ├── services/
│       ├── styles/
│       └── utils/
├── tests/
├── .env.example
├── main.py
├── requirements.txt
└── README.md
```

The exact contents may evolve as the project is refactored. This section documents the high-level organization rather than every individual file.

## Production Deployment

### Frontend

The React/Vite frontend is deployed through GitHub Pages:

```text
https://agien99.github.io/rouletteiq/
```

The Vite base path must remain consistent with the GitHub Pages repository path:

```text
/rouletteiq/
```

Frontend production builds obtain the backend address through:

```text
VITE_API_BASE_URL
```

### Backend

The FastAPI application is deployed on Render.

Production startup uses the API application under:

```text
app.api.main:app
```

The backend requires environment configuration including the PostgreSQL connection and allowed frontend origin.

Important production variables include:

```text
DATABASE_URL
API_ENV
LOG_LEVEL
CORS_ORIGINS
API_DOCS_ENABLED
```

Do not commit production secrets or database credentials to the repository.

### Database

The production persistence layer uses Neon PostgreSQL.

The backend accesses Neon through `DATABASE_URL`. Database credentials belong in deployment environment variables and must not be hardcoded in frontend or source files.

## Development Notes

### Frontend

From the `frontend` directory:

```bash
npm install
npm run dev
```

Before committing frontend changes:

```bash
npm run lint
npm run build
```

### Backend

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI development server from the repository root:

```bash
uvicorn app.api.main:app --reload
```

Run automated Python tests:

```bash
pytest
```

### Environment Configuration

Use `.env.example` as the reference for local configuration where applicable.

Never commit `.env` files containing real credentials.

## Important Maintenance Notes

For future development, keep these architectural rules in mind:

1. **Do not place database credentials in the React application.** The frontend communicates with FastAPI; FastAPI communicates with PostgreSQL.
2. **Keep domain logic out of API route handlers where possible.** API routes should validate requests, call application/domain services, and return responses.
3. **Treat prediction scores as ranking scores.** They are not probabilities or guaranteed win percentages.
4. **Preserve session isolation.** Statistics and predictions for one roulette session should not accidentally use another active session's short-term state.
5. **Evaluate a prediction against the spin it targeted.** Avoid creating duplicate pending prediction runs for the same session/target spin.
6. **Persist before relying on frontend state.** Browser state is temporary; Neon is the source of persistent session history.
7. **Keep the GitHub Pages base path synchronized with the repository name.** The production path is `/rouletteiq/`.
8. **Keep CORS configured by origin.** The production frontend origin is `https://agien99.github.io`; `/rouletteiq/` is a path, not a separate origin.
9. **Run tests before deployment.** Frontend lint/build and backend automated tests are the minimum regression checks.
10. **Do not assume ML data exists.** The application must remain functional when no trained model versions are available.

## Development Principle

RouletteIQ was built incrementally using the following development principle:

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

New features should continue to follow the same principle: make one coherent change, test it, understand its impact, verify the complete flow, and only then continue.

## Future Development

Possible future work includes:

- Stronger database-level idempotency for prediction generation
- Additional prediction strategies
- Larger historical datasets for ML experimentation
- Automated or controlled model retraining
- Deeper model-vs-baseline benchmarking
- Improved analytical visualizations
- Exportable session/evaluation reports
- Authentication or user-specific sessions if the application becomes multi-user
- Additional monitoring and production observability

Future features should be driven by measured usefulness and evaluation results rather than an assumption that increased model complexity will improve roulette prediction.

## Disclaimer

European Roulette outcomes on a fair wheel are designed to be random and independent.

RouletteIQ is an educational, statistical-analysis, AI/ML, and software-engineering project. Historical patterns, hot/cold numbers, statistical rankings, prediction scores, baseline strategies, and machine-learning outputs do not guarantee future outcomes.

The application should not be interpreted as providing guaranteed betting advice.
