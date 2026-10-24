"""
Abuja hot-dry season climate, from NASA POWER hourly air temperature.

Source: NASA POWER, MERRA-2 reanalysis, 2 m air temperature (T2M), local standard
time, Abuja (9.07 N, 7.40 E), 1 Feb - 30 Apr 2026.
Download: https://power.larc.nasa.gov/data-access-viewer/
(Single point, Hourly, T2M, Lat 9.07, Lon 7.40, Feb-Apr 2026, CSV)
Save as data/abuja_hourly.csv. The file is not stored in this repository.

Outputs
  outputs/climate_dashboard.png   four-panel dashboard
  outputs/climate_summary.csv     hourly profile, daily extremes, monthly means
  outputs/climate_story.md        the narrative, with every figure taken from the data

The script stops with an error if the data file is missing or incomplete.
"""
import csv, os, datetime
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

DATA = os.path.join("data", "abuja_hourly.csv")
OUT_PNG = os.path.join("outputs", "climate_dashboard.png")
OUT_CSV = os.path.join("outputs", "climate_summary.csv")
OUT_MD = os.path.join("outputs", "climate_story.md")
EXPECTED_HOURS = 89 * 24

DARK_BG, PANEL, GOLD, OFF_WHITE, MUTED = "#1A1A1A", "#2A2A2A", "#C9A84C", "#F0EDE6", "#8A8A8A"
MONTHS = {2: "February", 3: "March", 4: "April"}


def load(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"NASA POWER file not found: {os.path.abspath(path)}. "
                                "See the download steps at the top of this script.")
    rows = []
    with open(path, newline="") as f:
        for r in csv.reader(f):
            if len(r) >= 5 and r[0].strip().isdigit() and len(r[0].strip()) == 4:
                try:
                    t = float(r[4])
                except ValueError:
                    continue
                if -50 < t < 60:
                    rows.append((int(r[1]), int(r[2]), int(r[3]), t))
    if len(rows) != EXPECTED_HOURS:
        raise ValueError(f"Expected {EXPECTED_HOURS} valid hours, found {len(rows)}.")
    return rows


def main():
    rows = load(DATA)
    month = np.array([r[0] for r in rows])
    day = np.array([r[1] for r in rows])
    hour = np.array([r[2] for r in rows])
    temp = np.array([r[3] for r in rows])

    dates = sorted(set((m, d) for m, d in zip(month, day)))
    n_days = len(dates)
    grid = np.full((24, n_days), np.nan)            # hour x day
    for j, (m, d) in enumerate(dates):
        for h in range(24):
            sel = (month == m) & (day == d) & (hour == h)
            grid[h, j] = temp[sel][0]

    profile = np.nanmean(grid, axis=1)
    p_min = np.nanmin(grid, axis=1)
    p_max = np.nanmax(grid, axis=1)
    d_max = np.nanmax(grid, axis=0)
    d_min = np.nanmin(grid, axis=0)
    d_swing = d_max - d_min
    d_mean = np.nanmean(grid, axis=0)
    labels = [datetime.date(2026, m, d).strftime("%d %b") for m, d in dates]

    peak_h, trough_h = int(np.argmax(profile)), int(np.argmin(profile))
    hottest, coolest = int(np.argmax(d_max)), int(np.argmin(d_min))
    widest, narrowest = int(np.argmax(d_swing)), int(np.argmin(d_swing))
    monthly = {m: temp[month == m] for m in (2, 3, 4)}
    warm_start = profile[12:18]
    # Hours from the mean night minimum (05:00) to the mean afternoon maximum (peak)
    hours_to_peak = (peak_h - trough_h) % 24

    # ---- dashboard -------------------------------------------------------------
    fig = plt.figure(figsize=(18, 11), facecolor=DARK_BG)
    gs = GridSpec(2, 3, figure=fig, left=0.06, right=0.97, top=0.86, bottom=0.08,
                  hspace=0.38, wspace=0.28)
    fig.text(0.5, 0.955, "ABUJA HOT-DRY SEASON, FEBRUARY-APRIL 2026", ha="center",
             color=GOLD, fontsize=17, fontweight="bold", fontfamily="serif")
    fig.text(0.5, 0.92, "Hourly air temperature, NASA POWER (MERRA-2 reanalysis), 9.07 N 7.40 E, local standard time",
             ha="center", color=MUTED, fontsize=10)

    # (1) Season heatmap
    ax1 = fig.add_subplot(gs[0, 0:2])
    im = ax1.imshow(grid, aspect="auto", origin="lower", cmap="YlOrRd",
                    extent=[0, n_days, -0.5, 23.5])
    ax1.set_yticks(range(0, 24, 3))
    ax1.set_yticklabels([f"{h:02d}:00" for h in range(0, 24, 3)])
    tick_idx = list(range(0, n_days, 7))
    ax1.set_xticks([i + 0.5 for i in tick_idx])
    ax1.set_xticklabels([labels[i] for i in tick_idx], rotation=0, fontsize=8)
    ax1.set_title("Every hour of the season (89 days)", color=OFF_WHITE, fontsize=12, fontweight="bold")
    cb = fig.colorbar(im, ax=ax1, pad=0.01, fraction=0.025)
    cb.set_label("°C", color=OFF_WHITE)
    cb.ax.tick_params(colors=MUTED)
    cb.outline.set_edgecolor(MUTED)

    # (2) Average day with hourly range
    ax2 = fig.add_subplot(gs[0, 2])
    x = np.arange(24)
    ax2.fill_between(x, p_min, p_max, color=GOLD, alpha=0.25, label="Hourly range, 89 days")
    ax2.plot(x, profile, color=GOLD, lw=2.5, label="Average day")
    ax2.axvline(peak_h, color="#E07B67", ls="--", lw=1)
    ax2.axvline(trough_h, color="#8FB8C9", ls="--", lw=1)
    ax2.annotate(f"peak {peak_h:02d}:00", (peak_h, profile[peak_h]), xytext=(4, 6),
                 textcoords="offset points", color="#E07B67", fontsize=9)
    ax2.annotate(f"minimum {trough_h:02d}:00", (trough_h, profile[trough_h]), xytext=(4, -14),
                 textcoords="offset points", color="#8FB8C9", fontsize=9)
    ax2.set_xticks(range(0, 24, 3))
    ax2.set_xticklabels([f"{h:02d}" for h in range(0, 24, 3)])
    ax2.set_xlabel("Hour (local)", color=MUTED)
    ax2.set_ylabel("°C", color=MUTED)
    ax2.set_title("The average day", color=OFF_WHITE, fontsize=12, fontweight="bold")
    ax2.legend(loc="upper left", fontsize=8, facecolor=PANEL, edgecolor=MUTED, labelcolor=OFF_WHITE)

    # (3) Daily extremes through the season
    ax3 = fig.add_subplot(gs[1, 0:2])
    xd = np.arange(n_days)
    ax3.fill_between(xd, d_min, d_max, color=GOLD, alpha=0.2)
    ax3.plot(xd, d_max, color="#E07B67", lw=1.8, label="Daily maximum")
    ax3.plot(xd, d_min, color="#8FB8C9", lw=1.8, label="Daily minimum")
    ax3.plot(xd, d_mean, color=OFF_WHITE, lw=1, ls=":", label="Daily mean")
    ax3.scatter([hottest, coolest], [d_max[hottest], d_min[coolest]], color=GOLD, zorder=5, s=28)
    ax3.annotate(f"hottest day {labels[hottest]}: {d_max[hottest]:.1f} °C",
                 (hottest, d_max[hottest]), xytext=(-150, 8), textcoords="offset points",
                 color=GOLD, fontsize=9)
    ax3.annotate(f"coolest night {labels[coolest]}: {d_min[coolest]:.1f} °C",
                 (coolest, d_min[coolest]), xytext=(8, -14), textcoords="offset points",
                 color=GOLD, fontsize=9)
    ax3.set_xticks([i for i in tick_idx])
    ax3.set_xticklabels([labels[i] for i in tick_idx], fontsize=8)
    ax3.set_ylabel("°C", color=MUTED)
    ax3.set_title("Each day's maximum and minimum", color=OFF_WHITE, fontsize=12, fontweight="bold")
    ax3.legend(loc="upper right", fontsize=8, facecolor=PANEL, edgecolor=MUTED, labelcolor=OFF_WHITE, ncol=3)

    # (4) Monthly distribution
    ax4 = fig.add_subplot(gs[1, 2])
    data = [monthly[m] for m in (2, 3, 4)]
    bp = ax4.boxplot(data, patch_artist=True, widths=0.5,
                     medianprops=dict(color=OFF_WHITE, lw=2),
                     whiskerprops=dict(color=MUTED), capprops=dict(color=MUTED),
                     flierprops=dict(markeredgecolor=MUTED, markersize=3))
    for patch in bp["boxes"]:
        patch.set_facecolor(GOLD)
        patch.set_alpha(0.4)
    ax4.set_xticks([1, 2, 3])
    ax4.set_xticklabels([MONTHS[m] for m in (2, 3, 4)], color=OFF_WHITE)
    ax4.set_ylabel("°C", color=MUTED)
    ax4.set_title("Monthly spread of hourly temperature", color=OFF_WHITE, fontsize=12, fontweight="bold")

    for ax in (ax1, ax2, ax3, ax4):
        ax.set_facecolor(PANEL)
        ax.tick_params(colors=MUTED, labelsize=9)
        for s in ax.spines.values():
            s.set_edgecolor("#444444")
        if ax is not ax1:
            ax.grid(alpha=0.2, color="#555555")
    fig.text(0.5, 0.012,
             "Source: NASA POWER hourly T2M (MERRA-2 reanalysis). Reanalysis is model-based, not a station measurement.",
             ha="center", color=MUTED, fontsize=9)
    os.makedirs("outputs", exist_ok=True)
    fig.savefig(OUT_PNG, dpi=180, facecolor=DARK_BG)

    # ---- csv --------------------------------------------------------------------
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["section", "label", "value", "unit"])
        for h in range(24):
            w.writerow(["average_day", f"{h:02d}:00", round(profile[h], 2), "C"])
        for j in range(n_days):
            w.writerow(["daily", labels[j], f"{d_min[j]:.2f} to {d_max[j]:.2f}", "C"])
        for m in (2, 3, 4):
            w.writerow(["monthly_mean", MONTHS[m], round(monthly[m].mean(), 2), "C"])

    # ---- story ----------------------------------------------------------------
    m_means = {m: monthly[m].mean() for m in (2, 3, 4)}
    hottest_m = max(m_means, key=m_means.get)
    coolest_m = min(m_means, key=m_means.get)
    story = f"""# Abuja's hot-dry season, read from the data

*Every figure below is calculated by `climate_summary.py` from the NASA POWER file.*

## The hours

Across {n_days} days, from 1 February to 30 April 2026, the air in Abuja was recorded in hourly steps
{len(temp):,} times. The day has a clear rhythm. Air is coolest at {trough_h:02d}:00, when the average
temperature is {profile[trough_h]:.1f} °C. It climbs through the morning and peaks at {peak_h:02d}:00, when the
average reaches {profile[peak_h]:.1f} °C. That is {profile[peak_h] - profile[trough_h]:.1f} °C between the
coolest and hottest hour of an average day, and {hours_to_peak} hours from the coolest hour to the peak.

## The nights

Night does not bring much relief. At {trough_h:02d}:00 the average is {profile[trough_h]:.1f} °C, and
on the coolest night of the season the air fell to {d_min[coolest]:.1f} °C ({labels[coolest]}).
Those nights are when a building can release the heat it has stored during the day, which is the
window that night ventilation uses.

## The days

The hottest day was {labels[hottest]}, when the air reached {d_max[hottest]:.1f} °C. The widest
daily swing was on {labels[widest]}, at {d_swing[widest]:.1f} °C, and the narrowest on
{labels[narrowest]}, at {d_swing[narrowest]:.1f} °C. The average daily swing across the season is
{d_swing.mean():.1f} °C. A building designed for the average day will meet days that are very
different from it.

## The months

- February averaged {m_means[2]:.1f} °C.
- March averaged {m_means[3]:.1f} °C.
- April averaged {m_means[4]:.1f} °C.

{MONTHS[hottest_m]} was the warmest month and {MONTHS[coolest_m]} the coolest. The season does not
simply get hotter; the pattern shifts through the spring.

## What this means for building

The climate sets the problem. The outdoor air swings by about {profile[peak_h] - profile[trough_h]:.0f} °C
in an average day, and nights stay warm. Any wall in Abuja has to deal with heat arriving in the
afternoon and a cooling period at night. This summary describes the outdoor conditions only. How a
particular wall responds, and whether the room stays comfortable, depends on ventilation, windows,
roof and occupancy, which are not part of this climate data.

## Source and limits

NASA POWER hourly 2 m air temperature (T2M), derived from MERRA-2 reanalysis. Reanalysis is
model-based, not a station measurement. Local standard time is used throughout.
"""
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(story)

    print(f"Hours {len(temp)}, days {n_days}")
    print(f"Average day: min {profile[trough_h]:.2f} at {trough_h:02d}:00, max {profile[peak_h]:.2f} at {peak_h:02d}:00")
    print(f"Hottest day {labels[hottest]} {d_max[hottest]:.2f}; coolest night {labels[coolest]} {d_min[coolest]:.2f}")
    print(f"Widest swing {labels[widest]} {d_swing[widest]:.2f}; mean daily swing {d_swing.mean():.2f}")
    print(f"Saved -> {OUT_PNG}, {OUT_CSV}, {OUT_MD}")


if __name__ == "__main__":
    main()
