FROM continuumio/miniconda3:latest

WORKDIR /app

COPY docker/environment.yml .

RUN conda env create -f environment.yml && conda clean -afy

COPY src ./src
COPY .env .

EXPOSE 8501

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "vkvideos", "streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
