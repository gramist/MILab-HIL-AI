# MILab-HIL-AI
Sejong University MILab -  Ministry of Health and Welfare/HIL Project - AI_Server

### Getting Started
Checkout this repo, install dependencies, then start the gulp process with the following:
```
> git clone https://github.com/gramist/MILab-HIL-AI.git
```

### First Developer's notion url
딥러닝을 이용한 치매 환자의 이상행동 감지 시스템
<https://www.notion.so/devilzcough/c018bbd49e3e46499756464f1853a70e?v=ca10e27e372147508b2ca6d5009feb13>

### Project Description
This project was designed to enable intercompatibility by adding servers, DBs, etc. in the project of all staff members.
It also modularized each of the complex sources to help users understand.

### DB Table Create Query
```sql
CREATE TABLE `patient` (
    idx INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    patient_num VARCHAR(32) NOT NULL,
    data VARCHAR(64) NOT NULL
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;
```

### How to Run?
Terminal_1
```
> cd MILab-HIL-AI
> python server.py
```

Terminal_2
```
> curl -i -H "Content-Type: application/json" -X POST -d "{\"PacketType\": \"SensorLog\", \"PatientSeq\": 37, \"SensorIdk\": \"A2:22:44:55:22:11\", \"SensorCode\": 1, \"SensorCount\": 11, \"LogTime\": \"2019-08-25 1:16:30\"}" 127.0.0.1:5000/foo
```
