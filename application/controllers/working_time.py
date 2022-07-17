from application.services.working_time import WorkingTimeService

class WorkingTimeController():

    def get_working_time(self):
        return WorkingTimeService().get_working_time()
   
    def update_working_time(self, doc):
        doc["working_time"]["morning"] = [time.strftime("%H:%M") for time in doc["working_time"]["morning"]]
        doc["working_time"]["afternoon"] = [time.strftime("%H:%M") for time in doc["working_time"]["afternoon"]]
        doc["holidays"] = [time.strftime("%d-%m") for time in doc["holidays"]]
        return WorkingTimeService().update_working_time( doc)
   