# Scripts Directory

This directory contains all Python scripts for the Dickson polynomial value set research, organized by functional category.

## Directory Structure

### data_generation/
**Purpose:** Generate raw data for reversed Dickson polynomial value sets

- **Test.py** - Main data generation script
  - Computes D_n(1, x) for all x ∈ F_p using reversed recurrence relation
  - Generates data for primes 3 to 97
  - Outputs:
    - `data/reversed_dickson_values.csv` - Raw data (p, n, cardinality, values)
    - `data/reversed_dickson_values_by_cardinality.csv` - Sorted by cardinality
  - Usage: `python scripts/data_generation/Test.py`

### analysis/
**Purpose:** Analyze patterns and derive formulas from generated data

- **analyze_cardinality_2.py** - Initial discovery of cardinality=2 patterns
  - Extracts all (p,n) pairs where value set has exactly 2 elements
  - Groups indices by prime to identify patterns
  
- **analyze_remaining_patterns.py** - Investigates non-twin prime patterns
  - Analyzes indices that don't fit twin prime formula
  - Helps identify Formula 2 and Formula 3
  
- **derive_all_formulas.py** - Polynomial regression to derive all three formulas
  - Uses numpy.polyfit to find exact polynomial coefficients
  - Derives: n = 0.5p² + 0.5, n = p² - 1, n = 0.5p² + p - 0.5
  
- **derive_formula.py** - Single formula derivation with detailed output
  - Focuses on third formula derivation
  - Writes results to `output/results/formula_results.txt`

### verification/
**Purpose:** Verify formulas and theoretical predictions

- **verify_all_formulas_exact.py** - Exact verification with RMSE=0
  - Verifies all three formulas produce exactly matching indices
  - Confirms no rounding errors (perfect integer matches)
  - Primary verification script
  
- **verify_cardinality_2_patterns.py** - Pattern consistency checks
  - Verifies formulas across all primes in dataset
  
- **verify_value_sets.py** - Theoretical value set verification
  - Computes actual D_n(1, x) values using reversed recurrence
  - Confirms Formula 1 and 3 → {1, p-1}
  - Confirms Formula 2 → {1, 2}
  - Validates mathematical proof predictions

### visualization/
**Purpose:** Create plots and interactive visualizations

- **plot_scatter.py** - Generate static scatter plots
  - Creates individual PNG plots for each prime
  - Outputs to `output/plots/scatter_p_{p}.png`
  
- **plot_cardinality_2_indices.py** - Static plot of cardinality=2 indices
  - Visualizes all three formulas on single plot
  - Outputs to `output/plots/cardinality_2_indices_plot.png`
  
- **plot_cardinality_2_interactive.py** - Interactive HTML visualization
  - Plotly-based interactive plot with hover details
  - Toggle between log/linear y-axis
  - Color-coded by formula
  - Outputs to `output/interactive/cardinality_2_indices_interactive.html`

### utilities/
**Purpose:** Helper scripts for printing and displaying results

- **print_cardinality_2_indices.py** - Print all cardinality=2 indices
  - Groups by prime p
  - Shows all three special indices per prime
  - Formatted console output
  
- **print_notes.py** - Display research notes
  - Prints `docs/methodology/research_notes.md` to console
  - Quick reference during development

## Workflow

### Standard Analysis Workflow:
1. Generate data: `python scripts/data_generation/Test.py`
2. Verify formulas: `python scripts/verification/verify_all_formulas_exact.py`
3. Verify value sets: `python scripts/verification/verify_value_sets.py`
4. Create visualization: `python scripts/visualization/plot_cardinality_2_interactive.py`

### Discovery/Research Workflow:
1. Generate data (as above)
2. Analyze patterns: `python scripts/analysis/analyze_cardinality_2.py`
3. Derive formulas: `python scripts/analysis/derive_all_formulas.py`
4. Verify: `python scripts/verification/verify_all_formulas_exact.py`

## Dependencies

All scripts require:
- Python 3.x
- pandas

Additional dependencies by category:
- **analysis/**: numpy (for polynomial fitting)
- **visualization/**: matplotlib, plotly

Install all dependencies:
```bash
pip install pandas numpy matplotlib plotly
```

## Notes

- All file paths in scripts use relative paths from the script location
- Data files are always read from `../../data/` (relative to script)
- Output files are written to `../../output/{plots|interactive|results}/`
- Scripts can be run from any directory as long as relative structure is maintained
