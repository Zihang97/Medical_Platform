# Medical_Platform
Platform to monitor patients at home or in the hospitals

## Database Schema
### User table
| Field  | Type   |Null | Key | Default | Extra |
|------  |---------|-----| -----| -----|-----|
| id  | int   | NO | PRI | NULL | auto_increment|
|name| varchar(40)   | YES | | | |
|email|  varchar(40)  | YES | | | |
|address |   varchar(80)     | YES| | | |
|age |  int    |  YES| | | |
|gender |   varchar(10)  |  YES| | | |
|dob |  varchar(40)    | YES | | | |
