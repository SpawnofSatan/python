import os
import urllib
 
# Following is the directory with log files,
# On Windows substitute it where you downloaded the files
root = "/home/kpurru/logs"

keywords = "Windows", "Linux", "OS X", "Ubuntu", "Googlebot", "bingbot", "Android", "YandexBot", "facebookexternalhit"
d = {}
urls = {}
users = {}

total = 0
import gzip

for filename in os.listdir(root):
    if not filename.startswith("access.log"):
#        print "Skipping unknown file:", filename
        continue
    if filename.endswith(".gz"):
        continue
        fh = gzip.open(os.path.join(root, filename))
    else:
        fh = open(os.path.join(root, filename))
    print "Going to process:", filename
    for line in fh:
        total = total + 1
        try:
            source_timestamp, request, response, referrer, _, agent, _ = line.split("\"")
            method, path, protocol = request.split(" ")
            _, status_code, content_length, _ = response.split(" ")
            content_length = int(content_length)
            path=  urllib.unquote(path)
            print "Response bits:", response
            if path.startswith("/~"):
                username, remainder = path[2:].split("/", 1)
                try:
                    users[username] = users[username] + content_length
                except:
                    users[username] = 1
                print "Got user;", username
                
            url = "http://enos.itcollege.ee" + path
            
            try:
                urls[url] = urls[url] + 1
            except:
                urls[url] = 1
                                            
            for keyword in keywords:
                if keyword in agent:
                    try:
                        d[keyword] = d[keyword] + 1
                    except KeyError:
                        d[keyword] = 1
                    break # Stop searching for other keywords
        except ValueError:
            pass # This will do nothing, needed due to syntax   


print("Top visited users") 
results = users.items()
results.sort(key = lambda item:item[1], reverse=True)
for user, transferred_bytes in results[:30]:
    print user, " ==>" , transferred_bytes / (1024 * 1024), "MB"
                     
print("Top visited URL-s") 
results = urls.items()
results.sort(key = lambda item:item[1], reverse=True)
for url, hits in results[0:5]:
    print url, " ==>" , hits, "(", hits * 100 / total, "%)"

