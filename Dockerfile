FROM python:3.12.3
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt -q
COPY . .
CMD ["solara", "run", "solara_app.py", "--host", "0.0.0.0", "--port", "8000"]