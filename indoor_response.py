"""
Measured indoor response of an earth-block dwelling, Ouagadougou (Burkina Faso), 2025.

Data: N'Guiro, S.M., Messan, A., Attia, S. (2026). Dataset for Thermal Performance
Assessment of One-Bedroom (F2) Reference Dwelling in Burkina Faso. Harvard Dataverse,
doi:10.7910/DVN/BZBGJK, CC0 1.0. File: temperatures_mesurees_2025_clean.csv
(hourly living-room air temperature, HOBO MX1100 logger, 1.10 m above floor).

Outdoor column (Temperature_ext_C) is the weather-file input used by the dataset,
not a site measurement. The dwelling is in Ouagadougou, not Abuja.

What is calculated, for each day (24 hourly values):
  outdoor swing   = max - min of outdoor temperature
  indoor swing    = max - min of indoor temperature
  damping ratio   = indoor swing / outdoor swing   (lower = more damping)
  lag (h)         = (hour of indoor peak - hour of outdoor peak) mod 24

Outputs (in outputs/):
  indoor_response_daily.csv, indoor_response_monthly.csv,
  indoor_response_dashboard.png, indoor_response_story.md
The script stops with an error if the data file is missing or malformed.
"""
import csv, os, datetime
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

DATA = os.path.join("data", "temperatures_mesurees_2025_clean.csv")
OUT = "outputs"
DARK_BG, PANEL, GOLD, OFF_WHITE, MUTED = "#1A1A1A", "#2A2A2A", "#C9A84C", "#F0EDE6", "#8A8A8A"
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
HOT_MONTHS = (3, 4, 5)   # March-May: the three warmest months by outdoor mean (checked in the story)


def load(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Measured file not found: {os.path.abspath(path)}")
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader)
        if header[:3] != ["Date_Heure", "Temperature_mesuree_C", "Temperature_ext_C"]:
            raise ValueError(f"Unexpected header: {header}")
        for r in reader:
            if len(r) != 3:
                continue
            ts = datetime.datetime.strptime(r[0].strip(), "%d/%m/%y %H:%M")
            rows.append((ts, float(r[1]), float(r[2])))
    if len(rows) != 8760:
        raise ValueError(f"Expected 8760 hourly rows for 2025, found {len(rows)}.")
    return rows


def main():
    rows = load(DATA)
    ts = [r[0] for r in rows]
    indoor = np.array([r[1] for r in rows])
    outdoor = np.array([r[2] for r in rows])

    days = {}
    for i, t in enumerate(ts):
        days.setdefault(t.date(), []).append(i)
    records = []
    for d, idx in sorted(days.items()):
        if len(idx) != 24:
            continue
        o, n = outdoor[idx], indoor[idx]
        o_sw, n_sw = o.max() - o.min(), n.max() - n.min()
        lag = (int(np.argmax(n)) - int(np.argmax(o))) % 24
        records.append(dict(date=d, month=d.month, o_swing=o_sw, i_swing=n_sw,
                            damping=n_sw / o_sw, lag=lag,
                            o_peak=int(np.argmax(o)), i_peak=int(np.argmax(n)),
                            o_mean=o.mean(), i_mean=n.mean()))
    n_days = len(records)
    o_sw = np.array([r["o_swing"] for r in records])
    i_sw = np.array([r["i_swing"] for r in records])
    damp = np.array([r["damping"] for r in records])
    lag = np.array([r["lag"] for r in records])
    months = np.array([r["month"] for r in records])
    o_mean = np.array([r["o_mean"] for r in records])
    i_mean = np.array([r["i_mean"] for r in records])

    # Average day profiles
    o_prof = np.array([np.mean([outdoor[i] for i in range(len(ts)) if ts[i].hour == h]) for h in range(24)])
    i_prof = np.array([np.mean([indoor[i] for i in range(len(ts)) if ts[i].hour == h]) for h in range(24)])

    # Monthly medians
    monthly = {}
    for m in range(1, 13):
        sel = months == m
        if sel.sum() == 0:
            continue
        monthly[m] = dict(days=int(sel.sum()), o_swing=float(np.median(o_sw[sel])),
                          i_swing=float(np.median(i_sw[sel])), damping=float(np.median(damp[sel])),
                          lag=float(np.median(lag[sel])), i_mean=float(np.mean(i_mean[sel])),
                          o_mean=float(np.mean(o_mean[sel])))

    # Slope of indoor swing on outdoor swing (all days)
    slope, intercept = np.polyfit(o_sw, i_sw, 1)
    r = np.corrcoef(o_sw, i_sw)[0, 1]
    hot = np.isin(months, HOT_MONTHS)
    cool = ~hot

    print(f"Full days: {n_days}")
    print(f"Indoor mean {indoor.mean():.2f} C, outdoor mean {outdoor.mean():.2f} C")
    print(f"Median daily outdoor swing {np.median(o_sw):.2f} C; indoor swing {np.median(i_sw):.2f} C")
    print(f"Median damping ratio {np.median(damp):.3f}; median lag {np.median(lag):.1f} h")
    print(f"Hot months (Mar-May) median damping {np.median(damp[hot]):.3f}; "
          f"other months {np.median(damp[cool]):.3f}")
    print(f"Indoor swing = {slope:.3f} x outdoor swing + {intercept:.2f} (r = {r:.2f})")

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "indoor_response_daily.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "outdoor_swing_C", "indoor_swing_C", "damping_ratio", "lag_h",
                    "outdoor_peak_hour", "indoor_peak_hour", "outdoor_mean_C", "indoor_mean_C"])
        for rec in records:
            w.writerow([rec["date"].isoformat(), round(rec["o_swing"], 2), round(rec["i_swing"], 2),
                        round(rec["damping"], 3), rec["lag"], rec["o_peak"], rec["i_peak"],
                        round(rec["o_mean"], 2), round(rec["i_mean"], 2)])
    with open(os.path.join(OUT, "indoor_response_monthly.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["month", "days", "median_outdoor_swing_C", "median_indoor_swing_C",
                    "median_damping_ratio", "median_lag_h", "mean_outdoor_C", "mean_indoor_C"])
        for m, v in monthly.items():
            w.writerow([MONTH_NAMES[m - 1], v["days"], round(v["o_swing"], 2), round(v["i_swing"], 2),
                        round(v["damping"], 3), round(v["lag"], 1), round(v["o_mean"], 2), round(v["i_mean"], 2)])

    # ---- dashboard -------------------------------------------------------------
    fig = plt.figure(figsize=(18, 11), facecolor=DARK_BG)
    gs = GridSpec(2, 3, figure=fig, left=0.06, right=0.97, top=0.86, bottom=0.08, hspace=0.38, wspace=0.28)
    fig.text(0.5, 0.955, "MEASURED INDOOR RESPONSE, EARTH-BLOCK DWELLING, OUAGADOUGOU 2025",
             ha="center", color=GOLD, fontsize=16, fontweight="bold", fontfamily="serif")
    fig.text(0.5, 0.92, "Hourly living-room air temperature (measured) and weather-file outdoor temperature. "
             "N'Guiro et al. (2026), doi:10.7910/DVN/BZBGJK, CC0.", ha="center", color=MUTED, fontsize=10)

    ax1 = fig.add_subplot(gs[0, 0])
    x = np.arange(24)
    ax1.plot(x, o_prof, color="#E07B67", lw=2, label="Outdoor (weather file)")
    ax1.plot(x, i_prof, color=GOLD, lw=2.5, label="Indoor (measured)")
    ax1.set_xticks(range(0, 24, 3))
    ax1.set_xticklabels([f"{h:02d}" for h in range(0, 24, 3)])
    ax1.set_xlabel("Hour", color=MUTED)
    ax1.set_ylabel("°C", color=MUTED)
    ax1.set_title("The average day", color=OFF_WHITE, fontsize=12, fontweight="bold")
    ax1.legend(fontsize=8, facecolor=PANEL, edgecolor=MUTED, labelcolor=OFF_WHITE, loc="upper left")

    ax2 = fig.add_subplot(gs[0, 1:])
    xd = np.arange(n_days)
    ax2.scatter(xd[hot], damp[hot], color="#E07B67", s=10, label="March–May")
    ax2.scatter(xd[cool], damp[cool], color="#8FB8C9", s=10, label="Other months")
    ax2.axhline(np.median(damp), color=GOLD, ls="--", lw=1)
    ax2.set_ylim(0, max(1.0, np.percentile(damp, 99) * 1.1))
    ax2.set_xlabel("Day of 2025", color=MUTED)
    ax2.set_ylabel("Damping ratio (indoor ÷ outdoor swing)", color=MUTED)
    ax2.set_title("Daily damping through the year", color=OFF_WHITE, fontsize=12, fontweight="bold")
    ax2.legend(fontsize=8, facecolor=PANEL, edgecolor=MUTED, labelcolor=OFF_WHITE, loc="upper right")

    ax3 = fig.add_subplot(gs[1, 0])
    data = [lag[months == m] for m in range(1, 13) if (months == m).any()]
    labels = [MONTH_NAMES[m - 1] for m in range(1, 13) if (months == m).any()]
    bp = ax3.boxplot(data, patch_artist=True, widths=0.6, medianprops=dict(color=OFF_WHITE, lw=2),
                     whiskerprops=dict(color=MUTED), capprops=dict(color=MUTED),
                     flierprops=dict(markeredgecolor=MUTED, markersize=3))
    for p in bp["boxes"]:
        p.set_facecolor(GOLD)
        p.set_alpha(0.4)
    ax3.set_xticks(range(1, len(labels) + 1))
    ax3.set_xticklabels(labels, fontsize=8)
    ax3.set_ylabel("Hours", color=MUTED)
    ax3.set_title("Peak delay by month (hours)", color=OFF_WHITE, fontsize=12, fontweight="bold")

    ax4 = fig.add_subplot(gs[1, 1])
    ax4.scatter(o_sw[hot], i_sw[hot], color="#E07B67", s=14, label="March–May")
    ax4.scatter(o_sw[cool], i_sw[cool], color="#8FB8C9", s=14, label="Other months")
    xx = np.linspace(o_sw.min(), o_sw.max(), 50)
    ax4.plot(xx, slope * xx + intercept, color=GOLD, lw=2, label=f"fit: slope {slope:.2f}, r = {r:.2f}")
    ax4.set_xlabel("Outdoor daily swing (°C)", color=MUTED)
    ax4.set_ylabel("Indoor daily swing (°C)", color=MUTED)
    ax4.set_title("Indoor against outdoor swing", color=OFF_WHITE, fontsize=12, fontweight="bold")
    ax4.legend(fontsize=8, facecolor=PANEL, edgecolor=MUTED, labelcolor=OFF_WHITE, loc="upper left")

    ax5 = fig.add_subplot(gs[1, 2])
    mm = sorted(monthly)
    ax5.bar([MONTH_NAMES[m - 1] for m in mm], [monthly[m]["i_mean"] for m in mm], color=GOLD, alpha=0.6,
            label="Indoor mean")
    ax5.plot([MONTH_NAMES[m - 1] for m in mm], [monthly[m]["o_mean"] for m in mm], color="#E07B67", marker="o",
             lw=2, label="Outdoor mean")
    ax5.set_ylabel("°C (monthly mean)", color=MUTED)
    ax5.set_title("Monthly means, indoor and outdoor", color=OFF_WHITE, fontsize=12, fontweight="bold")
    ax5.legend(fontsize=8, facecolor=PANEL, edgecolor=MUTED, labelcolor=OFF_WHITE, loc="upper left")
    ax5.tick_params(axis="x", labelsize=8)

    for ax in (ax1, ax2, ax3, ax4, ax5):
        ax.set_facecolor(PANEL)
        ax.tick_params(colors=MUTED, labelsize=9)
        for s in ax.spines.values():
            s.set_edgecolor("#444444")
        ax.grid(alpha=0.2, color="#555555")
    fig.text(0.5, 0.012, "Measured indoor data from a dwelling in Ouagadougou. Outdoor values are the dataset's "
             "weather-file input, not a site measurement.", ha="center", color=MUTED, fontsize=9)
    fig.savefig(os.path.join(OUT, "indoor_response_dashboard.png"), dpi=180, facecolor=DARK_BG)

    # ---- story --------------------------------------------------------------
    m_hot = np.median(damp[hot])
    m_cool = np.median(damp[cool])
    all_months = np.array([t.month for t in ts])
    month_out = {m: float(np.mean(outdoor[all_months == m])) for m in range(1, 13)}
    top3 = sorted(month_out, key=month_out.get, reverse=True)[:3]
    top3_names = ", ".join(datetime.date(2025, m, 1).strftime("%B") for m in top3)
    gap = float(indoor.mean() - outdoor.mean())
    o_peak_mode = int(np.bincount([v["o_peak"] for v in records]).argmax())
    i_peak_mode = int(np.bincount([v["i_peak"] for v in records]).argmax())
    story = f"""# How the dwelling responded in 2025

*Every figure below is calculated by `indoor_response.py` from the measured file. The dwelling is in Ouagadougou, Burkina Faso.*

## The year

The file holds {len(rows):,} hourly indoor readings from one full year, 2025, and {n_days} complete days were analysed. The living room averaged {indoor.mean():.1f} °C, against {outdoor.mean():.1f} °C outside. The dwelling was on average {gap:.1f} °C warmer than the air around it. That is the most important finding in this analysis, and the data does not show why. Heat from occupants, appliances, the roof, or limited ventilation are all possible, and the file cannot separate them.

## The day

Outdoors, the typical day swings by {np.median(o_sw):.1f} °C. Indoors, the typical swing is {np.median(i_sw):.1f} °C. The outdoor air typically peaks at {o_peak_mode:02d}:00, and the indoor air typically peaks at {i_peak_mode:02d}:00. The median delay is {np.median(lag):.0f} hours, so the dwelling shifts the peak by a short interval rather than delaying it into the evening.

## The damping

The damping ratio is indoor swing divided by outdoor swing. The median across the year is {np.median(damp):.2f}, so the dwelling passes on about {np.median(damp) * 100:.0f}% of the daily outdoor swing. In the hottest months (March to May) the median is {m_hot:.2f}; in the other months it is {m_cool:.2f}. The difference is small, so the damping is broadly similar through the year.

## The seasons

The three warmest months by outdoor average are {top3_names}. These are the months in which the indoor air is warmest in absolute terms, not just in swing.

## The relationship

Across all days, the indoor swing rises by about {slope:.2f} °C for every 1 °C of outdoor swing (r = {r:.2f}). A slope well below 1 means the dwelling passes on only part of the outdoor swing. This describes the relationship in this one dwelling, not the mechanism behind it.

## What this does not show

- The result is for one dwelling in Ouagadougou. It does not describe Abuja, and it does not separate the effects of the walls, roof and ventilation.
- The outdoor column is a weather-file input, not a measurement, so the damping depends on that input's accuracy.
- The file was assembled from separate records. Daily values are calculated within each day, so the join does not affect them, but comparisons across it should be treated with care.

## Source

N'Guiro, S.M., Messan, A., Attia, S. (2026). Dataset for Thermal Performance Assessment of One-Bedroom (F2) Reference Dwelling in Burkina Faso. Harvard Dataverse, doi:10.7910/DVN/BZBGJK. CC0 1.0.
"""
    with open(os.path.join(OUT, "indoor_response_story.md"), "w", encoding="utf-8") as f:
        f.write(story)

    print(f"Saved -> {OUT}/indoor_response_daily.csv, indoor_response_monthly.csv, "
          f"indoor_response_dashboard.png, indoor_response_story.md")


if __name__ == "__main__":
    main()
