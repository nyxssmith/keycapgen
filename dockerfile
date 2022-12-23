FROM pymesh/pymesh


RUN apt update && apt install -y libstdc++6
RUN pip install jupyter jupyterlab


CMD ["sh", "-c", "jupyter lab --allow-root --no-browser --ip=*"]

#CMD ["jupyter","--ip 0.0.0.0","--allow root"]
#CMD ["jupyter","lab","--ip","0.0.0.0","--allow root"]