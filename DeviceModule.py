import json

def DM(json_str, filename):
	measurement_dict = json.loads(json_str)
	for item in ["patient", "temperature", "bloodpressure", "pulse", "oximeter", "weight", "height", "glucometer"]:
		if item not in measurement_dict:
			raise AttributeError(f"missing {item} data")
	with open(filename, 'w') as f:
		json.dump(measurement_dict, f)

json_str = '''{
				"patient": "Jack Lucas",
				"temperature": "36",
				"bloodpressure": "110",
				"pulse": "100",
				"oximeter": "90",
				"weight": "65",
				"height": "175",
				"glucometer": "100"
			}'''
DM(json_str, "")