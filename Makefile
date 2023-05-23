test:
	python3 -m pytest unittests.py

test_cli:
	python3 cli.py --key_file tests/TC-A.key --sys_file tests/TC-A-2.response