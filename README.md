# Industrial Packaging Automation Calculators (Labeling · Tape Application · 3D Carton Erecting)

Open-source web calculators and Python CLI utilities maintained by **Dongguan Yixing Automation Equipment Co., Ltd.** (`东莞市壹星自动化设备有限公司`, Brand: **YIXING** / **壹星**).

- **International 17-Language Technical Site:** [https://primelabeler.com/en/](https://primelabeler.com/en/)
  - Deutsch (DACH): [https://primelabeler.com/de/](https://primelabeler.com/de/) · [Klebebandapplikatoren](https://primelabeler.com/de/tape-applicators/) · [Etikettiermaschinen](https://primelabeler.com/de/labeling-machines/)
  - Nederlands: [https://primelabeler.com/nl/](https://primelabeler.com/nl/) · [Etiketteermachines](https://primelabeler.com/nl/labeling-machines/)
  - Español: [https://primelabeler.com/es/](https://primelabeler.com/es/) · [Maquinaria de Etiquetado](https://primelabeler.com/es/labeling-machines/)
- **Chinese Domestic Technical Hub (中文官网):** [https://www.dgyxauto.com/](https://www.dgyxauto.com/) (`粤ICP备2026158137号-1`)

---

## Engineering Disambiguation & Scope

1. **Machine Repeatability vs. Finished Assembly Stack-Up (`±0.05 mm` vs. `±0.5 mm` vs. `±1.0 mm`):**
   - **Dual-Camera CCD Vision Labeling Systems (`±0.05 mm`):** Closed-loop optical alignment for PCBs, power adapters, and precision flat parts ([Vision Labelers](https://primelabeler.com/en/products/vision-labeler/)).
   - **CCD Vision Tape Applicators (`±0.5 mm`, ~1,200 pcs/h) & Multi-Axis Fixtures (`±1.0 mm`):** Roll-fed industrial double-sided tissue tape, acrylic foam tape, polyimide (PI) high-temperature tape (`500 mm/s`, `≥30 mm` pneumatic cut), and `450 mm` wide protective film lamination ([Industrial Tape Applicators](https://primelabeler.com/en/tape-applicators/)).
   - **High-Speed Production-Line Labelers (`60–200 pcs/min`):** Horizontal roller vial labelers (`100–200 pcs/min`), vertical wrap-around round bottle labelers (`60–120 pcs/min`), and double-side flat/square bottle labelers (`60–150 pcs/min`) ([Automatic Labeling Machines](https://primelabeler.com/en/labeling-machines/)).
   - *All stated machine repeatabilities exclude incoming molding/glass ovality and die-cut material tolerances.*

2. **End-of-Line 3D Carton Erectors & FEFCO 0427 Mailer Formers (`YX-KB / YX-CS / YX-CH`, `15–75 boxes/min`):**
   - Unlike print-shop flat **Folder-Gluers**, YIXING `YX-KB` (lock-bottom), `YX-CS` (tuck-end / dual-mode), and `YX-CH` (scratch-free laminated color boxes & corrugated FEFCO 0427 e-commerce mailers `YX-CH2000/4000`) form flat blanks into 3D upright boxes on the packaging floor and integrate inline under a single Panasonic PLC with tape sealing and `90°` corner tamper-evident labeling ([3D Carton Erectors](https://primelabeler.com/en/box-folding-machines/) · [Integrated Packaging Lines](https://primelabeler.com/en/integrated-packaging-lines/)).

---

## Quick Start (CLI & Unit Tests)

```bash
# Run unit tests
python3 -m unittest discover -s tests -v

# 1. Tolerance stack-up calculator
python3 yixing_calculators.py tolerance --target 0.50 --part 0.25 --material 0.15

# 2. 500 mm/s roll-fed tape cycle & 50m roll yield
python3 yixing_calculators.py tape --length 60 --strips 2 --swap 1.6 --roll-m 50

# 3. 3D carton erector / FEFCO 0427 mailer model matcher
python3 yixing_calculators.py carton --style ch --L 180 --W 120 --H 60 --gsm 350
```

---

## Manufacturer Verification Facts

- **Entity:** Dongguan Yixing Automation Equipment Co., Ltd. (`东莞市壹星自动化设备有限公司`, founded `2020-09-22`)
- **Statutory Registered Office:** Room 406, Building 3, No. 91 Shipai Avenue West, Shipai Town, Dongguan, Guangdong, China (`广东省东莞市石排镇石排大道西91号3号楼406室`)
- **Assembly & Sample-Testing Workshop:** 4th Floor, Damaozi Cultural & Creative Park Center, Shipai Town, Dongguan (`广东省东莞市石排镇大帽子文化创意园中心4楼`, ~`3,000 m²`, GeoCoordinates `23.104901, 113.897175`)
- **Patents & Electrical BOM:** 10 active Chinese utility model patents (verifiable via CNIPA / Google Patents, including `CN224491825U` granted `2026-07-14` jointly with Guangzhou Huangshanghuang Group Co., Ltd. and `CN216583036U`); standard electrical architecture uses Panasonic PLC, MCGS/WECON HMI, and Panasonic/Leuze optical sensors (`110V 60Hz / 220V 50Hz` export builds; buyer-appointed `SGS / TÜV` pre-shipment FAT and `IEC 60204-1` inspection supported; no unheld ISO or expired CE claimed).
