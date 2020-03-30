#!/usr/bin/env python3

from sys import argv
import csv
import json
from matplotlib import dates, pyplot as plt
import numpy as np

def overhaul():
###
#Completely replaces existing json file with latest data or constructs a new file if none exists\
###
	with open("us-counties.csv") as data:
		entries = csv.reader(data)

		# for line in info:
		# 	print(line)
		entries = list(entries)
		titles = entries[0]
		dict_data = [{titles[i]:entry[i] for i in range(len(titles))} for entry in entries[1:]]
		# print(dict_data)
		output = {}
		for entry in dict_data:
			if not entry["state"] in output:
				# print(entry['state'])
				output[entry["state"]] = {}

			if not entry["county"] in output[entry["state"]]:
				output[entry["state"]][entry["county"]] = {"fips": entry["fips"], "date":[], "deaths":[], "cases":[]}

			for field in ["date", "deaths", "cases"]:
				output[entry["state"]][entry["county"]][field].append(entry[field])

		print(output["California"]["Alameda"])
		return output

def plot(data, state, county, xaxis = "date", yaxis = "cases", xscale = "linear", yscale = "log"):
	fig = plt.figure()

	xdata = data[state][county][xaxis]
	ydata = data[state][county][yaxis]
	xticks = xdata
	yticks = ydata

	if xaxis == "date":
		xdata = dates.datestr2num(xdata)

	if yaxis == "date":
		ydata = dates.datestr2num(ydata)

	xdata = np.array(xdata, dtype = float)
	ydata = np.array(ydata, dtype = float)

	plt.plot(xdata, ydata)
	plt.xscale(xscale)
	plt.yscale(yscale)
	plt.grid()
	if xaxis == "date":
		plt.xticks(xdata, xticks, rotation = 90, fontsize = 5)
	if yaxis == "date":
		plt.yticks(ydata, yticks)

	plt.xlabel(xaxis.capitalize())
	plt.ylabel(yaxis.capitalize())
	plt.title("COVID-19 Data for " + county + " CTY, " + state)
	plt.gcf().tight_layout()
	plt.savefig(state + county + ".png", dpi = 300)


def main():
	output = overhaul()
	plot(output, "New York", "New York City", yaxis = "deaths")
	plot(output, "Washington", "King", xaxis = "cases", yaxis = "deaths")


if __name__ == "__main__":
	main()




