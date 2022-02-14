import pytest
from DeviceModule import *

class TestDeviceModule:
	def test_device_module_no_input(self):
		with pytest.raises(AttributeError):
			DM("", "example.json")


	def test_device_module_incomplete_input(self):
		with pytest.raises(AttributeError):
			json_str = '''{
				"patient": "Jack Lucas",
				"temperature": "36",
				"bloodpressure": "110",
				"pulse": "100",
				"oximeter": "90",
				"weight": "65",
				"height": "175",
			}'''
			DM(json_str, "example.json")


	def test_device_module_no_filename(self):
		with pytest.raises(TypeError):
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
			DM(json_str)


	def test_device_module_empty_filename(self):
		with pytest.raises(FileNotFoundError):
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
			DM(json_str)
