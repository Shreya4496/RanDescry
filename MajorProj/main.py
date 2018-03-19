import pyshark
import argparse
#from detection_ransomware import *
import csv
import joblib
import os
import pickle
import sys
from sklearn.externals import joblib

def detection(filename):
	flag=0
	with open(filename) as csvfile:
		readCSV=csv.reader(csvfile,delimiter=',')
		
		for row in readCSV:
			
			clf = joblib.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),'classifier/classifier.pkl'))	 

			res= clf.predict([row])[0]
			if res==0 :
				print("File contains ransomware")
				flag=1
				break


	if flag==0:
		print("File is legitimate")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Detect malicious files')
    parser.add_argument('FILE', help='File to be tested')
    args = parser.parse_args()
    cap = pyshark.FileCapture(args.FILE)
    with open('data_h.csv', 'a') as f:
	    writer = csv.writer(f)
    i=0    
    no_of_packets=0	
    timepersec=0
    packetsize=0
    rstcnt=0
    set_src=set()
    set_dst=set()
    for packet in enumerate(cap):
           	   no_of_packets+=1
		   packetsize=packetsize+int(cap[no_of_packets-1].length)
		   #print no_of_packets
		   try :
			    flagval=cap[no_of_packets-1]['TCP'].flags
			    if int(flagval, 16) & 4 :
			      rstcnt=rstcnt+1
		   except KeyError as e:
		            print ""
				
		   
		   src_ip= cap[no_of_packets-1]['IP'].src
		   s_ip=src_ip.split('.')
		   ip=256*(256*(256*int(s_ip[0])+int(s_ip[1]))+int(s_ip[2]))+int(s_ip[3])
		   src_ip=ip
		   set_src.add(src_ip)
		   dest_ip= cap[no_of_packets-1]['IP'].dst
           	   d_ip=dest_ip.split('.')
		   ip=256*(256*(256*int(d_ip[0])+int(d_ip[1]))+int(d_ip[2]))+int(d_ip[3])
		   dest_ip=ip
		   set_dst.add(dest_ip)
                		   
    
	
    # 1. Total number of packets
    #print no_of_packets

    # 2. Total time elapsed
    t=cap[no_of_packets-1].sniff_time-cap[0].sniff_time
    t=str(t)	
    time=t.split(':')
    t1=int(time[0])*12+int(time[1])*60+int(round(float(time[2])))
    #print t1
    
    # 3. avg packet per sec
    avgtime=no_of_packets/t1
    #print avgtime
    
    # 4. Average Packet Size
    avgpacketsize= packetsize/no_of_packets
    #print avgpacketsize

    # 5. Total bytes
    #print packetsize

    # 6. Average bytes per second
    avgbyte = packetsize/t1
    #print avgbyte

    # 7. RST Cnt
    #print rstcnt

    # 8. Unique no. of src IPs
    #print len(set_src)

    # 9. Unique no. of dest IPs
    #print len(set_dst)

    rows=[no_of_packets,t1,avgtime,avgpacketsize,packetsize,avgbyte,rstcnt,len(set_src),len(set_dst)]
    with open(r'data_h.csv', 'a') as f:
	    writer = csv.writer(f)
	    writer.writerow(rows)
    detection('data_h.csv')
   




