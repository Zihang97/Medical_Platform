import pytest
from Modules.device_module import *

class TestDeviceModule:
	def test_device_module_no_input(self):
		with pytest.raises(json.decoder.JSONDecodeError):
			dm_json_check("")


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
			dm_json_check(json_str)


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
			dm_json_check(json_str)


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
			dm_json_check(json_str)

