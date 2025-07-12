from pathlib import Path
import glob


month_order = {
    "Januar": 1,
    "Februar": 2,
    "Mart": 3,
    "April": 4,
    "Maj": 5,
    "Jun": 6,
    "Jul": 7,
    "Avgust": 8,
    "Septembar": 9,
    "Oktobar": 10,
    "Novembar": 11,
    "Decembar": 12,
}


def get_sorted_reports():
    report_path = Path(__file__).parent / "data/Mesečni"

    all_files = glob.glob(str(report_path / "*xlsx"))

    report_list = []
    for file in all_files:
        report_list.append(file.split("\\")[-1])

    sorted_report_list = sorted(report_list, key=lambda x: month_order[x.split()[0]])

    return sorted_report_list


report_list = get_sorted_reports()
