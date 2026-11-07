FROM python:3.11-slim

# Membuat user non-root untuk keamanan sistem
RUN useradd --create-home appuser
WORKDIR /home/appuser

# Salin skrip aplikasi
COPY app.py .

# Ubah kepemilikan file ke user non-root
RUN chown -R appuser:appuser /home/appuser
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
