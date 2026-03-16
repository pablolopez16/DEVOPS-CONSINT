FROM python:3.11   

WORKDIR /application              

COPY requirements.txt . 
RUN pip install -r requirements.txt  

COPY app.py .       
COPY startapplication.sh . 

RUN chmod +x startapplication.sh       

EXPOSE 8000                 

CMD ["./startapplication.sh"] 