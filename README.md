Create Virtual environment first
python -m venv venv
or 
py -m venv venv

Activate Virtual environment
Linux:
source venv/bin/activate
Windows Git Bash:
source venv/Scripts/activate
Windows CMD:
.\venv\Scripts\activate


On Linux: Just install requirements for Project
pip install -r requirements.txt


On Windows :
Step 1: Install git for Windows

Step 2: Clone this repository and go inside the folder using the following commands

git clone https://github.com/RvTechiNNovate/face_recog_dlib_file.git venv/face_recog_dlib_file
cd venv/face_recog_dlib_file

Step 3: Enter the following command to install dlib and cmake using pip

Python 3.7:
pip install dlib-19.19.0-cp37-cp37m-win_amd64.whl

Python 3.8:
pip install dlib-19.19.0-cp38-cp38-win_amd64.whl

Step 4: Install requirements for Project
cd ../..
pip install -r requirements.txt

Start server
cd src
python run_server.py