import random
import re
import shutil
import sys, os
import urllib.request
from datetime import datetime, timedelta
from PIL import Image
from dateutil import relativedelta
sys.path = [os.path.dirname(sys.path[0])] + sys.path

from data import data
from application import config, create_app_without_api
from application.models.profile import Profile
from application.models.attendance import Attendance

def check_working_day(thisdate):
    holidays = {
        datetime(thisdate.year, 4, 30),
        datetime(thisdate.year, 5, 1),
        datetime(thisdate.year, 9, 2)
    }
    if thisdate.weekday() < 5 and thisdate not in holidays:
        return True
    return False

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def gen_data():
    models = []
    for index, user in enumerate(data):
        doc = {
            "name": user["name"],
            "code": str(20209062 + index),
            "position": "Nhân viên",
            "creation_date": datetime(2022, 3, 15)
        }
        model = Profile(**doc)
        models.append(model)
    Profile.objects.insert(models, load_bulk=False)

def gen_attendace():
    attendances = []
    ids = Profile.objects().scalar("id")
    start_date = datetime(2022, 3, 15)
    end_date = datetime.now()
    for single_date in daterange(start_date, end_date):
        if not check_working_day(single_date):
            continue  
        for id in ids:
            arrive_time = single_date.replace(hour=7, minute=40) + relativedelta.relativedelta(minutes=random.randint(0, 25))
            leave_time = single_date.replace(hour=16, minute=59) + relativedelta.relativedelta(minutes=random.randint(0, 10))
            doc = {
                "profile_id": id,
                "creation_date": single_date,
                "attendance_times": [arrive_time, leave_time]
            }
            attendance = Attendance(**doc)
            attendances.append(attendance)
    Attendance.objects.insert(attendances, load_bulk=False)


def download_img(image_url, file_path, file_name):
    full_path = os.path.join(file_path, file_name + '.jpg')
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,} 
    request=urllib.request.Request(image_url,None,headers)
    response = urllib.request.urlopen(request)
    # install PIL package to convert the response into a PIL Image object to further save it
    image=Image.open(response)
    image.save(full_path)
    pass

def generate_face():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'faces')
    for i in range(442, 1200):
        download_img("https://thispersondoesnotexist.com/image", path, "{}".format(i))

def get_url():
    fp = urllib.request.urlopen("https://this-person-does-not-exist.com/en")
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()

    img = re.findall(r"<img id=\"avatar\"(.*?)src=\"(.*?)\" alt=\"\">", mystr)
    if img:
        return img[0][1]
    return None

def generate_face2():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'faces')
    for i in range(1200):
        img = get_url()
        if img:
            download_img("https://this-person-does-not-exist.com/" + img, path, "{}".format(i))


def pick_image_to_profile():
    ids = Profile.objects().scalar("id")
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'faces')
    for index, id in enumerate(ids):
        profile_id = str(id)
        folder_path = os.path.join(config.PortalApi.IMAGES_FOLDER_PATH, profile_id)
        shutil.rmtree(folder_path, ignore_errors=True)
        os.mkdir(folder_path)
        filename = path + "/{}.jpg".format(index)
        if os.path.isfile(filename):
            shutil.copy(filename, folder_path)

if __name__ == "__main__":
    app = create_app_without_api()
    with app.app_context():
        # gen_data()
        # gen_attendace()
        # generate_face()
        # pick_image_to_profile()
        # generate_face2()
        pass
    