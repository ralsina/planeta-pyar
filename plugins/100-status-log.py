# rawdog plugin to keep a log of how successful we've been fetching feeds
# Adam Sampson <ats@offog.org>

import rawdoglib.plugins, time, threading, re, os

display_as = [
	(r"ok-3.*", "#afffaf"),
	(r"ok-.*", "#40ff40"),
	(r"redirect-.*", "#ffff40"),
	(r"error-timeout", "#ffafaf"),
	(r"error-.*", "#ff4040"),
	(None, "#7fffff"),
	]

class StatusLogPlugin:
	def __init__(self):
		self.lock = threading.Lock()
		self.logfile = "status-log"
		self.outputfile = "status-log.html"

	def config_option(self, config, name, value):
		if name == "statuslogfile":
			self.logfile = value
			return False
		elif name == "statusoutputfile":
			self.outputfile = value
			return False
		else:
			return True

	def mid_update_feed(self, rawdog, config, feed, content):
		if content is None:
			status = "error-parse"
		else:
			s = content.get("status")
			if s is None:
				if len(content["feed"]) == 0:
					status = "error-timeout"
				else:
					status = "ok-nostatus"
			elif s in (301, 302):
				status = "redirect-%d" % s
			elif s / 100 in (4, 5):
				status = "error-%d" % s
			else:
				status = "ok-%d" % s

		s = "%d %s %s" % (time.time(), status, feed.url)
		config.log("Logging status: ", s)

		self.lock.acquire()
		f = open(self.logfile, "a")
		f.write("%s\n" % s)
		f.close()
		self.lock.release()

		return True

	def shutdown(self, rawdog, config):
		period = 12 * 60 * 60
		division = 60 * 60
		divs = period / division

		starttime = time.time() - period
		ts = list(time.localtime(starttime))
		ts[3], ts[4], ts[5] = ts[3] + 1, 0, 0
		starttime = time.mktime(ts)

		try:
			f = open(self.logfile)
		except IOError:
			config.log("No logfile to read")
			return

		# Find a point in the file reasonably close before the start
		# time.
		f.seek(0, 2)
		pos = f.tell()
		while 1:
			pos -= 1024
			if pos < 0:
				pos = 0
			f.seek(pos)
			if pos == 0:
				break
			f.readline()
			l = f.readline()
			if l == "":
				pos = 0
				f.seek(pos)
				break
			if int(l[:-1].split(" ", 2)[0]) < starttime:
				break
		config.log("Starting to read logfile from ", pos)

		feeds = {}

		while 1:
			l = f.readline()
			if l == "":
				break
			(t, status, url) = l[:-1].split(" ", 2)
			if t < starttime:
				continue

			if url not in feeds:
				feeds[url] = [(None, None, -1)] * divs
			n = int((int(t) - starttime) / division)
			if n >= divs:
				config.log("Log entry after current time: ", l[:-1])
				continue

			val = 0
			for (exp, colour) in display_as[:-1]:
				if re.match(exp, status):
					break
				val += 1
			colour = display_as[val][1]

			if feeds[url][n][2] < val:
				feeds[url][n] = (colour, status, val)

		f.close()

		newfn = self.outputfile + ".new"
		f = open(newfn, "w")
		f.write("""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">
<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
    <meta name="robots" content="noindex,nofollow,noarchive">
    <link rel="stylesheet" href="style.css" type="text/css">
    <title>rawdog feed status</title>
</head>
<body id="rawdog">
<div id="page">
<div id="header">
<h1>rawdog feed status</h1>
</div>

<div id="status">
<table id="feedstatus">
<tr>
""")
		for t in range(0, period, division):
			f.write("<th>%s</th>\n" % time.strftime("%Hh", time.localtime(starttime + t)))
		f.write("<th>Feed</th>\n")
		f.write("</tr>\n")

		names = {}
		for url in feeds.keys():
			if url in rawdog.feeds:
				names[url] = rawdog.feeds[url].get_html_name(config)
			else:
				names[url] = url

		urllist = feeds.keys()
		urllist.sort(lambda a, b: cmp(names[a].lower(), names[b].lower()))
		for url in urllist:
			slots = feeds[url]

			f.write("<tr>\n")
			for i in range(divs):
				(colour, status, val) = slots[i]
				if val == -1:
					f.write("<td></td>\n")
				else:
					status = re.sub(r'^.*-', '', status)
					if status == "timeout":
						status = "TO"
					f.write("""<td style="background-color: %s;">%s</td>\n""" % (colour, status))

			if url in rawdog.feeds:
				name = rawdog.feeds[url].get_html_name(config)
			else:
				name = url
			f.write("""<td><a href="%s">%s</a></td>\n""" % (url, name))
			f.write("</tr>\n")

		f.write("""</table>
</div>
</div>
</body>
</html>
""")
		f.close()
		os.rename(newfn, self.outputfile)

		return True

p = StatusLogPlugin()
rawdoglib.plugins.attach_hook("config_option", p.config_option)
rawdoglib.plugins.attach_hook("mid_update_feed", p.mid_update_feed)
rawdoglib.plugins.attach_hook("shutdown", p.shutdown)
