FROM python:3.14
LABEL maintainer=Amirali_Tanabian

RUN adduser --disabled-password --gecos "" user

WORKDIR /app

COPY requirments.txt .
RUN pip install -r requirments.txt

COPY --chown=user:user . .
RUN chown user:user /app

USER user
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]