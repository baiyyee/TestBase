# TestBase

**TestBase** is a scaffold project to start a automation test project.

- System Environment (Opitonal)
  
| PARAMETER      | DESCRIPTION    |
| -------------- | -------------- |
| NACOS_HOST     | nacos host     |
| NACOS_USERNAME | nacos username |
| NACOS_PASSWORD | nacos password |
| NACOS_TENANT   | nacos tenant   |
| PYTEST_CMD     | pytest cmd     |


- Directory Structure

```console
|── TestBase
    ├── config            ................... Global Config Sets
        ├── api.py        ................... API Sets
        ├── const.py      ................... Global Constant
    ├── data              ................... Test Data Sets
        ├── api           ................... API Test Data
        ├── app           ................... APP Test Data
        ├── feature       ................... Feature Test Data
        ├── monitor       ................... Online Monitor Data
        ├── page          ................... UI Test Page Model
        ├── ramp          ................... Rampup Test Data
        ├── security      ................... Security Test Data
        ├── stress        ................... Stress/Performance Test Data
    ├── doc               ................... Test Docs
    ├── server            ................... API Demo Or Online Toolkit
    ├── test              ................... TestCase Sets
        ├── api           ................... API TestCase
        ├── app           ................... APP TestCase
        ├── feature       ................... Feature TestCase
        ├── monitor       ................... Online TestCase
        ├── ramp          ................... Rampup TestCase
        ├── security      ................... Security TestCase
        ├── stress        ................... Stress/Performance TestCase
        ├── tool          ................... Test Tool
        ├── ui            ................... UI TestCase
        ├── conftest.py   ................... Global Fixture
    ├── .gitignore        ................... Git Ignore Rule
    ├── crontab           ................... Schedule Task Config
    ├── Dockerfile        ................... Docker Build File
    ├── LICENSE           ................... License File
    ├── pytest.ini        ................... Pytest Config
    ├── README.md         ................... Readme File
    ├── requirements.txt  ................... Project Dpendency
    ├── run.sh            ................... Docker Initiate Shell Script 
```