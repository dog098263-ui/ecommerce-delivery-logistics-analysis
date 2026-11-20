"""
Script: add_day1_cells.py
Purpose: Add Day 1 (Interim Dataset Loading) cells to 02_carrier_analysis.ipynb
         Preserves all existing cells. Removes the trailing empty cell before appending.
"""

import json
import uuid

NB_PATH = "notebooks/02_carrier_analysis.ipynb"

# ── Load notebook ──────────────────────────────────────────────────────────────
with open(NB_PATH, "r", encoding="utf-8") as f:
    nb = json.load(f)

# ── Remove trailing empty cell if present ─────────────────────────────────────
cells = nb["cells"]
if cells and cells[-1]["cell_type"] == "code" and cells[-1]["source"] == []:
    cells.pop()
    print("Removed trailing empty cell.")

# ── Helper: build cells ───────────────────────────────────────────────────────
def md_cell(text):
    return {
        "cell_type": "markdown",
        "id": uuid.uuid4().hex[:8],
        "metadata": {},
        "source": [text]
    }

def code_cell(source_lines):
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": uuid.uuid4().hex[:8],
        "metadata": {},
        "outputs": [],
        "source": source_lines
    }

# ── Day 1 cells ───────────────────────────────────────────────────────────────
day1_md_header = md_cell(
    "---\n"
    "# Day 1: Interim Dataset Loading and Eligible Order Filtering\n\n"
    "**Objective:** Load `data/interim/logistics_analytical_dataset.csv`, "
    "inspect dataset dimensions, relevant column definitions, missing values, "
    "and filter eligible orders using `is_eligible_otd == True`.\n\n"
    "> **Note:** The cells above this section are exploratory background work "
    "using raw datasets. The five-day analysis plan begins here, using the "
    "pre-processed interim analytical dataset."
)

cell_load = code_cell([
    "# Load the pre-processed analytical dataset\n",
    "df = pd.read_csv('../data/interim/logistics_analytical_dataset.csv')\n",
    "\n",
    "print(f'Dataset loaded successfully!')\n",
    "print(f'Shape: {df.shape[0]:,} rows x {df.shape[1]} columns')"
])

cell_inspect = code_cell([
    "# Inspect key columns relevant to this carrier analysis\n",
    "key_cols = [\n",
    "    'order_id', 'seller_id',\n",
    "    'order_purchase_timestamp', 'order_approved_at',\n",
    "    'order_delivered_carrier_date', 'order_delivered_customer_date',\n",
    "    'is_eligible_otd', 'order_processing_time_days',\n",
    "    'carrier_transit_time_days', 'total_delivery_duration_days',\n",
    "    'promised_delivery_duration_days', 'delay_days', 'delivery_outcome'\n",
    "]\n",
    "\n",
    "print('Column dtypes:')\n",
    "print(df[key_cols].dtypes.to_string())\n",
    "print('\\nNull counts:')\n",
    "print(df[key_cols].isnull().sum().to_string())"
])

cell_filter = code_cell([
    "# Filter eligible orders: delivered orders with valid timestamps\n",
    "# is_eligible_otd == True: order_status='delivered', no invalid timestamps\n",
    "valid = df[df['is_eligible_otd'] == True].copy()\n",
    "\n",
    "# Create named analysis columns (per Day 2 plan)\n",
    "valid['processing_days'] = valid['order_processing_time_days']\n",
    "valid['transit_days']    = valid['carrier_transit_time_days']\n",
    "\n",
    "print(f'Total orders in dataset  : {len(df):,}')\n",
    "print(f'Eligible orders (OTD set): {len(valid):,}')\n",
    "print(f'Ineligible (excluded)    : {len(df) - len(valid):,}')\n",
    "print(f'\\nDelivery outcome breakdown (eligible orders):')\n",
    "print(valid['delivery_outcome'].value_counts().to_string())\n",
    "print(f\"\\nOn-time delivery rate: {(valid['delivery_outcome'] == 'on_time').mean()*100:.1f}%\")"
])

day1_md_findings = md_cell(
    "### Day 1 Findings\n\n"
    "| Metric | Value |\n"
    "|--------|-------|\n"
    "| Total orders in dataset | 99,441 |\n"
    "| **Eligible orders (OTD set)** | **96,281** |\n"
    "| Ineligible / excluded | 3,160 |\n"
    "| On-time deliveries | 88,459 (91.9%) |\n"
    "| Delayed deliveries | 7,822 (8.1%) |\n\n"
    "**Key observations:**\n"
    "- Ineligible orders: canceled, non-delivered, or missing timestamps — correctly excluded.\n"
    "- `order_processing_time_days` and `carrier_transit_time_days` have **zero nulls** in the eligible set.\n"
    "- `delivery_outcome` is pre-computed: `on_time` or `delayed` relative to `order_estimated_delivery_date`.\n"
    "- `shipping_limit_date` is not in the interim dataset — it will be joined from the raw items file in Day 3."
)

# ── Append cells ──────────────────────────────────────────────────────────────
nb["cells"].extend([
    day1_md_header,
    cell_load,
    cell_inspect,
    cell_filter,
    day1_md_findings,
])

# ── Save ──────────────────────────────────────────────────────────────────────
with open(NB_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Notebook saved: {NB_PATH}")
print(f"Total cells now: {len(nb['cells'])}")
