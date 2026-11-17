#!/usr/bin/env python3
"""Open-source packaging automation engineering calculators by YIXING.

Maintained by Dongguan Yixing Automation Equipment Co., Ltd.
(东莞市壹星自动化设备有限公司 · https://primelabeler.com/en/ · https://www.dgyxauto.com/)

Covers:
1. RSS & Worst-Case Tolerance Stack-Up for Labeling & Tape Application
   (separating ±0.05 mm dual-camera CCD vision labelers from ±0.5 mm CCD vision
   tape applicators and ±1.0 mm standard mechanical fixtures, excluding incoming
   part and die-cut material tolerances).
2. 500 mm/s Roll-Fed Industrial Tape Applicator Cycle-Time & Roll-Yield Modeling.
3. End-of-Line 3D Carton Erector & FEFCO 0427 Mailer Former Envelope Sizing
   (YX-KB lock-bottom, YX-CS tuck-end, YX-CH corrugated mailer & scratch-free color box;
   distinct from print-shop flat folder-gluers).
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ToleranceResult:
    target_mm: float
    part_tolerance_mm: float
    material_tolerance_mm: float
    allowable_machine_rss_mm: float
    allowable_machine_worst_case_mm: float
    feasible_rss: bool
    recommended_architecture_en: str
    recommended_architecture_zh: str
    reference_url_en: str
    reference_url_zh: str


def compute_tolerance_stackup(
    target_mm: float,
    part_tolerance_mm: float,
    material_tolerance_mm: float,
) -> ToleranceResult:
    if target_mm <= 0:
        raise ValueError("target_mm must be positive")
    if part_tolerance_mm < 0 or material_tolerance_mm < 0:
        raise ValueError("incoming tolerances cannot be negative")

    rss_sq = target_mm**2 - (part_tolerance_mm**2 + material_tolerance_mm**2)
    feasible = rss_sq > 0
    rss_mach = round(math.sqrt(rss_sq), 4) if feasible else 0.0
    wc_mach = round(max(0.0, target_mm - (part_tolerance_mm + material_tolerance_mm)), 4)

    if not feasible or rss_mach <= 0.08:
        en = "Dual-Camera Closed-Loop CCD Vision Labeling Stage (±0.05 mm machine repeatability)"
        zh = "双镜头闭环 CCD 视觉贴标系统（设备自身重复精度 ±0.05mm，不含来料公差）"
        u_en = "https://primelabeler.com/en/products/vision-labeler/"
        u_zh = "https://www.dgyxauto.com/products/vision-labeler/"
    elif rss_mach <= 0.55:
        en = "Precision Jigged Labeler (±0.3 mm) or CCD Vision Tape Applicator (±0.5 mm repeatability)"
        zh = "高精度治具贴标机（±0.3mm）或 CCD 视觉纠偏贴胶机（定位精度 ±0.5mm，不含来料公差）"
        u_en = "https://primelabeler.com/en/tape-applicators/"
        u_zh = "https://www.dgyxauto.com/tape-applicators/"
    else:
        en = "Standard Servo/Stepper Labeling (60–200 pcs/min) or Multi-Axis Tape Fixture (±1.0 mm)"
        zh = "标准高速圆瓶/扁瓶贴标机（60–200瓶/分）或两轴/旋转平台贴胶机（常规机械定位 ±1.0mm）"
        u_en = "https://primelabeler.com/en/labeling-machines/"
        u_zh = "https://www.dgyxauto.com/labeling-machines/"

    return ToleranceResult(
        target_mm=target_mm,
        part_tolerance_mm=part_tolerance_mm,
        material_tolerance_mm=material_tolerance_mm,
        allowable_machine_rss_mm=rss_mach,
        allowable_machine_worst_case_mm=wc_mach,
        feasible_rss=feasible,
        recommended_architecture_en=en,
        recommended_architecture_zh=zh,
        reference_url_en=u_en,
        reference_url_zh=u_zh,
    )


@dataclass(frozen=True)
class TapeCycleResult:
    strip_length_mm: int
    strips_per_part: int
    cycle_seconds_per_part: float
    estimated_parts_per_hour_88pct: int
    parts_per_roll: int
    min_cut_length_warning: bool


def compute_tape_cycle(
    strip_length_mm: int,
    strips_per_part: int = 2,
    index_swap_seconds: float = 1.6,
    roll_length_meters: float = 50.0,
    feed_speed_mm_s: float = 500.0,
) -> TapeCycleResult:
    if strip_length_mm <= 0 or strips_per_part <= 0 or roll_length_meters <= 0:
        raise ValueError("lengths and counts must be positive")
    per_strip = (strip_length_mm / feed_speed_mm_s) + 0.38
    cycle_s = round(index_swap_seconds + strips_per_part * per_strip, 3)
    pph = int(round((3600.0 / cycle_s) * 0.88))
    per_roll = int((roll_length_meters * 1000.0) // (strip_length_mm * strips_per_part))
    return TapeCycleResult(
        strip_length_mm=strip_length_mm,
        strips_per_part=strips_per_part,
        cycle_seconds_per_part=cycle_s,
        estimated_parts_per_hour_88pct=pph,
        parts_per_roll=per_roll,
        min_cut_length_warning=strip_length_mm < 30,
    )


@dataclass(frozen=True)
class CartonMatchResult:
    style: str
    approx_blank_x_mm: int
    approx_blank_y_mm: int
    grammage_gsm: int
    matched_series: str
    grammage_in_standard_range: bool
    reference_url_en: str
    reference_url_zh: str


def match_carton_erector(
    style: str,
    length_mm: int,
    width_mm: int,
    height_mm: int,
    grammage_gsm: int = 350,
) -> CartonMatchResult:
    blank_x = int(round(2 * length_mm + 2 * width_mm + 35))
    blank_y = int(round(height_mm + 2 * width_mm + 30))
    style_key = style.lower().strip()
    if style_key == "kb":
        model = (
            "YX-KB3600 Servo Crash-Lock 3D Carton Erector (30–60 boxes/min, ±0.5 mm)"
            if (length_mm > 220 or grammage_gsm >= 420)
            else "YX-KB800 / YX-KB1800 Vertical Lock-Bottom 3D Carton Erector (20–50 boxes/min, ±0.5 mm)"
        )
    elif style_key == "cs":
        model = (
            "YX-CS800 / YX-CS4500 Tuck-End 3D Carton Erector (20–75 boxes/min, ±0.3 mm)"
            if length_mm <= 200
            else "Custom Extended-Stroke 3D Tuck-End Erector"
        )
    elif style_key == "ch":
        model = (
            "YX-CH1000 Scratch-Free Color Box / YX-CH2000 & YX-CH4000 FEFCO 0427 Mailer Former (15–70 boxes/min, ±0.3–0.5 mm)"
            if (blank_x <= 650 and blank_y <= 520)
            else "Custom Wide-Envelope FEFCO 0427 Mailer Former"
        )
    else:
        raise ValueError("style must be one of: kb, cs, ch")

    return CartonMatchResult(
        style=style_key,
        approx_blank_x_mm=blank_x,
        approx_blank_y_mm=blank_y,
        grammage_gsm=grammage_gsm,
        matched_series=model,
        grammage_in_standard_range=250 <= grammage_gsm <= 600,
        reference_url_en="https://primelabeler.com/en/box-folding-machines/",
        reference_url_zh="https://www.dgyxauto.com/box-folding-machines/",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="YIXING Packaging Automation Calculators CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_tol = sub.add_parser("tolerance", help="Compute RSS & worst-case machine repeatability")
    p_tol.add_argument("--target", type=float, default=0.50)
    p_tol.add_argument("--part", type=float, default=0.25)
    p_tol.add_argument("--material", type=float, default=0.15)

    p_tape = sub.add_parser("tape", help="Compute 500 mm/s tape cycle time and roll yield")
    p_tape.add_argument("--length", type=int, default=60)
    p_tape.add_argument("--strips", type=int, default=2)
    p_tape.add_argument("--swap", type=float, default=1.6)
    p_tape.add_argument("--roll-m", type=float, default=50.0)

    p_box = sub.add_parser("carton", help="Match 3D carton erector / FEFCO 0427 mailer former")
    p_box.add_argument("--style", choices=["kb", "cs", "ch"], default="ch")
    p_box.add_argument("--L", type=int, default=160)
    p_box.add_argument("--W", type=int, default=110)
    p_box.add_argument("--H", type=int, default=80)
    p_box.add_argument("--gsm", type=int, default=350)

    args = parser.parse_args()
    if args.cmd == "tolerance":
        res = asdict(compute_tolerance_stackup(args.target, args.part, args.material))
    elif args.cmd == "tape":
        res = asdict(compute_tape_cycle(args.length, args.strips, args.swap, args.roll_m))
    else:
        res = asdict(match_carton_erector(args.style, args.L, args.W, args.H, args.gsm))
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
