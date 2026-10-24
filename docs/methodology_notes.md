# Methodology notes

## 0. Climate input

Hourly 2 m air temperature (T2M) from NASA POWER, derived from MERRA-2 reanalysis, local standard time, for Abuja (9.07 N, 7.40 E), 1 February to 30 April 2026. The file contains 2,136 hourly values with no missing data. `climate_summary.py` checks the count and rejects values outside -50 to 60 °C. Averages are taken over all days for each hour. Reanalysis is model-based and is not a station measurement.

## 1. Scope

The study compares documented material properties and embodied carbon for two wall types: compressed earth block (CEB) and concrete block. It does not simulate indoor temperature or comfort. The reason is stated in section 6.

## 2. Thermal calculation

- Conduction resistance: R = d / k, for thickness d and conductivity k.
- Heat capacity per square metre of wall face: C = ρ · cp · d.
- Ranges are computed for each combination of documented bounds. No single value is chosen.

## 3. Inputs and status

| Input | Value | Source | Status |
|---|---|---|---|
| CEB density | 1800 kg/m³ | Auroville Earth Institute CSEB table, class B/C | Documented |
| CEB conductivity | 0.81–0.93 W/m·K | Auroville CSEB table | Documented |
| CEB specific heat | 650–850 J/kg·K | Auroville CSEB table, written "KJ/Kg" | Documented; unit label to check |
| CEB embodied carbon | 51.5 kg CO₂/m³ | Auroville CSEB data, 2005 | Documented; boundary and cement content unknown |
| Block density | 1614–2002 kg/m³ | Nigerian sandcrete measurements | Documented (three studies) |
| Block conductivity | Not established | No verified Nigerian value; Ouedraogo (2024) Table 1 gives 0.80 W/m·K for cement block, a model input | Not used for resistance |
| Block specific heat | 1000 J/kg·K | Ouedraogo et al. (2024), Table 1, cement block (model input) | Documented in source; applied to Nigerian density range |
| CEB (Ouedraogo, case B) | k 1.02 W/m·K, ρ 1840 kg/m³, cp 975 J/kg·K, 14 cm, 8% cement | Ouedraogo et al. (2024), Table 1 | Initial model input |
| Cement block (case C) | k 0.80 W/m·K, ρ 1000 kg/m³, cp 1000 J/kg·K, 15 cm | Ouedraogo et al. (2024), Table 1 | Initial model input |
| Block thickness | 225 mm | Secondary sources quoting NIS 87 | Not verified against the standard |
| Embodied carbon, dense block | 14.8 kg CO₂e/m² of 140 mm | IBU EPD, Holcim UK, A1–A3 | Documented; different product |
| Cement factor | 0.763 kg CO₂e/kg | ECO Platform EPDIE-21-52, A1–A3 | Documented |
| Cement per block | 2.0–2.5 kg | Nigerian sandcrete study, 20–25 blocks per 50 kg bag | Documented; block size assumed as 225 × 225 × 450 mm |

## 3a. Monitoring period of the comparable study

The Ouedraogo et al. (2024) pilot buildings were monitored from September to November 2017, not 2024. The validation used the typical week of 12–18 November 2017. Discomfort was about 80% for both buildings before modification, and 33.3% (CEB) and 35.7% (cement block) after plaster, airtight openings and scheduled ventilation.

## 4. Embodied carbon calculation

- CEB per m² of 300 mm wall: 51.5 × 0.300 = 15.4 kg CO₂.
- Concrete block cement-only per m² of face: cement per block × 0.763 ÷ face area (0.450 × 0.225 m). This gives 15.1–18.8 kg CO₂.
- The cement-only value is a lower bound on the block's total impact.

## 5. Interpretation limits

- The CEB and block figures are per square metre of wall face, but the thicknesses differ (300 mm and 225 mm). Thickness is not normalised.
- The CEB boundary is unknown, so the CEB and block totals may not be on the same basis.
- The IBU reference is a dense block of a different product, shown only for context.
- Thermal ranges are conduction-only. They do not include surface resistances, air movement or thermal storage behaviour.

## 6. Why the dynamic model is not reported

A first-order room model was tested against measured indoor temperatures of a naturally ventilated dwelling in Ouagadougou, using the dataset's outdoor input. The model matched the mean (NMBE −9.1%, CVRMSE 11.0%, within ASHRAE Guideline 14 hourly limits) but not the daily swing: 0.7 °C modelled against 4.6 °C measured (the mean of daily indoor swings; the median reported in the measured-data analysis is 4.7 °C). The model omits roof gains, ventilation and internal gains, and the dwelling's walls (14 cm CEB, 15 cm block) differ from the comparison walls. Its swing and comfort results are therefore not used.

## 7. Open items

- Obtain the dwelling's material properties table to validate with the dwelling's own wall inputs.
- Confirm the NIS 87 block dimensions against the standard.
- Obtain a documented CEB stabilisation level and cement content.
- Find a verified CEB supplier in Abuja.
- Find a measured night-ventilation rate for a hot-dry climate.

## Standard not consulted

Block widths of 150 mm and 225 mm are taken from secondary sources that quote the Nigerian sandcrete block standard (NIS 87). The standard itself was not consulted, and the edition in force (NIS 87:2000, NIS 87:2007 or NIS 978:2017) has not been confirmed. Values drawn from it should be checked against the standard before any dimension is used for design.

## Use of AI tools

Claude (Anthropic) assisted with script development, verification runs, and drafting of the documentation. The research question, the choice of sources, the interpretation of results, and the decision to report the failed validation are the author's. All values were checked against the cited sources, and any value that could not be checked is stated as a gap.
