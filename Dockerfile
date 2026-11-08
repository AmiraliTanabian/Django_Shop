FROM python:3.14
LABEL maintainer=Amirali_Tanabian
RUN adduser user

# --chown : For debug use db (attempt to write a readonly database)
COPY --chown=user:user ./ ./

# RUN pip install -r requirments.txt -i https://mirror-pypi.runflare.com/
RUN pip install -r requirments.txt 

USER user
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]