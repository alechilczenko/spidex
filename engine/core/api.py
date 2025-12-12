import requests
from config import Config

def submit_data(result,server_name,api_endpoint):
    requests.post("{}{}".format(server_name,api_endpoint), json=result)

def submit_report(total,found,exec_time,start,end):
    report = {
        "found":found,
        "exec_time": str(exec_time),
        "total":total,
        "start_time": start.strftime("%m/%d/%Y, %H:%M:%S"),
        "end_time": end.strftime("%m/%d/%Y, %H:%M:%S")
    }
    submit_data(report,Config.SERVER_NAME,Config.API_REPORT_ENDPOINT)

