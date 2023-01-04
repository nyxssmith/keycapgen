FROM ubuntu:20.04


RUN apt update && apt install -y libstdc++6 python3-pip python3 
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install meshlib jupyter jupyterlab

COPY CharacterOntoKeycap.py CharacterOntoKeycap.py

CMD ["sh", "-c", "python3 /CharacterOntoKeycap.py"]

#CMD ["sh", "-c", "jupyter lab --allow-root --no-browser --ip=*"]

#CMD ["jupyter","--ip 0.0.0.0","--allow root"]
#CMD ["jupyter","lab","--ip","0.0.0.0","--allow root"]