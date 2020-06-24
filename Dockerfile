FROM python:3.7
COPY gameloop.py .
COPY ai_controller.py .
COPY data_controller.py .
COPY gameplay_controller.py .
COPY gameplay_models.py .
COPY simulate.c .
COPY training_data.csv .
RUN gcc -o simulate simulate.c -fopenmp
RUN pip install pandas
RUN pip install tensorflow-cpu                  
RUN pip install boto3
RUN python -c "import ai_controller; ai_controller.setup_model(); ai_controller.train_model(5)"