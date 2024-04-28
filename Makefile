VENV := venv
PYTHON := python3

# Target to create the virtual environment
venv:
	$(PYTHON) -m venv $(VENV)
	source $(VENV)/bin/activate && pip install -r requirements.txt

# Target to clean up the virtual environment
clean:
	rm -rf $(VENV)

.PHONY: venv activate clean