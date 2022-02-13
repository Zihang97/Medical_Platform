# Medical_Platform
Platform to monitor patients at home or in the hospitals

## Database Schema
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

