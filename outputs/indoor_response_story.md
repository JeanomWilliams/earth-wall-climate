# How the dwelling responded in 2025

*Every figure below is calculated by `indoor_response.py` from the measured file. The dwelling is in Ouagadougou, Burkina Faso.*

## The year

The file holds 8,760 hourly indoor readings from one full year, 2025, and 365 complete days were analysed. The living room averaged 32.2 °C, against 29.3 °C outside. The dwelling was on average 2.9 °C warmer than the air around it. That is the most important finding in this analysis, and the data does not show why. Heat from occupants, appliances, the roof, or limited ventilation are all possible, and the file cannot separate them.

## The day

Outdoors, the typical day swings by 10.9 °C. Indoors, the typical swing is 4.7 °C. The outdoor air typically peaks at 15:00, and the indoor air typically peaks at 17:00. The median delay is 2 hours, so the dwelling shifts the peak by a short interval rather than delaying it into the evening.

## The damping

The damping ratio is indoor swing divided by outdoor swing. The median across the year is 0.42, so the dwelling passes on about 42% of the daily outdoor swing. In the hottest months (March to May) the median is 0.39; in the other months it is 0.42. The difference is small, so the damping is broadly similar through the year.

## The seasons

The three warmest months by outdoor average are April, March, May. These are the months in which the indoor air is warmest in absolute terms, not just in swing.

## The relationship

Across all days, the indoor swing rises by about 0.33 °C for every 1 °C of outdoor swing (r = 0.71). A slope well below 1 means the dwelling passes on only part of the outdoor swing. This describes the relationship in this one dwelling, not the mechanism behind it.

## What this does not show

- The result is for one dwelling in Ouagadougou. It does not describe Abuja, and it does not separate the effects of the walls, roof and ventilation.
- The outdoor column is a weather-file input, not a measurement, so the damping depends on that input's accuracy.
- The file was assembled from separate records. Daily values are calculated within each day, so the join does not affect them, but comparisons across it should be treated with care.

## Source

N'Guiro, S.M., Messan, A., Attia, S. (2026). Dataset for Thermal Performance Assessment of One-Bedroom (F2) Reference Dwelling in Burkina Faso. Harvard Dataverse, doi:10.7910/DVN/BZBGJK. CC0 1.0.
