FROM python:alpine
COPY main.py main.py
COPY patient.py patient.py
RUN pip install fastapi uvicorn pymongo pydantic
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# Same
# CMD uvicorn main:app --host 0.0.0.0 --port 8000 
