# Stockholm
Ransomware project from 42 School

## Description
The goal of this project is coding a ransomware program in Python.

The program looks for a folder called `infection` in the home of the user running the script. If the folder is found, it will encrypt every file with an extension afected by WannaCry leaving a .ft file extension to every file encrypted, and write a file called `key.key` in the folder where the user is running the program

In case of testing, strongly recommend using a docker container or a VM. Be careful!