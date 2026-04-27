# Bayesian A/B Testing Platform

Production-style MERN app for creating experiments, rendering HTML/CSS variants safely, collecting preference data, and allocating traffic with Bayesian Thompson Sampling.

## What is included

- `backend/`: Express + MongoDB API with JWT authentication, RBAC, experiment management, interaction tracking, and Bayesian posterior updates.
- `frontend/`: React + TypeScript UI for user and admin workflows.

## Core workflow

1. Register or log in as a `user` or `admin`.
2. Create an experiment with 2 to 6 variants.
3. Add HTML and CSS for each variant.
4. Choose the experiment mode:
   - `side_by_side`: show multiple variants together and record a preferred winner
   - `thompson_sampling`: serve one variant per visitor based on posterior samples
5. Record impressions and user outcomes.
6. Update Beta posteriors:
   - Side-by-side winner: `alpha += 1`
   - Side-by-side losers: `beta += 1`
   - Thompson success on shown variant: `alpha += 1`
   - Thompson failure on shown variant: `beta += 1`
7. Recalculate `probabilityBest` with Monte Carlo sampling over each variant's Beta posterior.

## Backend API

### Auth

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`

### Experiments

- `POST /api/experiments`
- `GET /api/experiments`
- `GET /api/experiments/:id`
- `PATCH /api/experiments/:id/status` (`admin` only)

### Variants

- `POST /api/variants`
- `GET /api/variants/:experimentId`

### Interactions

- `POST /api/interactions/record-click`
- `POST /api/interactions/record-impression`
- `POST /api/interactions/record-outcome`

### Bayesian

- `POST /api/bayesian/update-posterior`
- `GET /api/bayesian/allocation/:experimentId`
- `GET /api/bayesian/summary/:experimentId`
- `GET /api/bayesian/serve/:experimentId`

### Admin

- `GET /api/admin/experiments`

## Database models

- `User`: `name`, `email`, `password`, `role`
- `Experiment`: `title`, `description`, `createdBy`, `variantCount`, `variantIds`, `mode`, `status`
- `Variant`: `experimentId`, `name`, `htmlContent`, `cssContent`, `clicks`, `impressions`
- `BayesianState`: `experimentId`, `variantId`, `alpha`, `beta`, `probabilityBest`

## Local setup

### 1. Backend

```bash
cd backend
cp .env.example .env
npm install
npm run seed
npm run dev
```

Default backend URL: `http://localhost:5000`

### 2. Frontend

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Default frontend URL: `http://localhost:5173`

## Sample seeded users

- Admin: `admin@example.com` / `password123`
- User: `user@example.com` / `password123`

## Notes

- Variant HTML/CSS is sanitized to strip `<script>` tags, inline event handlers, and `javascript:` URLs.
- Rendering happens inside sandboxed iframes on the frontend.
- `thompson_sampling` experiments serve one variant per visitor and update only the shown variant's posterior based on success or failure.
- Thompson Sampling and `probabilityBest` calculations live in `backend/src/services/bayesianService.js` and `backend/src/utils/beta.js`.
- `.gitignore` excludes dependencies, build output, logs, and local `.env` files so the repo is ready for GitHub.
