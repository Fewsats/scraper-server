freeze:
	pip freeze > requirements.txt
install:
	python -m venv venv
	pip install -r requirements.txt
run:
	gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:9111
clean:
	rm -rf venv
