fh = open("access.log")

for line in fh:
	try:
		source_timestamp, request, response, _, _, agent, _ = line.split("\"")
		method, path, protocol = request.split(" ")
		print "User visited URL: http://enos.itcollege.ee" + path
	except ValueError:
		print "Failed to parse:", line
