import pytest
from Modules.device_module import *

class TestDeviceModule:
	def test_device_module_no_input(self):
		with pytest.raises(json.decoder.JSONDecodeError):
			DM("", "example.json")


	def test_device_module_incomplete_input(self):
		with pytest.raises(AttributeError):
			json_str = '''{
				"patientid": "001",
				"temperature": "36",
				"bloodpressure": "110",
				"pulse": "100",
				"oximeter": "90",
				"weight": "65",
				"height": "175"
			}'''
			DM(json_str, "example.json")


	def test_device_module_no_filename(self):
		with pytest.raises(TypeError):
			json_str = '''{
				"patientid": "001",
				"temperature": "36",
				"bloodpressure": "110",
				"pulse": "100",
				"oximeter": "90",
				"weight": "65",
				"height": "175",
				"glucometer": "100"
			}'''
			DM(json_str)


	def test_device_module_empty_filename(self):
		with pytest.raises(FileNotFoundError):
			json_str = '''{
				"patientid": "001",
				"temperature": "36",
				"bloodpressure": "110",
				"pulse": "100",
				"oximeter": "90",
				"weight": "65",
				"height": "175",
				"glucometer": "100"
			}'''
			DM(json_str, "")


	def test_device_module_not_number(self):
		with pytest.raises(ValueError):
			json_str = '''{
				"patientid": "001",
				"temperature": "36",
				"bloodpressure": "110",
				"pulse": "100",
				"oximeter": "90",
				"weight": "65",
				"height": "175",
				"glucometer": "hello"
			}'''
			DM(json_str, "example.json")


	def test_device_module_negative_number(self):
		with pytest.raises(ValueError):
			json_str = '''{
				"patientid": "001",
				"temperature": "36",
				"bloodpressure": "110",
				"pulse": "-100",
				"oximeter": "90",
				"weight": "65",
				"height": "175",
				"glucometer": "100"
			}'''
			DM(json_str, "example.json")

