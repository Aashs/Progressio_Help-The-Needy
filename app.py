from http import client
from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/donors")
def donors():
    f = open("data/donors.json", "r")
    donors_str = f.read()
    all_donors = json.loads(donors_str)     

    return render_template("donors/list.html", donors=all_donors)


@app.route("/donors/add", methods=['GET', 'POST'])
def donor_create():

    f = open("data/donors.json", "r")
    donors_str = f.read()
    f.close()
    all_donors = json.loads(donors_str)    

    next_id = 1
    if len(all_donors) > 0:
        next_id = all_donors[-1]["id"] + 1

    if request.method == 'POST':
        name = request.form["name"]
        food_type = request.form["food_type"]
        quantity = request.form["quantity"]
        expiry_date = request.form["expiry_date"]
        location = request.form["location"]
        contact = request.form["contact"]

        if name == "":
            return "Name is required"

        all_donors.append(
            {
                "id": next_id,
                "name": name,
                "food_type": food_type,
                "quantity": quantity,
                "expiry_date": expiry_date,
                "location": location,
                "contact": contact,
            }
        )

        updated_donors = json.dumps(all_donors)
        f = open("data/donors.json", "w")
        f.write(updated_donors)
        f.close()

        return redirect("/donors")
    
    return render_template("donors/add.html", next_id=next_id)


@app.route("/donors/<id>")
def donor(id):

    f = open("data/donors.json", "r")
    donors_str = f.read()
    f.close()
    all_donors = json.loads(donors_str)

    donor_by_id = list(filter(lambda x: (x["id"] == int(id)), all_donors))
    donor_by_id = donor_by_id[0]

    return render_template("donors/view.html", donor=donor_by_id)


@app.route("/donors/edit/<id>", methods=['GET', 'POST'])
def donor_edit(id):

    f = open("data/donors.json", "r")
    donors_str = f.read()
    f.close()
    all_donors = json.loads(donors_str)

    donor_by_id = list(filter(lambda x: (x["id"] == int(id)), all_donors))
    donor_by_id = donor_by_id[0]
    donor_index = all_donors.index(donor_by_id)

    if request.method == 'POST':
        name = request.form["name"]
        food_type = request.form["food_type"]
        quantity = request.form["quantity"]
        expiry_date = request.form["expiry_date"]
        location = request.form["location"]
        contact = request.form["contact"]
        all_donors[donor_index] = {
            "id": donor_by_id["id"], 
            "name": name,
            "food_type": food_type,
            "quantity": quantity,
            "expiry_date": expiry_date,
            "location": location,
            "contact": contact 
        }

        updated_donors = json.dumps(all_donors)
        f = open("data/donors.json", "w")
        f.write(updated_donors)
        f.close()

        return redirect('/donors')

    return render_template("donors/update.html", donor_id=id, donor=donor_by_id)


@app.route("/donors/delete")
def donor_delete():

    f = open("data/donors.json", "r")
    donors_str = f.read()
    f.close()
    all_donors = json.loads(donors_str)

    donor_id = request.args.get("id")
    donor_by_id = list(filter(lambda x: (x["id"] == int(donor_id)), all_donors))
    donor_by_id = donor_by_id[0]
    donor_index = all_donors.index(donor_by_id)

    del all_donors[donor_index]
    updated_donors = json.dumps(all_donors)

    f = open("data/donors.json", "w")
    f.write(updated_donors)
    f.close()

    return redirect("/donors")

@app.route("/receptionists")
def receptionists():
    f = open("data/donors.json", "r")
    donors_str = f.read()
    all_donors = json.loads(donors_str)     
    
    location = ""

    return render_template("receptionists/list.html", donors=all_donors, location=location)

@app.route("/receptionists/<id>")
def receptionist_view(id):

    f = open("data/donors.json", "r")
    donors_str = f.read()
    f.close()
    all_donors = json.loads(donors_str)

    donor_by_id = list(filter(lambda x: (x["id"] == int(id)), all_donors))
    donor_by_id = donor_by_id[0]

    return render_template("receptionists/view.html", donor=donor_by_id)

@app.route("/receptionists/search", methods=['GET'])
def receptionist_search():

    f = open("data/donors.json", "r")
    donors_str = f.read()
    f.close()
    all_donors = json.loads(donors_str)

    location = request.args["location"]

    if location == "":
        return redirect('/receptionists')

    donors_by_location = list(filter(lambda x: (x["location"].lower() == location.lower()), all_donors))

    return render_template("receptionists/list.html", donors=donors_by_location, location=location)

@app.route("/receptionists/claim/<int:id>", methods=['POST'])
def claim_food(id):
    f = open("data/donors.json", "r")
    donors_str = f.read()
    f.close()
    all_donors = json.loads(donors_str)

    donor_by_id = next((x for x in all_donors if x["id"] == id), None)

    if donor_by_id:
        if "claimed" not in donor_by_id:
            donor_by_id["claimed"] = True

            updated_donors = json.dumps(all_donors)
            f = open("data/donors.json", "w")
            f.write(updated_donors)
            f.close()

            return jsonify({"success": True})
    
    return jsonify({"success": False})