import json

def DM(json_str, filename):
	measurement_dict = json.loads(json_str)
	for item in ["patientid", "temperature", "bloodpressure", "pulse", "oximeter", "weight", "height", "glucometer"]:
		if item not in measurement_dict:
			raise AttributeError(f"missing {item} data")
	cnt = 0
	if not measurement_dict["patientid"]:
		raise ValueError("personal id can't be empty")
	for k, v in measurement_dict.items():
		if k != "patientid":
			if v:
				cnt = 1
			try:
				v = float(v)
			except:
				raise ValueError("measurement data should be numbers")
			if v < 0:
				raise ValueError("measurement data should be positive")
	if cnt == 0:
		raise ValueError("measurement data can't be empty")

	with open(filename, 'w') as f:
		json.dump(measurement_dict, f)

# json_str = '''{
# 				"patientid": "001",
# 				"temperature": "36",
# 				"bloodpressure": "110",
# 				"pulse": "100",
# 				"oximeter": "90",
# 				"weight": "65",
# 				"height": "175",
# 				"glucometer": "-100"
# 			}'''
# try:
# 	DM(json_str, "example.json")
# except ValueError as e:
# 	print(e.args[0])