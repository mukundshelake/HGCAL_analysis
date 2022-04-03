# require cms inviroment to run this file
import fileinput, string, sys, os, time, datetime
import csv
from array import array
import math
import ROOT as R
import argparse as arg
import numpy as np

parser = arg.ArgumentParser(description='input and output file discription')
parser.add_argument('-f', '--inout', dest='files', default=('input.txt','out.csv'), type=str, nargs=2, help="input ['input.txt',out.csv]")

args = parser.parse_args()
print args.files[0],args.files[1]

def csv_reader(file):
    x,y,z = array('d'), array('d'), array('d')
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        line_count = 0
        for row in csv_reader:
            if (line_count <= 7):
		line_count = line_count+1
		#print row
            elif(line_count >= 8 and line_count <= 31):
		line_count = line_count+1
		#print row
		x.append(float(row[0]))
		y.append(float(row[1]))
		z.append(float(row[2]))
	return x,y,z

def csv_writer(csvfile,txtfile,Nodge_width,NG_tG_NG_length,MB_to_MB_length):
    write_fist_line = False
    if not os.path.exists(csvfile):write_fist_line = True
    with open(csvfile, mode='a') as cordinate_file:
        cordinate_writer = csv.writer(cordinate_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if(write_fist_line):cordinate_writer.writerow(["txtfile","Nodge_width","NG_tG_NG_length","MB_to_MB_length"])
        #cordinate_writer.writerow(["150.0", "0.0","0.0","0.0"])
        #for i in range(0, len(x)):
        cordinate = [txtfile,Nodge_width,NG_tG_NG_length,MB_to_MB_length]
            # print(cordinate)
        cordinate_writer.writerow(cordinate)

def Get_Nodge_width(x,y):  # Nodge width calculation
	Nodge_width = array('d') 
	for nodge_cor in [[3,4],[5,6],[11,12],[13,14],[19,20],[21,22]]:
	     Nodge_width.append(math.sqrt(pow(x[nodge_cor[0]-1]-x[nodge_cor[1]-1],2)+pow(y[nodge_cor[0]-1]-y[nodge_cor[1]-1],2))) # we doing -1 since array start from zero
	return Nodge_width

def Get_side_MB_to_MB(x,y): # Mouse Bite to Mouse Bite side length calulation
 	MB_to_MB_side = array('d')
	for MB_cor in [[2,7],[8,9],[10,15],[16,17],[18,23],[24,1]]:
		 MB_to_MB_side.append(math.sqrt(pow(x[MB_cor[0]-1]-x[MB_cor[1]-1],2)+pow(y[MB_cor[0]-1]-y[MB_cor[1]-1],2))) # we are doing -1 sinace array start from zero
	return MB_to_MB_side

def Get_side_NG_to_NG(x,y): # Nodge to Nodge side length calulation
        NG_to_NG_side = array('d')
        for NG_cor in [[4,5],[12,13],[20,21]]:
		NG_to_NG_side.append(math.sqrt(pow(x[NG_cor[0]-1]-x[NG_cor[1]-1],2)+pow(y[NG_cor[0]-1]-y[NG_cor[1]-1],2))) # we are doing -1 sinace array start from zero
	return NG_to_NG_side

if __name__ == "__main__":
	filepath = ""
	inputfile = args.files[0]
	csvfile = args.files[1]

	x,y,z = csv_reader(filepath+inputfile)	
	print "x len = ",len(x)," ",x
	print "y len = ",len(y)," ",y
	print "z len = ",len(z)," ",z
	Nodge_widths = Get_Nodge_width(x,y)
	Nodge_width = np.average(np.array(Nodge_widths))
	print  "Nodge_widths len = ",len(Nodge_widths)," ",Nodge_widths, " Nodge width = ",Nodge_width
	MB_to_MB_lengths = Get_side_MB_to_MB(x,y)
	MB_to_MB_length = np.average(np.array(MB_to_MB_lengths))	
	print "MB_to_MB_lengths len = ",len(MB_to_MB_lengths)," ",MB_to_MB_lengths," MB_to_MB_length = ",MB_to_MB_length
	NG_to_NG_lengths = Get_side_NG_to_NG(x,y)
	NG_to_NG_length = np.average(np.array(NG_to_NG_lengths))
	print "NG_to_NG_lengths len = ",len(NG_to_NG_lengths)," ",NG_to_NG_lengths, " NG_to_NG_length = ",NG_to_NG_length

	csv_writer(csvfile,inputfile,Nodge_width,NG_to_NG_length,MB_to_MB_length)

	"""c1 = R.TCanvas( 'c1', 'A Simple Graph Example', 600,600,600,600 )
	c1.SetFillColor( 33 )
	c1.SetGrid()
	
	gr = R.TGraph( len(x), x, y )
	gr.SetLineColor( 2 )
	gr.SetLineWidth( 4 )
	gr.SetMarkerColor( 4 )
	gr.SetMarkerStyle( 21 )
	gr.SetTitle( ' Baseplate cornor corrdinates' )
	gr.GetXaxis().SetTitle( 'X ( mm)' )
	gr.GetYaxis().SetTitle( 'Y ( mm)' )
	gr.GetYaxis().SetRangeUser( -5,200 )
	gr.Draw( 'AP' )
	c1.Print("Plots/"+inputfile.rsplit(".",2)[0]+".png")
	c1.Print("Plots/"+inputfile.rsplit(".",2)[0]+".pdf")"""
	
	#raw_input()
