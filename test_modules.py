import pytest
from Modules.device_module import *

class TestDeviceModule:
	def test_device_module_no_input(self):
		with pytest.raises(json.decoder.JSONDecodeError):
			dm_json_check("")


	def test_device_module_incomplete_input(self):
		with pytest.raises(AttributeError):
			json_str = '''{
				"patientname": "Jack",
				"temperature": "36.5",
				"systolicbloodpressure": "110",
				"diastolicbloodpressure": "70",
				"pulse": "95",
				"oximeter": "98"
			}'''
			dm_json_check(json_str)


	def test_device_module_not_number(self):
		with pytest.raises(ValueError):
			json_str = '''{
				"patientname": "Jack",
				"temperature": "36.5",
				"systolicbloodpressure": "110",
				"diastolicbloodpressure": "70",
				"pulse": "95",
				"oximeter": "98",
				"glucometer": "hello"
			}'''
			dm_json_check(json_str)


	def test_device_module_negative_number(self):
		with pytest.raises(ValueError):
			json_str = '''{
				"patientname": "Jack",
				"temperature": "36.5",
				"systolicbloodpressure": "110",
				"diastolicbloodpressure": "-70",
				"pulse": "95",
				"oximeter": "98",
				"glucometer": "82"
			}'''
			dm_json_check(json_str)

