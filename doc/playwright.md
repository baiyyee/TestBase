- playwright

```console

playwright codegen --save-storage=auth.json
playwright codegen --load-storage=auth.json


pytest --slowmo 100
pytest --browser chromium
pytest --browser-channel chrome
pytest --base-url http://localhost:8080
playwright show-trace trace.zip
pytest --headed -slowmo=2000 --tracing retain-on-failure --video retain-on-failure --screenshot only-on-failure

```