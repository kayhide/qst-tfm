dev:
	fd .py | entr -cdr python src/main.py
.PHONY: dev

browse:
	feh -. output
.PHONY: browse
