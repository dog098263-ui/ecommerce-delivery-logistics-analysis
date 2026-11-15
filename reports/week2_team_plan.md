# Week 2: Team Work Division & Collaboration Roadmap
**Project 1: E-commerce Delivery & Logistics Performance Analysis**  
**Engineering Focus**: KPI Engineering, Multi-Dimensional Segmentation & Delay Pattern Analysis

---

## 👥 Team Roles & Responsibilities

| Member | GitHub Username | Role & Assigned Area | Feature Branch | Primary Deliverables |
| :--- | :--- | :--- | :--- | :--- |
| **Aman Shakil (Lead)** | `dog098263-ui` | Core KPI Engine & Metric Governance | `feature/aman-core-kpis` | `src/kpis.py`<br>`reports/kpi_definitions.md`<br>`data/processed/validated_kpis.csv` |
| **Abhijith V** | `Me-Abhijith-V` | Carrier & Dispatch Latency Analysis | `feature/abhijith-carrier-analysis` | `notebooks/02_carrier_analysis.ipynb`<br>`reports/figures/carrier_performance.png` |
| **Akhila Nair** | `akhila-nair2005` | Regional & Route Logistics Analysis | `feature/akhila-regional-analysis` | `notebooks/02_regional_analysis.ipynb`<br>`reports/figures/regional_delay_matrix.png` |
| **Adbot** | `adbot-47` | Temporal & Weekday Delay Patterns | `feature/adbot-temporal-patterns` | `notebooks/02_temporal_analysis.ipynb`<br>`reports/figures/weekday_delay_heatmap.png` |
| **Bhagyashree** | `Bhagyashree-2004` | Product Categories & Rating Impact | `feature/bhagyashree-category-ratings` | `notebooks/02_category_ratings.ipynb`<br>`reports/figures/rating_decay_curve.png` |

---

## 📅 Daily Commit & Milestone Schedule (Week 2)

```text
Day 1 (Mon): Branch Creation & Baseline Setup
Day 2 (Tue): Data Aggregations & Core Metric Calculations
Day 3 (Wed): Segment Comparisons & Sample Size Filtering
Day 4 (Thu): Visualization, Edge-Case Auditing & Interpretation
Day 5 (Fri): Documentation, Final Script Cleanups & Pull Request to Main
```

---

## 📋 Detailed Task Breakdown by Team Member

### 1. Aman Shakil (`dog098263-ui`) — Core KPI Engine & Governance
* **Goal**: Build reusable SQL & Python KPI modules and maintain metric accuracy.
* **Daily Commit Plan**:
  * **Day 1**: Author `reports/kpi_definitions.md` detailing explicit numerators, denominators, and exclusion logic for:
    * On-Time Delivery (OTD) Rate
    * Cancellation Rate
    * Average Delivery Duration & Delay
    * Order Processing Time (Placement to Dispatch)
  * **Day 2**: Implement modular SQL queries in `src/kpis.py` against `data/interim/logistics.db`.
  * **Day 3**: Build reusable Python KPI wrapper functions returning formatted metrics and summaries.
  * **Day 4**: Generate and validate `data/processed/validated_kpi_dataset.csv` (excluding corrupted timestamps).
  * **Day 5**: Review and merge teammates' Pull Requests into `main`.

### 2. Abhijith V (`Me-Abhijith-V`) — Carrier & Dispatch Latency
* **Goal**: Disentangle seller processing delays from carrier transit delays.
* **Daily Commit Plan**:
  * **Day 1**: Create `notebooks/02_carrier_analysis.ipynb` and import interim dataset.
  * **Day 2**: Measure split between **Processing Latency** (`purchase` to `carrier_date`) vs. **Transit Latency** (`carrier_date` to `delivery_date`).
  * **Day 3**: Measure seller compliance against `shipping_limit_date` (on-time vs late handoff to carrier).
  * **Day 4**: Rank top dispatch routes and seller performance with volume thresholds (exclude sellers with <10 orders to prevent small-sample bias).
  * **Day 5**: Export summary table, save `carrier_performance.png`, and open Pull Request.

### 3. Akhila Nair (`akhila-nair2005`) — Regional & Route Logistics
* **Goal**: Identify geographic fulfillment bottlenecks across Brazil.
* **Daily Commit Plan**:
  * **Day 1**: Create `notebooks/02_regional_analysis.ipynb` and inspect customer/seller state pairs.
  * **Day 2**: Analyze Intrastate (same state) vs. Interstate (cross-state) fulfillment speed and delay rates.
  * **Day 3**: Calculate delay rates and average freight fees across all 27 Brazilian destination states.
  * **Day 4**: Highlight top 5 high-delay shipping corridors (e.g. SP -> BA, SP -> RJ).
  * **Day 5**: Save `regional_delay_matrix.png`, document regional findings, and open Pull Request.

### 4. Adbot (`adbot-47`) — Temporal & Weekday Delay Patterns
* **Goal**: Uncover operational day-of-week and seasonal bottlenecks.
* **Daily Commit Plan**:
  * **Day 1**: Create `notebooks/02_temporal_analysis.ipynb` and extract date components (weekday, hour, month).
  * **Day 2**: Group processing times by order purchase day (Monday to Sunday) to test weekend dispatch backlogs.
  * **Day 3**: Analyze carrier pickup patterns by day of the week (do weekend orders take longer to enter transit?).
  * **Day 4**: Track monthly OTD rate trends (2017–2018) to discover holiday spikes (e.g. Black Friday fulfillment lag).
  * **Day 5**: Save `weekday_delay_heatmap.png`, document operational cutoff recommendations, and open Pull Request.

### 5. Bhagyashree (`Bhagyashree-2004`) — Product Categories & Rating Impact
* **Goal**: Measure category delivery complexity and customer rating sensitivity.
* **Daily Commit Plan**:
  * **Day 1**: Create `notebooks/02_category_ratings.ipynb` using English translated product categories.
  * **Day 2**: Compare delivery duration and cancellation rates across product categories (e.g. heavy furniture vs small electronics).
  * **Day 3**: Construct customer rating decay curves: Plot mean review scores and % of 1-star reviews against delay buckets (On-Time, 1-3 days late, 4-7 days late, 8+ days late).
  * **Day 4**: Document causal limitations (distinguish correlation between late delivery and low ratings from other factors like product defects).
  * **Day 5**: Save `rating_decay_curve.png`, summarize customer satisfaction insights, and open Pull Request.

---

## 🛠 Collaboration & Git Branching Workflow

Each team member will work in their dedicated branch so there are **zero merge conflicts**:

```bash
# 1. Fetch latest changes from main
git checkout main
git pull origin main

# 2. Switch to your feature branch
git checkout -b feature/<your-branch-name>

# 3. Commit daily with descriptive messages
git add .
git commit -m "feat(carrier): compute dispatch vs transit latency breakdown"

# 4. Push branch to GitHub
git push -u origin feature/<your-branch-name>

# 5. Open a Pull Request on GitHub for review and merge into main
```
