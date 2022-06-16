#!/usr/bin/env python3
# usage: $ python3 analyze1518.py ./output/phase-*/*/bluetooth.log
import sys
import json
import datetime
import matplotlib.pyplot as plt

#threshold_min = 5 # minutes
#threshold_min = 10 # minutes
#threshold_min = 15 # minutes
#threshold_min = 20 # minutes
#threshold_min = 25 # minutes
threshold_min = 30 # minutes
#threshold_min = 60 # minutes

infilenames_list = sys.argv[1:]
#print(infilenames_list)

rate1518_list = []
number1518_list = []
total_numbers_list = []

for infilename in infilenames_list:
  print(infilename)
  contacts_counter = {}
  with open(infilename, 'r') as infile:
    timestamp_old_dict = {}
    for line in infile:
      #try: 
      data_dict = json.loads(line)
      #except:
      #  continue
      
      #print(data_dict)
      #print(data_dict['id'], int(data_dict['timestamp'])*0.001, datetime.datetime.fromtimestamp(int(data_dict['timestamp'])*0.001), data_dict['data'][0]['bluetooth']['hwAddrHash'], data_dict['data'][0]['bluetooth']['strength'], data_dict['data'][0]['bluetooth']['deviceClass'], data_dict['data'][0]['bluetooth']['majorDeviceClass'])
      id_number = data_dict['id']
      timestamp = int(data_dict['timestamp'])*0.001
      hwAddrHash = data_dict['data'][0]['bluetooth']['hwAddrHash']
      strength = data_dict['data'][0]['bluetooth']['strength']
      deviceClass = data_dict['data'][0]['bluetooth']['deviceClass']
      majorDeviceClass = data_dict['data'][0]['bluetooth']['majorDeviceClass']

      if int(deviceClass) in [524, 276, 1028, 1048, 1796, 516, 1052, 280]: 
        if hwAddrHash not in contacts_counter:
          contacts_counter[hwAddrHash] = 1
          timestamp_old_dict[hwAddrHash] = timestamp
        else:
          if timestamp - timestamp_old_dict[hwAddrHash] >= threshold_min*float(60): # 30 min
            contacts_counter[hwAddrHash] += 1
          timestamp_old_dict[hwAddrHash] = timestamp


  #print(contacts_counter)
  total_number = len(contacts_counter)
  number1518 = 0
  for k, v in contacts_counter.items():
    if v == 1:
      number1518 += 1
#  if total_number >= 10:
  if total_number >= 100:
    #print('rate1518:', infilename, float(number1518)/total_number, number1518, total_number)
    print('rate1518:', float(number1518)/total_number, number1518, total_number)
    rate1518_list.append( float(number1518)/total_number )
    number1518_list.append( number1518 )
    total_numbers_list.append( total_number )

plt.plot(total_numbers_list, rate1518_list, linestyle='', marker='.')
plt.xlabel('Total # of encountered devices')
plt.ylabel('Percentage of Ichi-go Ichi-ye')
plt.savefig('result_plot-min%d.png' % threshold_min)
plt.savefig('result_plot-min%d.eps' % threshold_min)
plt.clf()


plt.hist(number1518_list, bins=100)
plt.xlabel('# of Ichi-go Ichi-ye contacts')
plt.ylabel('Frequency')
plt.savefig('result_hist_num-min%d.png' % threshold_min)
plt.savefig('result_hist_num-min%d.eps' % threshold_min)
plt.clf()

plt.hist(number1518_list, bins=100, log=True)
plt.xlabel('# of Ichi-go Ichi-ye contacts')
plt.ylabel('Frequency')
plt.savefig('result_hist_num_logy-min%d.png' % threshold_min)
plt.savefig('result_hist_num_logy-min%d.eps' % threshold_min)
plt.clf()
 

plt.hist(rate1518_list, bins=100)
plt.xlabel('Percentage of Ichi-go Ichi-ye')
plt.ylabel('Frequency')
plt.savefig('result_hist-min%d.png' % threshold_min)
plt.savefig('result_hist-min%d.eps' % threshold_min)
plt.clf()
 

