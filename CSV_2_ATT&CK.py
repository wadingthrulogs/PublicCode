import csv, re, json

showsubs = "true"
sub_match = re.compile(r"[T]\d\d\d\d\.\d\d\d")
tech_match = re.compile(r"[T]\d\d\d\d")
ids = []


filename = "testdata.csv"


layer = {
    "description": "test",
    "name": "test",
    "domain": "enterprise-attack",
    "version": {
        "layer": "4.4",
        "attack": "12", 
        "navigator": "4.5"
    },
    "techniques": []
}



def count_elements(lst):
    count_dict = {}

    for elem in lst:
        if elem in count_dict:
            count_dict[elem] += 1
        else:
            count_dict[elem] = 1
    

    return count_dict



with open(filename, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Name of the column to search through
        potentional_match = (row['b'])
        sub_results = sub_match.search(potentional_match)
        tech_results = tech_match.search(potentional_match)

    if sub_results:
        ids.append(sub_results.group())
    elif tech_results:
        ids.append(tech_results.group())

counted_ids = count_elements(ids)


for tech_ids, count in counted_ids.items():
    if sub_match.search(tech_ids):
        tech = tech_match.search(tech_ids)

        sub_tech_on = {
            "techniqueID": tech.group(),
            "showSubTechniques": showsubs,
            "color": "#66b1ff"
        }
        sub_tech = {
            "score": count,
            "color": "#66b1ff",
            "techniqueID": tech_ids,
            "showSubtechniques": showsubs,
            "comment": "yep"
        }
        layer["techniques"].append(sub_tech_on)
        layer["techniques"].append(sub_tech)
    else:
        full_tech = {
            "score": count,
            "color": "#66b1ff",
            "techniqueID": tech_ids,
            "showSubTechniques": showsubs,
            "comment": "yep"
        }
        layer["techniques"].append(full_tech)


with open("my_nav_layer.json", "w") as outfile:
    json.dump(layer,outfile)