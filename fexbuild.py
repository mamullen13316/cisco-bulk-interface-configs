# This script will create FEXs and configure the interfaces to be used for the fabric uplinks.
# Please send any errors/comments/suggestions to mamullen@cisco.com.

# fex_mod_begin = The module number where the 1st FEX fabric link will be connected
# fex_number = The beginning FEX number,  will be incremented by one for each FEX
# fex_port_begin = The port that the first FEX will be connected to
# fex_uplinks = The number of fabric uplinks for FEXs
# mod_ports = The number of ports on a module
# breakout is a boolean that can be set to True if 40G ports are using 4x10 breakout

# Variables for testing in the interactive shell. These are overwritten by the command line
# arguments when executing from the command line.
fex_mod_begin = 3 ;
fex_number = 100 ;
fex_port_begin = 1 ;
fex_uplinks = 2 ;
fex_qty = 9
breakout = 'TRUE' ;
mod_ports = 12


# Create the command line arguments using the argparse module
 
import argparse
 
parser = argparse.ArgumentParser(description='''fexbuild.py -- Version 1.0 --
This script will create FEXs and configure the interfaces to be used for the fabric uplinks.
Please send any errors/comments/suggestions to mamullen@cisco.com.''')
parser.add_argument('-module',help='The beginning module number to start creating fabric links. The default is 1.',required=False, default=1)
parser.add_argument('-port',help='The beginning port number to start creating fabric links.  The default is 1.', required=False, default=1)
parser.add_argument('-uplinks',help='The number of fabric uplinks to use for each FEX.  The default is 2.',required=False, default=2)
parser.add_argument('-fex_count',help='The number of FEXs you are creating. The default is 1.',required=True, default=1)
parser.add_argument('-module_ports',help='The number of ports available on the module for creating uplinks. The default is 48.',required=False, default=48)
parser.add_argument('-fex_number',help='The beginning FEX number. The default is 100.',required=False,default=100)
parser.add_argument('-fex_increment',help='''The number by which you want to increment the FEX number.
Useful for example if you want to put all the odd FEXs on one side and even on the other. The default is 1.''',required=False, default=1)
parser.add_argument('-breakout',help='Specify this flag to do 40G to 4x10G interface breakout.',required=False,action="store_true",default=False)
parser.add_argument('-fex_aa',help='Specify this flag if the FEXs will be dual homed to two parent switches.',required=False,action="store_true",default=False)
parser.add_argument('-fcoe',help='Specify this flag to configure fcoe on all FEXs.',required=False,action="store_true",default=False)
parser.add_argument('-fcoe_even',help='Specify this flag if you only want to configure fcoe on the even numbered FEXs', required=False,action="store_true",default=False )
parser.add_argument('-fcoe_odd',help='Specify this flag if you only want to configure fcoe on the odd numbered FEXs', required=False,action="store_true",default=False )
parser.add_argument('-filename',help='Specify a filename to store the output.',required=False, default="")


args = parser.parse_args()

fex_mod_begin = int(args.module)
fex_number = int(args.fex_number)
fex_port_begin = int(args.port)
fex_uplinks = int(args.uplinks)
fex_qty = int(args.fex_count)
mod_ports = int(args.module_ports)
breakout = args.breakout
fex_aa = args.fex_aa
fex_increment = int(args.fex_increment)
fcoe = args.fcoe
fcoe_even = args.fcoe_even
fcoe_odd = args.fcoe_odd
output_file = args.filename


## show values ##
print ("*****************************************************")
print ("Beginning module number: %s" % str(fex_mod_begin) )
print ("Number of ports on module: %s" % str(mod_ports) )
print ("Beginning port is %s" % str(fex_port_begin) )
print ("Total number of FEXs to configure: %s" % str(fex_qty) )
print ("Number of uplinks per FEX: %s" % str(fex_uplinks) )
print ("Beginning FEX number is: %s" % str(fex_number) )
print ("FEX number will increment by: %s" % str(fex_increment) )
print ("Using 40G-to-4x10G breakout: %s" % breakout )
print ("FEXs will be dual-homed (aka. FEX active/active): %s" % fex_aa )
print ("Configure FCoE: %s" % fcoe )
print ("Configure FCoE only on even FEXs: %s" % fcoe_even )
print ("Configure FCoE only on odd FEXs: %s" % fcoe_odd )
print ("Output will be saved to file: %s" % output_file )
print ("******************************************************")

import sys

if sys.version_info[1] == 3 :
	input_var = input("Do you want to continue (Y/N): ")
else :
	input_var = raw_input("Do you want to continue (Y/N): ")	

if input_var.lower() != 'y' :
	exit()

print ("")
print ("Continuing...")
print ("")

def CreateOutput(output_list):
	'''Function to print the output to screen and write to file if specified'''
	for item in output_list:
		print (item)
		if output_file != "":
			f.write(item)
			f.write('\n')

# Begin main program execution

if output_file != '' :
	f = open (output_file,'w')

output_list = []
breakout_count = 0
for i in range (1,fex_qty+1) :
	output_list.append ('fex ' + str(fex_number))
	output_list.append (' pinning max-links 1')
	if fcoe :
		output_list.append (' fcoe')
# if the fcoe_even flag is set check if fex_number is even
	if fcoe_even and fex_number%2==0 :
		output_list.append (' fcoe')
# if the fcoe_odd flag is set check if fex_number is odd
	if fcoe_odd and fex_number%2!=0 :
		output_list.append (' fcoe')
	output_list.append ('')
	output_list.append ('interface port-channel' + str(fex_number))
	output_list.append (' switchport mode fex-fabric')
	output_list.append (' fex associate ' + str(fex_number))
	if fex_aa :
		output_list.append (' vpc ' + str(fex_number))
	output_list.append ('')

# Check if doing 40G to 4x10G breakout, if TRUE then execute this block
	if breakout :		
		for x in range (1,fex_uplinks + 1) :
			if fex_port_begin > mod_ports :
				fex_mod_begin = fex_mod_begin + 1
				fex_port_begin = 1
			breakout_count = breakout_count + 1
			output_list.append ('interface Ethernet' + str(fex_mod_begin) + '/' + str(fex_port_begin) + '/' + str(breakout_count))
			output_list.append (' switchport mode fex-fabric')
			output_list.append (' channel-group ' + str(fex_number) + ' force')
			output_list.append (' no shut')
			output_list.append ('')
			if breakout_count == 4 :
				breakout_count = 0
				fex_port_begin = fex_port_begin + 1
			if x == fex_uplinks :
				fex_number = fex_number + fex_increment
		
	else :
# No breakout	
		for x in range (1,fex_uplinks + 1) :
			if fex_port_begin > mod_ports :
				fex_mod_begin = fex_mod_begin + 1
				fex_port_begin = 1
		
			output_list.append ('interface Ethernet' + str(fex_mod_begin) + '/' + str(fex_port_begin))
			output_list.append (' switchport mode fex-fabric')
			output_list.append (' channel-group ' + str(fex_number) + ' force')
			output_list.append (' no shut')
			output_list.append ('')
			fex_port_begin = fex_port_begin + 1
			if x == fex_uplinks :
				fex_number = fex_number + fex_increment

CreateOutput(output_list)

if output_file != '' :
	f.close()




		
		