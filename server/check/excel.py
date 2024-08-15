import json
from openpyxl import Workbook

json_path = ""

columns = [
    "Tax",
    "Opening Stock",
    "Purchase",
    "Gross Profit",
    "Sale",
    "closing Stock",
]


def process_json(json_path):
    with open(f"config.json") as f:
        config = json.load(f)
    fy = config["fy"]
    name = config["name"]
    wb = Workbook()
    ws = wb.create_sheet("2022")
    ws.append([name])
    ws.append(columns)
    with open("2022.json") as f:
            data = json.load(f)
    for i in data["Discription"]:
            list = [
                data["Discription"][i]["Tax"],
                data["Discription"][i]["OS"],
                data["Discription"][i]["Pur"],
                data["Discription"][i]["GP"],
                data["Discription"][i]["Sale"],
                data["Discription"][i]["CS"],
            ]
            ws.append(list)
    wb.save(f"{name}.xlsx")

process_json(json_path)
        