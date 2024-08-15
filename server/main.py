from flask import Flask, render_template, jsonify, request, send_file
import sqlite3 as sq
import json
import os
from flask_cors import CORS
import pandas as pd
from openpyxl.styles import Alignment
import waitress
# import openpyxl as xl

app = Flask(__name__)
CORS(app)
cors = CORS(app, resource={r"/*": {"origins": "*"}})

# db_path="database/DATABASE.db"

NAME={"name":""}

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def process_json(files, name, code):
    file_dict = {}
    for file in files:
        with open(f"companies/{code}/{file}.json") as f:
            data = json.load(f)
        data_list = [
                [      
                data["Discription"][i]["Tax"],
                data["Discription"][i]["OS"],
                data["Discription"][i]["Pur"],
                data["Discription"][i]["GP"],
                data["Discription"][i]["Sale"],
                data["Discription"][i]["CS"],
                ]
            for i in data["Discription"]
        ]
        data_list.append([data["total"]["Tax"], data["total"]["OS"], data["total"]["Pur"], data["total"]["GP"], data["total"]["Sale"], data["total"]["CS"]])
        columns = [
            "Tax",
            "Opening Stock",
            "Purchase",
            "Gross Profit",
            "Sale",
            "closing Stock",
        ]
        # old
        df = pd.DataFrame(data_list, columns=columns)
        file_dict[file] = df
        
    
    # new :
    output_file = f"static/download/code({code}).xlsx"
    with pd.ExcelWriter(output_file) as writer:
    # Write each DataFrame to a separate sheet
      for sheet_name, df in file_dict.items():
        df.to_excel(writer, sheet_name=f"{sheet_name}", index=False)
        workbook = writer.book
        worksheet = workbook[f"{sheet_name}"]
        # Set column widths
        worksheet.column_dimensions["B"].width = 20
        worksheet.column_dimensions["C"].width = 20
        worksheet.column_dimensions["D"].width = 20
        worksheet.column_dimensions["E"].width = 20
        worksheet.column_dimensions["F"].width = 20
        # Add a header
        worksheet.insert_rows(0)
        worksheet.merge_cells('A1:F1')
        worksheet['A1'] = f"{name} (Financial Year {sheet_name})"
        worksheet['A1'].font = 'Arial Black'
        # center text
        for row in worksheet.iter_rows():
          for cell in row:
            cell.alignment = Alignment(horizontal="center", vertical="center")


def connect_db(code: str, name: str) -> bool:
    try:
        con = sq.connect("static/database/DATABASE.db")
        cur = con.cursor()
        cur.execute(
            "INSERT INTO COMPANY_DATABASE (CODE, NAME) VALUES (?, ?);", (int(code), name)
        )
        con.commit()
        con.close()
        return True
    except Exception as e:
        print(e)
        return False


def get_db(query):
    db = sq.connect("static/database/DATABASE.db")
    db.row_factory = dict_factory
    cur = db.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    db.close()
    # print(jsonify(rows))
    return jsonify(rows)


@app.route("/home", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        return get_db("SELECT * FROM COMPANY_DATABASE;")
    else:
        try:
            data = request.get_json()
            return get_db(
                f"""SELECT * FROM COMPANY_DATABASE WHERE NAME LIKE '%{data['search']}%' ;"""
            )
        except Exception as e:
            return get_db("SELECT * FROM COMPANY_DATABASE;")


@app.route("/save", methods=["POST", "GET"])
def save():
    data = request.get_json()
    company = data["company"]
    cy = data["cy"]
    code = company["code"]
    discription = company["Discription"]
    total = company["total"]
    path = f"companies/{code}"
    with open(f"{path}/{cy}.json", "w") as json_file:
        json.dump({"Discription": discription, "total": total}, json_file, indent=4)
    # print(data)
    return jsonify(data)


@app.route("/code/<int:code>", methods=["POST", "GET"])
def code(code):
    path = f"companies/{code}"
    with open(f"{path}/config.json", "r") as file:
       config = json.load(file)
    if request.method == "GET":
        with open(f"{path}/{config['fy'][0]}.json") as file:
            discription = json.load(file)
        # print(data)
        config.update(discription)
        print(config)
        return jsonify(config)
    if request.method == "POST":
        data = request.get_json()
        fy = data["fy"]
        with open(f"{path}/{fy}.json") as file:
            discription = json.load(file)
        config.update(discription)
        print(config)
        return jsonify(config)


@app.route("/new_fy", methods=["GET", "POST"])
def new_fy():
    data = request.get_json()
    path = f"companies/{data['code']}"
    with open(f"{path}/config.json") as file:
        config = json.load(file)
    config["fy"].append(data["fy"])
    with open(f"{path}/config.json", "w") as json_file:
        json.dump(config, json_file, indent=4)
    with open(f"{path}/{int(data['fy'])-1}.json") as file:
        discription = json.load(file)
    for i in discription["Discription"]:
        discription["Discription"][i].update(
            {
                "OS": discription["Discription"][i]["CS"],
                "Pur": 0,
                "GP": 0,
                "Sale": 0,
                "CS": 0,
            }
        )
    with open(f"{path}/{data['fy']}.json", "w") as f:
        json.dump(discription, f, indent=4)
    return jsonify("created")


@app.route("/create", methods=["POST"])
def create():
    try:
        # Get data from the form fields
        code = request.get_json()["code"]
        name = request.get_json()["name"]
        discription = request.get_json()["Discription"]
        total = request.get_json()["total"]
        fy = request.get_json()["fy"]
        path = f"companies/{code}"
        # print(code)
        if not os.path.exists(path):
            os.makedirs(path)
            with open(f"{path}/config.json", "w") as json_file:
                json.dump(
                    {
                        "code": code,
                        "name": name,
                        "fy": fy,
                    },
                    json_file,
                    indent=4,
                )
            with open(f"{path}/{fy[0]}.json", "w") as json_file:
                json.dump({"Discription": discription, "total": total}, json_file, indent=4)
            connect_db(code, name)
            # get_db()
            print(f"Received data: Code={code}")
            return jsonify("Company created successfully!")
        else:
            return jsonify("Company already exists!")
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify("Error occurred while processing data.")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    code = data["code"]
    name = data["name"]
    fys = data["fys"]
    NAME["name"]=name
    # json_path = f"companies/{code}/{fy}.json"
    process_json(fys, name, code)
    return jsonify("file generated")

@app.route("/download/<int:code>", methods=["GET"])
def download(code):
    path = f"static/download/code({code}).xlsx"
    return send_file(path, as_attachment=True)

@app.route("/new_code", methods=["POST", "GET"])
def new_code():
    code = get_db("SELECT CODE FROM COMPANY_DATABASE ORDER BY CODE DESC LIMIT 1;")
    return code

@app.route("/modify", methods=["POST", "GET"])
def modify():
    if request.method == "POST":
        data = request.get_json()
        company = data["company"]
        cy = company["fy"]
        code = company["code"]
        discription = data["Data"]["Discription"]
        total = data["Data"]["total"]
        path = f"companies/{code}"
        with open(f"{path}/config.json") as json_file:
            config=json.load(json_file)
            config.update({"name": data["Data"]["name"]})
        with open(f"{path}/config.json", "w") as json_file:
            print(config)
            json.dump(config, json_file, indent=4)
            db = sq.connect("static/database/DATABASE.db")
            cur = db.cursor()
            cur.execute(f"UPDATE COMPANY_DATABASE SET name='{data['Data']['name']}' WHERE CODE = {code};")
            db.commit()
            db.close()
        with open(f"{path}/{cy}.json", "w") as json_file:
          json.dump({"Discription": discription, "total": total}, json_file, indent=4)
        print(path)
        return jsonify(data)
    else:
        code = request.args.get('code')
        fy = request.args.get('fy')
        path = f"companies/{code}"
        with open(f"{path}/config.json") as file:
            config = json.load(file)
        with open(f"{path}/{fy}.json") as file:
            discription = json.load(file)
        # print(data)
        config.update(discription)
        print(config)
        return jsonify(config)


if __name__ == "__main__":
    # waitress.serve(app, host="0.0.0.0", port=5000)
    app.run(host="0.0.0.0", port=5000, debug=True)
