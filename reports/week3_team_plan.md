# Week 3: Team Work Division & Collaboration Roadmap
**Project 1: E-commerce Delivery & Logistics Performance Analysis**  
**Engineering Focus**: Deeper Analysis, Root-Cause Prioritization & Operational Opportunity Assessment

---

## 👥 Team Roles & Responsibilities

| Member | GitHub Username | Role & Assigned Investigation | Feature Branch | Primary Deliverables |
| :--- | :--- | :--- | :--- | :--- |
| **Aman Shakil (Lead)** | `dog098263-ui` | Prioritized Issue Matrix & Executive Recommendations | `feature/aman-prioritized-issues` | `reports/prioritized_issue_list.csv`<br>`reports/week3_operational_recommendations.md`<br>`src/prioritize_issues.py` |
| **Abhijith V** | `Me-Abhijith-V` | Warehouse Dispatch Bottlenecks & Seller SLA Deep Dive | `feature/abhijith-warehouse-sla-deepdive` | `notebooks/03_warehouse_sla_deepdive.ipynb`<br>`reports/figures/seller_dispatch_sla_distribution.png` |
| **Akhila Nair** | `akhila-nair2005` | Regional Root-Cause Analysis & High-Risk Corridors | `feature/akhila-regional-rootcause` | `notebooks/03_regional_rootcause_analysis.ipynb`<br>`reports/figures/high_risk_corridors_deepdive.png` |
| **Adbot** | `adbot-47` | Weekend Dispatch Cut-Off Policy & Peak Surge Simulation | `feature/adbot-cutoff-and-seasonality` | `notebooks/03_cutoff_and_seasonality_simulation.ipynb`<br>`reports/figures/weekend_cutoff_simulation.png` |
| **Bhagyashree** | `Bhagyashree-2004` | Bulky Category Dynamics & Dynamic Promise Modeling | `feature/bhagyashree-bulky-freight-dynamics` | `notebooks/03_bulky_category_dynamics.ipynb`<br>`reports/figures/dynamic_promise_buffer_simulation.png` |

---

## 📅 Daily Commit Targets (Monday – Friday)

```text
Day 1 (Mon): Branch Setup, Issue Isolation & Hypothesis Formulation
Day 2 (Tue): Granular Root-Cause Filtering & Duration Split Metrics
Day 3 (Wed): Simulation / Risk Modeling & Trend Evaluation
Day 4 (Thu): Actionable Metric Quantification & Visualization
Day 5 (Fri): Operational Recommendations & Pull Request to Main
```

---

## 📋 Detailed Task Breakdown by Team Member

### 1. Aman Shakil (`dog098263-ui`) — Prioritized Issue Matrix & Executive Recommendations
* **Goal**: Synthesize cross-functional findings into a business-weighted issue matrix and draft executive operational recommendations.
* **Daily Plan**:
  * **Day 1**: Formalize issue prioritization methodology: $\text{Priority Score} = \text{Volume Affected} \times \text{Avg. Delay Days} \times \text{Rating Degradation Penalty}$.
  * **Day 2**: Build `src/prioritize_issues.py` ranking the top operational bottlenecks (Weekend dispatch, RJ regional corridor, Bulky furniture SLA).
  * **Day 3**: Export `reports/prioritized_issue_list.csv` with quantitative impact metrics.
  * **Day 4**: Draft `reports/week3_operational_recommendations.md` detailing operational follow-up actions and expected KPI uplifts.
  * **Day 5**: Review team pull requests on GitHub and merge into `main`.

### 2. Abhijith V (`Me-Abhijith-V`) — Warehouse Dispatch Bottlenecks & Seller SLA
* **Goal**: Evaluate chronic merchant packaging delays ($>4.0$ days) and deadline compliance.
* **Daily Plan**:
  * **Day 1**: Create `notebooks/03_warehouse_sla_deepdive.ipynb` and isolate orders with dispatch latency $>3$ days.
  * **Day 2**: Analyze distribution of `shipping_limit_date` breaches and quantify their impact on cancellation rates.
  * **Day 3**: Segment sellers by dispatch compliance tiers (Consistently Fast, Average, Chronic Laggers).
  * **Day 4**: Model the impact of a seller penalty/reward policy (simulating OTD uplift if chronic laggers improved to median speed).
  * **Day 5**: Save `reports/figures/seller_dispatch_sla_distribution.png` and open Pull Request.

### 3. Akhila Nair (`akhila-nair2005`) — Regional Root-Cause & High-Risk Corridors
* **Goal**: Investigate regional delay anomalies (especially Rio de Janeiro and Bahia).
* **Daily Plan**:
  * **Day 1**: Create `notebooks/03_regional_rootcause_analysis.ipynb` focusing on destination states with delay rates $>12\%$.
  * **Day 2**: Compare local carrier transit times within Rio de Janeiro (RJ) vs. São Paulo (SP) to isolate last-mile infrastructure bottlenecks.
  * **Day 3**: Evaluate freight cost vs. delivery duration trade-offs across distance bands.
  * **Day 4**: Quantify the impact of establishing regional staging hubs or alternative carrier partnerships in high-delay regions.
  * **Day 5**: Save `reports/figures/high_risk_corridors_deepdive.png` and open Pull Request.

### 4. Adbot (`adbot-47`) — Weekend Dispatch Cut-Off Policy & Peak Seasonality
* **Goal**: Quantify weekend dispatch delays and model operational cut-off improvements.
* **Daily Plan**:
  * **Day 1**: Create `notebooks/03_cutoff_and_seasonality_simulation.ipynb`.
  * **Day 2**: Measure the exact latency penalty for orders placed after Friday 2:00 PM vs. Thursday morning orders.
  * **Day 3**: Simulate the effect of a weekend dispatch policy (quantifying days saved if carriers picked up parcels on Saturdays).
  * **Day 4**: Deep dive into the Black Friday 2017 volume spike: quantify how long the backlog took to clear.
  * **Day 5**: Save `reports/figures/weekend_cutoff_simulation.png` and open Pull Request.

### 5. Bhagyashree (`Bhagyashree-2004`) — Bulky Category Dynamics & Dynamic Promise Modeling
* **Goal**: Protect customer satisfaction in complex freight categories (Furniture, Heavy Appliances).
* **Daily Plan**:
  * **Day 1**: Create `notebooks/03_bulky_category_dynamics.ipynb` isolating heavy categories ($>5\text{ kg}$).
  * **Day 2**: Compare promised delivery dates against actual delivery duration for bulky vs. small parcels.
  * **Day 3**: Simulate dynamic promised delivery windows (e.g. adding 3–5 days buffer to bulky categories at checkout).
  * **Day 4**: Quantify how many orders shift from "Delayed" to "On-Time" under dynamic buffering, and the resulting review score protection.
  * **Day 5**: Save `reports/figures/dynamic_promise_buffer_simulation.png` and open Pull Request.

---

## 🛠 Daily Git Protocol

```bash
# Morning: Fetch latest changes from main
git checkout main
git pull origin main
git checkout -b feature/<your-assigned-week3-branch>

# Evening: Stage, commit, and push
git add .
git commit -m "feat: [detailed description of today's work]"
git push -u origin feature/<your-assigned-week3-branch>
```
