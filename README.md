# Medical_Platform
Platform to monitor patients at home or in the hospitals

## Branches
### Phase 0&1
All commits of phase 0 & 1 are in branch `Phase1` (now it's merged to `main` branch but not deleted).  
`Phase1` mainly achieves a device module, which uses json string of device measurement data as input and stores all data into a json file. In addition, this device module can handle error conditions, checking if measurement fields are missing and if measurement results are numbers and positive.

### Phase 2
All commits of phase 2 are in branch `Phase2` (now it's merged to `main` branch but not deleted).  
`Phase2` mainly achieves a restful system. Based on module in `Phase1`, it builds a website that allows users to enter device measurement results. Then the restful system will transfer the results into json string and pass into device module, checking fields and data errors and storing them in json file. The restful system is also deployed to AWS.

### Phase 3
All commits of phase 3 are in branch `Phase3` (now it's merged to `main` branch but not deleted).  
`Phase3` achieves chat module and corresponding restful api. In chat module it can send text/video/voice messages to other user. The text messages are directly stored in MySQL database while the addresses of video/voice files are stored in the database. A chat table is built for users (You can find its schema in [Database Schema](#database-schema)). As different users are needed in chat module, I also developed login/register functionality in restful api for the convenience of chat module testing. The user information and password are stored in user table.    

Below are several screenshots of my restful website till `Phase3`

#### Index

<img src='Pictures/index.PNG'> 

#### Signup and Login Page
<img src='Pictures/signup.PNG' width=49%> <img src='Pictures/login.PNG' width=49%>

#### Main Page
Upload large video/voice file may take some time, please be patient.

<img src='Pictures/mainpage.PNG' width=49%> <img src='Pictures/mainpage2.PNG' width=49%>

#### Display Message Page
Messages received will be displayed at the left side of the screen while messages sent will be displayed at the right side.

<img src='Pictures/display.PNG'>

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

### Chat table
| Field  | Type   |Null | Key | Default | Extra |
|------  |---------|-----| -----| -----|-----|
| connecting_user  | varchar(40)   | NO|  | NULL | |
| message_type | varchar(10)   |YES  | | NULL| |
| content | text   | YES | | NULL| |
| status | varchar(10)   | YES | | NULL| |
|time | date| YES | | NULL | |
