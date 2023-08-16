"""
Load CSV data containing lymphatic involvement of head and neck cancer patients
and keep only those with oral cavity tumors (i.e., specific ICD codes).
"""
import argparse
from pathlib import Path

import pandas as pd


ORAL_CAVITY_ICD_CODES = {
    "tongue": [
        "C02",
        "C02.0",
        "C02.1",
        "C02.2",
        "C02.3",
        "C02.4",
        "C02.8",
        "C02.9",
    ],
    "gums and cheeks": [
        "C03",
        "C03.0",
        "C03.1",
        "C03.9",
        "C06",
        "C06.0",
        "C06.1",
        "C06.2",
        "C06.8",
        "C06.9",
    ],
    "floor of mouth": [
        "C04",
        "C04.0",
        "C04.1",
        "C04.8",
        "C04.9",
    ],
    # "palate": ["C05", "C05.0", "C05.1", "C05.2", "C05.8", "C05.9",],
    # "salivary glands": ["C08", "C08.0", "C08.1", "C08.9",],
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="Input CSV file")
    parser.add_argument("--output", type=Path, help="Output CSV file")
    args = parser.parse_args()

    patient_data = pd.read_csv(args.input, header=[0, 1, 2])
    is_oral_cavity = patient_data["tumor", "1", "subsite"].isin(
        icd for icd_list in ORAL_CAVITY_ICD_CODES.values() for icd in icd_list
    )
    is_isb = patient_data["patient", "#", "institution"] == "Inselspital Bern"
    oral_cavity_data = patient_data[is_oral_cavity & is_isb]

    oral_cavity_data.to_csv(args.output, index=False)
