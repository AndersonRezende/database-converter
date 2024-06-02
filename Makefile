#.PHONY: install format lint test sec
.PHONY: install format lint

install:
	@sudo apt install python3-pip
	@sudo apt install build-essential
	@sudo apt install libssl-dev libffi-dev libncurses5-dev zlib1g zlib1g-dev libreadline-dev libbz2-dev libsqlite3-dev make gcc
	@pip install -r requirements.txt
format:
	@blue .
lint:
	@blue . --check
test:
	@pytest -v
sec:
	@pip-audit

