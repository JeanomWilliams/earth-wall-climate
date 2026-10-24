# Earth and Concrete-Block Walls in Abuja: Material Comparison

A personal research project by Jeanom Christiana Williams, published openly. It compares documented data on earthen and concrete-block walls and records the limits of the evidence. TERRA is named only as the context for the author's interest.
Author: Jeanom Christiana Williams.

## Key findings

- **Measured indoor response (Ouagadougou, 2025):** the typical indoor daily swing is 4.7 °C, against 10.9 °C outdoors. The median damping ratio (indoor swing ÷ outdoor swing) is 0.42. The indoor air averaged 32.2 °C against 29.3 °C outdoors, and the indoor peak typically falls about two hours after the outdoor peak.
- **Ventilation:** in a published study of two pilot buildings in Ouagadougou, plaster, airtight openings and scheduled ventilation reduced discomfort from about 80% to about 33% (earth block) and 36% (cement block). The choice of wall made a difference of about two percentage points; the ventilation measures made far more.
- **Abuja climate (NASA POWER reanalysis, Feb–Apr 2026):** the average day swings 13.5 °C, from 23.2 °C at 05:00 to 36.7 °C at 13:00. The hottest day reached 41.0 °C.
- **Materials:** the embodied-carbon comparison is partial. The CEB total (15.4 kg CO₂ per m² of 300 mm wall) has an unknown boundary. The concrete-block figure (15.1–18.8 kg CO₂ per m² of face) is a cement-only lower bound.
- **Limits:** there is no measured Abuja data; the Nigerian block standard (NIS 87) was not consulted; CEB stabilisation is not stated; and no measured night-ventilation rate exists for the hot-dry Sahel.
- **Method note:** a first-order thermal model was tested against the measured Ouagadougou dwelling. It reproduced the mean temperature but not the daily swing, so its results are not reported as findings.

## Question

Which wall materials are supported by documented data for Abuja and comparable West African conditions, and what do they cost in embodied carbon?

## What this repository contains

- `climate_summary.py`: reads the NASA POWER hourly file and writes the Abuja climate dashboard, a data table and a written account of the season.
  - Outputs: `outputs/climate_dashboard.png` (four panels: every hour of the season, the average day, each day's extremes, and the monthly spread), `outputs/climate_summary.csv`, and `outputs/climate_story.md`.
  - Every figure in the story is calculated from the data by the script.
- `indoor_response.py`: analyses a measured indoor dataset for an earth-block dwelling in Ouagadougou (2025). It calculates, for each day, the outdoor and indoor swing, the damping ratio and the peak delay.
  - Input: `data/temperatures_mesurees_2025_clean.csv`, from N'Guiro et al. (2026), doi:10.7910/DVN/BZBGJK, CC0. Download it from that DOI and place it in `data/`.
  - Outputs: `outputs/indoor_response_daily.csv`, `outputs/indoor_response_monthly.csv`, `outputs/indoor_response_dashboard.png`, `outputs/indoor_response_story.md`.
- `material_comparison.py`: calculates conduction resistance and heat capacity for each wall option, and embodied carbon per square metre of wall face.
  - Output: `outputs/material_comparison.csv`, `outputs/embodied_carbon.png`.
- `docs/methodology_notes.md`: each input, its source and its status.

**Climate data.** Download the NASA POWER file and save it as `data/abuja_hourly.csv`:
1. Go to https://power.larc.nasa.gov/data-access-viewer/
2. Select Single Point, Hourly. Enter latitude 9.07 and longitude 7.40.
3. Select parameter T2M (temperature at 2 metres) and the period 1 February to 30 April 2026.
4. Download as CSV and save to `data/abuja_hourly.csv`.

The `data/` folder is included in the repository. `climate_summary.py` stops with an error if the file is missing.

**Run:** `python climate_summary.py` and `python material_comparison.py` from the repository root. Each needs only the packages in `requirements.txt`; `climate_summary.py` also needs the data file.

## Measured indoor response (Ouagadougou, 2025)

- The living room averaged 32.2 °C against 29.3 °C outside: about 2.9 °C warmer over the year. The data does not show the cause.
- The typical day swings 10.9 °C outdoors and 4.7 °C indoors (median damping ratio 0.42). The 4.7 °C is the median of the 365 daily indoor swings; the 4.6 °C quoted in the validation check (methodology notes, section 6) is the mean of the same daily swings.
- The indoor peak typically falls about 2 hours after the outdoor peak (15:00 outdoors, 17:00 indoors).
- The three warmest months are April, March and May, and damping is similar in those months and the rest of the year.

This is one dwelling in Ouagadougou, not Abuja. Its outdoor input is a weather file, not a measurement. The full account is in `outputs/indoor_response_story.md`.

## Climate (NASA POWER, Abuja, 1 Feb to 30 Apr 2026)

- The average day ranges from 23.2 °C at 05:00 to 36.7 °C at 13:00.
- The hottest day was 16 February (41.0 °C). The coolest night was 1 March (18.8 °C).
- The mean daily swing is 13.6 °C; the widest swing was 19.9 °C on 8 March.
- Monthly means: February 29.5 °C, March 30.3 °C, April 28.4 °C.

The full account is in `outputs/climate_story.md`. These are reanalysis values (MERRA-2), not station measurements.

## Results

**Thermal cases (per square metre of wall face; each case keeps its own source)**

| Case | Source | k (W/m·K) | ρ (kg/m³) | cp (J/kg·K) | Thickness | R (m²K/W) | C (kJ/m²K) |
|---|---|---|---|---|---|---|---|
| CEB A | Auroville CSEB table (2005) | 0.81–0.93 | 1800 | 650–850 | 300 mm | 0.32–0.37 | 351–459 |
| CEB B | Ouedraogo et al. (2024), Table 1 | 1.02 | 1840 | 975 | 140 mm | 0.137 | 251 |
| Cement block C | Ouedraogo et al. (2024), Table 1 | 0.80 | 1000 | 1000 | 150 mm | 0.187 | 150 |
| Concrete block D | Nigerian sandcrete measurements (density only) | not established | 1614–2002 | 1000 (from C) | 225 mm | not calculated | 363–450 |

Case C and case B come from the same study's Table 1 and are initial model inputs, not measured values. Case D has no verified conductivity, so its resistance is not calculated.

**Embodied carbon (kg CO₂ per m² of wall face)**

| Wall | Value | Basis |
|---|---|---|
| CEB 300 mm | 15.4 | Auroville Earth Institute data; boundary and cement content not stated |
| Concrete block 225 mm, cement only | 15.1–18.8 | Cement content from 20–25 blocks per bag; 0.763 kg CO₂/kg cement |
| Dense concrete block 140 mm, reference | 14.8 | IBU EPD, A1–A3, Holcim UK |

The cement-only figure for the 225 mm block is a lower bound. Its total impact, including sand, water, transport and manufacture, is higher. The 140 mm reference is a different product and thickness, so it is shown for comparison only.

## Availability in Abuja and West Africa

| Item | Finding | Source | Status |
|---|---|---|---|
| Cement price, Nigeria 2026 | ₦9,300–9,700 per 50 kg bag (January); ₦13,000–15,000 in some regions (July) | FCCPC figures, reported by Africa Intelligence and The Guardian | Regulator-based; commercial price sites excluded |
| CEB presses | Sold by overseas manufacturers, about USD 980–13,500 | Manufacturer listings | Listings only |
| CEB supplier in Abuja | None verified | Not found | Gap |
| Concrete block machines, Abuja | ₦850,000–1,350,000 | Jiji listings | Listings only |

## Gaps

- No verified CEB supplier in Abuja.
- The CEB stabilisation level and cement content are not stated in the Auroville source.
- The NIS 87 standard for sandcrete blocks was not accessed. Block widths of 150 and 225 mm come from secondary sources.
- No measured night-ventilation rate for hot-dry climates was found.

## Scope

This repository compares materials. It does not simulate a room. An earlier dynamic model was tested against a measured dwelling in Ouagadougou. It reproduced the mean indoor temperature but not the daily swing (0.7 °C modelled, 4.6 °C measured), so its wall-performance and comfort results are not reported here.

## Data sources

- Auroville Earth Institute. Compressed stabilised earth block basic data. earth-auroville.com
- IBU EPD, Holcim UK Masterdenz 140 7.3N, 2025. ibu-epd.com
- ECO Platform EPD EPDIE-21-52, CEM I Portland cement, 2022. Cement Manufacturers Ireland.
- Nigerian sandcrete block studies (cement content per bag, and measured densities).
- Ouedraogo et al. (2024), Optimisation of thermal comfort in a hot and dry tropical climate, JMMCE 12, 1–16, doi:10.4236/jmmce.2024.121001. Table 1 values for CEB and cement block.
- FCCPC cement price figures, reported in 2026 press coverage.

## Comparable study (Ouedraogo et al., 2024)

Two pilot buildings at 2iE, Kamboinsé, Ouagadougou, were monitored from September to November 2017 (validation over the typical week of 12–18 November 2017). Before any change, both buildings were uncomfortable for about 80% of the year. After plaster, airtight openings and scheduled ventilation, discomfort fell to 33.3% for CEB and 35.7% for cement block. The authors attribute the CEB advantage to thermal inertia. The result supports the view that ventilation changes comfort more than wall choice.

## Standard not consulted

Block widths of 150 mm and 225 mm are taken from secondary sources that quote the Nigerian sandcrete block standard (NIS 87). The standard itself was not consulted, and the edition in force (NIS 87:2000, NIS 87:2007 or NIS 978:2017) has not been confirmed. Values drawn from it should be checked against the standard before any dimension is used for design.

## Use of AI tools

Claude (Anthropic) assisted with script development, verification runs, and drafting of the documentation. The research question, the choice of sources, the interpretation of results, and the decision to report the failed validation are the author's. All values were checked against the cited sources, and any value that could not be checked is stated as a gap.
