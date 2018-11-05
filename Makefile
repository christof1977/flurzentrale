.PHONY: run app clean
# .SILENT:

## Flurzentrale-GUI Makefile
## -------------------------
## ⁣
## This file contains various targets to support working with this repository.


#SRC:=gui
#ENV_BIN:=$(ENV)/bin
#ENV_PYTHON:=$(ENV_BIN)/$(PYTHON)
ENV_PYTHON:=/usr/local/bin/python3

## ⁣
## Deployment:

run:		## Run Interstellar-GUI
#run: env
	$(ENV_PYTHON) main.py

env: $(ENV_BIN)/activate install
$(ENV_BIN)/activate: requirements.txt
	test -d $(ENV) || $(PYTHON) -m $(VENV) $(ENV)
	$(ENV_PYTHON) -m pip install -qq --upgrade pip
	$(ENV_PYTHON) -m pip install -qq -r requirements.txt
	touch ./$(ENV_BIN)/activate


clean:		## Remove generated files (env, docs, ...)
	rm -rf build/
	rm -rf dist 

app:
	/usr/local/bin/pyinstaller --windowed --onefile --icon=icon.icns flurzentrale.spec


help:		## Show this help
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

