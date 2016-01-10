Máster en Ingeniería Informática
Universidad Complutense de Madrid
Sistemas de gestión de datos y de la información
Grupo 3: Hristo Ivanov, Alberto Lorente
10 Enero 2016

La presentación es el archivo presentacion.pdf.

El código fuente podemos encontrar en los archivos:
  prism.py
  id3.py

Los archivo, que contienen los cunjuntos de entrenamiento utilizados en la
presentación son los siguientes:
  id3_problem.csv
  incomplete.csv
  lens.csv

Podemos ejecutar el código de la siguiente manera:
  python prism.py lens.csv

Ambos algoritmos generan un archivo .dot con el resultado obtenido. Podemos
visualizar estos archivos:
  xdot out_id3.dot
  xdot out_prism.dot

Create .zip:
  zip Grupo_3.zip id3_problem.csv incomplete.csv lens.csv prism.py id3.py README.txt presentacion.pdf
