
# base of miniconda image
FROM python:3.9.13

# streamlit-specific commands
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'
RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml'

# copying all analysis code to image
COPY . .
WORKDIR /the-leapfrog-calculator-main
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# run app
CMD ["streamlit", "run", "app.py"]