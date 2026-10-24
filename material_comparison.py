"""
Material comparison for earthen and concrete-block walls, Abuja / West Africa.

Scope: documented material properties, embodied carbon (open EPDs), and the
availability evidence found. No room simulation. An earlier dynamic model failed
validation against a measured dwelling (daily swing 0.7 C modelled vs 4.6 C
measured), so its dynamic results are not reported here.

Every thermal input carries its source. Values from different sources are kept
as separate cases and are not averaged or merged.

Thermal cases (conduction resistance R = d / k; heat capacity C = rho * cp * d)
  A. CEB, Auroville Earth Institute CSEB table (2005)
       k 0.81-0.93 W/m.K, rho 1800 kg/m3 (class B/C), cp 650-850 J/kg.K
       Source writes specific heat as "KJ/Kg"; read as kJ/kg.K.
       Stabilisation level and cement content not stated.
  B. CEB, Ouedraogo et al. (2024), Table 1, pilot building, 14 cm, 8% cement
       k 1.02, rho 1840 kg/m3, cp 975 J/kg.K (initial values, model inputs)
  C. Cement block, Ouedraogo et al. (2024), Table 1, pilot building, 15 cm
       k 0.80, rho 1000 kg/m3, cp 1000 J/kg.K (initial values, model inputs)
       The paper's wall is coated with 2.5 cm mortar each side; not included here.
  D. Concrete block, Nigerian density range, 225 mm
       rho 1614-2002 kg/m3 (Nigerian sandcrete measurements, 3 studies)
       cp 1000 J/kg.K (from case C, model input)
       Conductivity NOT established: no verified source for a Nigerian block value.
       Resistance therefore not calculated for this case.

Embodied carbon (kg CO2 per m2 of wall face)
  CEB 300 mm, total, Auroville 2005: 51.5 kg CO2/m3 x 0.300 m; boundary unknown.
  Concrete block 225 mm, cement only, Nigerian bag-yield (20-25 blocks per 50 kg
    bag) x 0.763 kg CO2e/kg cement (ECO Platform EPDIE-21-52, A1-A3); lower bound.
  Dense concrete block 140 mm, total A1-A3, IBU EPD, Holcim UK Masterdenz 140 7.3N;
    reference only, different product and thickness.
"""
import csv, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join("outputs", "material_comparison.csv")
OUT_PNG = os.path.join("outputs", "embodied_carbon.png")

# Each case: label, source, k (None if not established), rho, cp, thickness (m)
THERMAL_CASES = [
    ("CEB A (k 0.81)", "Auroville CSEB table", 0.81, 1800.0, 650.0, 0.300),
    ("CEB A (k 0.81)", "Auroville CSEB table", 0.81, 1800.0, 850.0, 0.300),
    ("CEB A (k 0.93)", "Auroville CSEB table", 0.93, 1800.0, 650.0, 0.300),
    ("CEB A (k 0.93)", "Auroville CSEB table", 0.93, 1800.0, 850.0, 0.300),
    ("CEB B", "Ouedraogo et al. 2024, Table 1", 1.02, 1840.0, 975.0, 0.140),
    ("Cement block C", "Ouedraogo et al. 2024, Table 1", 0.80, 1000.0, 1000.0, 0.150),
    ("Concrete block D, 1614 kg/m3", "Nigerian sandcrete measurements", None, 1614.0, 1000.0, 0.225),
    ("Concrete block D, 2002 kg/m3", "Nigerian sandcrete measurements", None, 2002.0, 1000.0, 0.225),
]


def thermal_rows():
    rows = []
    for label, source, k, rho, cp, d in THERMAL_CASES:
        r = round(d / k, 3) if k else "not established"
        c = round(rho * cp * d / 1000.0, 1)          # kJ/m2.K
        rows.append([label, source, k if k else "not established", rho, cp, round(d * 1000), r, c])
    return rows


def embodied_rows():
    rows = []
    ceb_co2 = 51.5 * 0.300
    rows.append(["CEB 300 mm", "total, Auroville 2005 (boundary unknown)", round(ceb_co2, 1)])
    face = 0.450 * 0.225
    for per_bag in (25, 20):
        cement_kg = 50.0 / per_bag
        co2 = cement_kg * 0.763 / face
        rows.append(["Concrete block 225 mm",
                     f"cement only, {per_bag} blocks/bag ({cement_kg:.1f} kg/block), lower bound",
                     round(co2, 1)])
    rows.append(["Dense concrete block 140 mm (reference)", "total A1-A3, IBU EPD", 14.8])
    return rows


def main():
    os.makedirs("outputs", exist_ok=True)
    thermal = thermal_rows()
    emb = embodied_rows()

    print("Thermal cases (R = d/k, m2K/W; C = rho*cp*d, kJ/m2K)")
    print(f"{'case':<30}{'k':>6}{'rho':>7}{'cp':>7}{'d mm':>6}{'R':>16}{'C':>9}")
    for t in thermal:
        print(f"{t[0]:<30}{str(t[2]):>6}{t[3]:>7.0f}{t[4]:>7.0f}{t[5]:>6}{str(t[6]):>16}{t[7]:>9}")

    print("\nEmbodied carbon per m2 of wall face (kg CO2)")
    for e in emb:
        print(f"  {e[0]:<38} {e[1]:<62} {e[2]:>6}")

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["section", "case", "source", "k_W_per_mK", "density_kg_m3", "cp_J_per_kgK",
                    "thickness_mm", "R_m2K_per_W", "C_kJ_per_m2K", "embodied_kg_CO2_per_m2"])
        for t in thermal:
            w.writerow(["thermal", t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], ""])
        for e in emb:
            w.writerow(["embodied", e[0], e[1], "", "", "", "", "", "", e[2]])

    labels = ["CEB 300 mm\n(total, Auroville)", "Concrete block 225 mm\n(cement only, 25/bag)",
              "Concrete block 225 mm\n(cement only, 20/bag)", "Dense block 140 mm\n(total, IBU EPD ref.)"]
    values = [emb[0][2], emb[1][2], emb[2][2], emb[3][2]]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(labels, values, color=["#C9A84C", "#5C8DA3", "#5C8DA3", "#9AA5AD"], edgecolor="#222222")
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.3, f"{v:.1f}", ha="center", fontsize=9)
    ax.set_ylabel("kg CO2 per m2 of wall face")
    ax.set_title("Embodied carbon per square metre of wall face (documented sources)")
    ax.grid(axis="y", alpha=0.3)
    fig.text(0.5, 0.01, "CEB boundary unknown; block values are cement-only lower bounds, except the 140 mm reference (total A1-A3).",
             ha="center", fontsize=7, color="#555555")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(OUT_PNG, dpi=180)
    print(f"\nSaved -> {OUT}")
    print(f"Saved -> {OUT_PNG}")


if __name__ == "__main__":
    main()
