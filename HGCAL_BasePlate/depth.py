import fileinput, string, sys, os, time, datetime
import csv
from array import array
import math
import ROOT as R
import argparse as arg
import numpy as np

parser = arg.ArgumentParser(description='input and output file discription')
parser.add_argument('-f', '--inout', dest='files', default=('input_central.txt','input_obloid.txt','out.csv'), type=str, nargs=3, help="input ['input_central.txt','input_obloid.txt',out.csv]")

args = parser.parse_args()
print args.files[0],args.files[1],args.files[2]

def csv_reader(file):
    x,y,z = array('d'), array('d'), array('d')
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        line_count = 0
        for row in csv_reader:
            if (line_count <= 7):
		line_count = line_count+1
		#print row
            elif(line_count >= 8 and line_count <= 17):
		line_count = line_count+1
		#print row
		x.append(float(row[0]))
		y.append(float(row[1]))
		z.append(float(row[2]))
	return x,y,z

def csv_writer(csvfile,BasePlate,Avg_central_depth,Avg_obloid_depth):
    write_fist_line = False
    if not os.path.exists(csvfile):write_fist_line = True
    with open(csvfile, mode='a') as cordinate_file:
        cordinate_writer = csv.writer(cordinate_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if(write_fist_line):cordinate_writer.writerow(["Baseplate","Avg_depth_of_central_hole","avg_depth_of_obloid_hole"])
        #cordinate_writer.writerow(["150.0", "0.0","0.0","0.0"])
        #for i in range(0, len(x)):
        cordinate = [BasePlate,Avg_central_depth,Avg_obloid_depth]
            # print(cordinate)
        cordinate_writer.writerow(cordinate)

def Get_depth(z):
	lower = np.average(z[:4])
	upper = np.average(z[5:])
	depth = upper - lower
	return round(depth,4)

if __name__ == "__main__":
	filepath = ""
	inputfile_c = args.files[0]
	inputfile_o = args.files[1]
	csvfile = args.files[2]

	x,y,z = csv_reader(filepath+inputfile_c)
	central_depth = Get_depth(z)

	x,y,z = csv_reader(filepath+inputfile_o)
	obloid_depth = Get_depth(z)	
	#print(central_depth,obloid_depth)
	Baseplate = 'Baseplate6'
	csv_writer(csvfile,Baseplate,central_depth,obloid_depth)
