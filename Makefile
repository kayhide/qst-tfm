dev:
	fd .py | entr -cdr python src/main.py
.PHONY: dev

browse:
	feh -. -d output
.PHONY: browse
