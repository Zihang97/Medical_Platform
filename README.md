# Medical_Platform
Platform to monitor patients at home or in the hospitals

## Branches
All commits of phase 0 & 1 are in branch `Phase1` (now it's merged to `main` branch but not deleted).  
`Phase1` mainly achieves a device module, which uses json string of device measurement data as input and stores all data into a json file. In addition, this device module can handle error conditions, checking if measurement fields are missing and if measurement results are numbers and positive.

All commits of phase 2 are in branch `Phase2` (now it's merged to `main` branch but not deleted).  
`Phase2` mainly achieves a restful system. Based on module in `Phase1`, it builds a website that allows users to enter device measurement results. Then the restful system will transfer the results into json string and pass into device module, checking fields and data errors and storing them in json file. The restful system is also deployed to AWS.

# Chat Module
## User Story
As a medical professional (Nurse or Doctor), I want to write a text or upload video/voice message to a patient.  
As a patient, I want to write a text or upload video/voice message to medical professional.  
As a patient or MP, I want to search for keywords in messages and chats.  
As a patient or MP, I want to check the history of chats and corresponding sending time (displaying chats).

## Design
I decide to use SQL database for chat module. Though columns in SQL are fixed compared to fields in document database, I'll use `TEXT` type to store messages. `TEXT` type can store anything entered as a string with no limit on length of string. Another reason for using SQL is that all other modules use SQL and user infomation are also stored in SQL database. It'll be quite complex to communicate between SQL and document if only chat module use document database.

# Device Module
## Input template for device module
The input to device module has to be in json format and follow below template.
```
{
  "patientid": "001",
  "temperature": "36",
  "bloodpressure": "70/110",
  "pulse": "100",
  "oximeter": "90",
  "weight": "65",
  "height": "175",
  "glucometer": "100"
}
```
All fields are required. If any field missing, there will be an error raised.
The units for measurement fields are listed following.
| Field  | Unit   |
|------  |---------|
|temperature| ℃|
|bloodpressure|mmHg|
|pulse| bpm|
|oximeter| %|
|weight| kg|
|height| cm|
|glucometer| mg/dL|

# Database Schema
### User table
| Field  | Type   |Null | Key | Default | Extra |
|------  |---------|-----| -----| -----|-----|
| id  | int   | NO | PRI | NULL | auto_increment|
|name| varchar(40)   | YES | | NULL| |
|email|  varchar(40)  | YES | |NULL | |
|address |   varchar(80)     | YES| | NULL| |
|age |  int    |  YES| | NULL| |
|gender |   varchar(10)  |  YES| |NULL | |
|dob |  varchar(40)    | YES | |NULL | |

### Role table
| Field  | Type   |Null | Key | Default | Extra |
|------  |---------|-----| -----| -----|-----|
| id  | int   | NO | PRI | NULL | auto_increment|
| role | varchar(40)| YES | | NULL| |

### Role Assgiment table
| Field  | Type   |Null | Key | Default | Extra |
|------  |---------|-----| -----| -----|-----|
| user_id  | int   | NO |  | NULL |foreign_key|
| role_id | int | NO | | NULL|foreign_key |

### Device table
| Field  | Type   |Null | Key | Default | Extra |
|------  |---------|-----| -----| -----|-----|
| id  | int   | NO | PRI | NULL | auto_increment|
| device | varchar(40)   | YES | | NULL| |
|dateofpurchase|  date | YES | |NULL | |
|MACaddress |   varchar(40)  |  YES| |NULL | |
|user_id | int    | YES | |NULL | foreign_key|

### Device Measurement table
| Field  | Type   |Null | Key | Default | Extra |
|------  |---------|-----| -----| -----|-----|
| user_id  | int   | NO |  | NULL | foreign_key|
| measurement_type | varchar(40)   | YES | | NULL| |
| result | varchar(40)   | YES | | NULL| |
|time | date| YES | | NULL | |

