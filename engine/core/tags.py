import webtech
from bs4 import BeautifulSoup

def get_tags(ip,port):
    try:
        wt = webtech.WebTech(options={'json': False})
        result = wt.start_from_url(f"http://{ip}:{port}", timeout=1)
        return result
    except webtech.utils.ConnectionException:
        return None

#Filter report from webtech and only return web technologies
def get_web_technologies(ip,banner,port):
    tags_list = []

    if bool(BeautifulSoup(banner, "html.parser").find()):
        #Checks if the banners received contain HTML to analyze technologies
        tags = get_tags(ip,port)

        if tags != None:
            #Removing unnecessary words and duplicates from the received list

            techs = tags.replace("\t-","").splitlines()
            filt = [x.strip() for x in techs if not "Detected" in x and not "Target" in x]
            tags_list.append(filt)

        flat_list = [item for sublist in tags_list for item in sublist]
        if flat_list:
            return list(set(flat_list))
    else:
        return None

