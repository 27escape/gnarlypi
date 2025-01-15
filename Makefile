init:
	sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED & pip install -r requirements.txt

test:
	py.test tests

.PHONY: init test
