# # This script generates bulk interface configuration for switches running NX-OS.
# 
# Please send any errors/comments/suggestions to mamullen@cisco.com.

# desc = The text portion of the description
# desc_counter = An incrementing number appended to the description (ex. C-SERIES-1, C-SERIES-2...
# mod_begin = The beginning module number
# mod_end = The ending module number
# mod_ports = The number of ports on the module
# pc_number = The starting point for port-channel and vPC number
# pc_links = The number of links in a port-channel
# port_begin = The beginning port number 
# port_total = The total number of ports to be configured (if using 4x10G breakout, list number of logical interfaces)
# port_mode = The switchport mode of the interface,  valid values are TRUNK or ACCESS
# port_vlans = A string containing the allowed VLAN list. Use a single vlan if port mode is ACCESS. 
#              Enter a blank space ('') to leave out the allowed vlans.
# breakout = a boolean value which indicates whether 40G to 4x10G breakout is to be used
# fex_hifs = a boolean value which indicates whether the ports are host interfaces on a FEX
# fex_number = the beginning FEX number
# vpc = a boolean value which indicates whether port-channels/vpc will be configured

# These variables can be used for testing in the interactive shell.
# They will get overwritten by command line arguments during cmd line
# execution

desc = 'HPC7000-' ;
desc_counter = 1 ;
mod_begin = 1 ;
mod_ports = 48 ;
pc_number = 1 ;
pc_links = 2 ;
port_begin = 1 ;
port_total = 15 ;
port_mode = 'TRUNK'
port_vlans = ''
fex_hifs = 'True'
fex_number = 100
breakout = 'False'
vpc = 'True'

# Accepting the command line arguments with argparse

import argparse
 
parser = argparse.ArgumentParser(description='''interfacebuild.py -- Version 1.0 --
This script generates bulk interface configuration for switches running NX-OS. 
Please send any errors/comments/suggestions to mamullen@cisco.com.''')
parser.add_argument('-ports',help='Total number of ports to be configured.', required=True)
parser.add_argument('-port_begin',help='The port number to begin numbering.  The default is 1.', required=False, default=1)
parser.add_argument('-module', help='The number of the module to start numbering. The default is 1.',required=False, default=1)
parser.add_argument('-module_ports', help='The number of ports on the module. The default is 48.',required=False, default=48)
parser.add_argument('-mode',help='The switchport mode to be used. Valid values are ACCESS or TRUNK', required=False, default='TRUNK')
parser.add_argument('-vlans',help='The vlan (access mode) or vlan list (trunk mode). Default is no vlan list specified.',required=False,default='')
parser.add_argument('-desc',help='The description applied to each interface. If spaces in the description, it must be enclosed in quotes.', required=False,default='')
parser.add_argument('-desc_count', help='An incrementing number appended to the description (ex. SERVER-1, SERVER-2...). This is the starting value. The default value is 1', required=False, default=1)
parser.add_argument('-vpc', help='Specify this flag to create port-channels and vPCs.', required=False, action="store_true", default=False)
parser.add_argument('-pc_links',help='The number of links in a port-channel. The default is 2.',required=False,default=2)
parser.add_argument('-pc_number',help='The starting port-channel number.',required=False,default=1)
parser.add_argument('-breakout',help='Specify this flag to do 40G to 4x10G interface breakout.',required=False,action="store_true",default=False)
parser.add_argument('-breakout_type',help='Specify 40G for 40G to 4x10G breakout, or 100G for 100G to 10x10G breakout.',required=False,default="40G")
parser.add_argument('-fex',help='Specify this flag to create FEX HIFs. Note that this will not work with the breakout flag set.',action="store_true",default=False)
parser.add_argument('-fex_number',help='Specify the starting FEX number. The default is 100.',default=100)
parser.add_argument('-vfc',help='Specify this flag to create Virtual Fiber Channel interfaces.', required=False,action="store_true",default=False)
parser.add_argument('-vfc_number',help='The beginning VFC number. The default is 1.', required=False,default=1)
parser.add_argument('-fex_aa',help='''Specify this flag if creating host vPCs on FEXs that are dual-homed (aka. Active/Active). 
When specified, configuration of a vpc number on the port-channel is suppressed. See the section on Enhanced vPC
in the configuration guide for more information.''', required=False,action="store_true", default=False )
parser.add_argument('-filename',help='Specify a filename to store the output.', required=False,default='' )

args = parser.parse_args()

desc = args.desc 
desc_counter = int(args.desc_count) 
mod_begin = int(args.module) 
mod_ports = int(args.module_ports) 
pc_number = int(args.pc_number)
pc_links = int(args.pc_links) 
port_begin = int(args.port_begin) 
port_total = int(args.ports) 
port_mode = args.mode
port_vlans = args.vlans
fex_hifs = args.fex
fex_number = int(args.fex_number)
breakout = args.breakout
breakout_type = args.breakout_type.upper()
vpc = args.vpc
vfc = args.vfc
vfc_number = int(args.vfc_number)
fex_aa = args.fex_aa
output_file = args.filename
 
## show values ##
print ("*****************************************************")
print ("Beginning module number: %s" % str(mod_begin) )
print ("Number of ports on module: %s" % str(mod_ports) )
print ("Total number of ports to configure: %s" % str(port_total) )
print ("Beginning port is %s" % str(port_begin) )
print ("Description is: %s" % desc )
print ("Description counter starts at: %s" % str(desc_counter) )
print ("Switchport mode is: %s" % port_mode )
print ("VLAN list is: %s" % port_vlans )
print ("Configure vPC: %s" % vpc )
print ("Number of port-channel links: %s" % str(pc_links) )
print ("Beginning vPC number: %s" % str(pc_number) )
print ("Using breakout: %s" % breakout )
print ("Breakout Type: %s" % breakout_type )
print ("Configuring FEX HIFs: %s" % fex_hifs )
print ("Beginning FEX number: %s" % str(fex_number) )
print ("Virtual Fiber Channel (VFC) creation: %s" % vfc )
print ("Beginning VFC number: %s" % vfc_number )
print ("Dual-homed FEX (Active/Active): %s" % fex_aa )
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

# Functions used within the main program

def CreatePC(pc_links,pc_number,vfc):
	if vfc and pc_links > 1 :
		print ('VFC creation is True and the number of port-channel links is > 1.')
		print ('This is an unsupported configuration. Please reduce the port-channel')
		print ('links to 1 or disable VFC creation.  Program will now exit.')
		exit()
	output_list.append('interface Port-channel' + str(pc_number))

def CreateDesc(desc,desc_counter):
	if desc != '' :
		output_list.append (' description ' + desc + str(desc_counter))

def PortMode(port_mode,port_vlans):
	if port_mode.lower() == 'trunk' :
		output_list.append (' switchport mode trunk')
		output_list.append (' spanning-tree port type edge trunk')
		if port_vlans != '' :
			output_list.append (' switchport trunk allowed vlan ' + port_vlans)
		
	if port_mode.lower() == 'access' :
		output_list.append (' switchport mode access')
		output_list.append (' spanning-tree port type edge')
		if port_vlans != '' :
			output_list.append (' switchport access vlan ' + port_vlans)
	
def CreateVFC(vfc_number,mod_begin,breakout_counter,port_number):
	output_list.append ('interface vfc' + str(vfc_number))
	if breakout:
		output_list.append (' bind interface Ethernet' + str(mod_begin) + '/' + str(port_number) + '/' + str(breakout_counter))
	if not breakout and not fex_hifs:
		output_list.append (' bind interface Ethernet' + str(mod_begin) + '/' + str(port_number))
	if not breakout and fex_hifs:
		output_list.append (' bind interface Ethernet' + str(fex_number) + '/' + '1/' + str(port_number))
	output_list.append (' no shut')
	output_list.append ('')
	

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

port_number = port_begin	
breakout_counter = 0
port_counter = 0

while port_counter < port_total:

# Doing 40G to 4x10G breakout and vPC
	if breakout and vpc:
		output_list = []
		CreatePC(pc_links,pc_number,vfc)
		CreateDesc(desc,desc_counter)
		PortMode(port_mode,port_vlans)
		output_list.append (' vpc ' + str(pc_number))
		output_list.append (' no shut')
		output_list.append ('')
	
		for y in range (1,pc_links+1):
			if port_number > mod_ports :
				mod_begin = mod_begin + 1
				port_number = 1
			if breakout_type == '40G' and breakout_counter == 4 :
				port_number = port_number + 1
				if port_number > mod_ports :
					mod_begin = mod_begin + 1
					port_number = 1
				breakout_counter = 1
			elif breakout_type == '100G' and breakout_counter == 10 :
				port_number = port_number + 1
				if port_number > mod_ports :
					mod_begin = mod_begin + 1
					port_number = 1
				breakout_counter = 1
			else :
				breakout_counter = breakout_counter + 1
			if port_counter < port_total :	
				output_list.append ('interface Ethernet' + str(mod_begin) + '/' + str(port_number) + '/' + str(breakout_counter))
				CreateDesc(desc,desc_counter)
				output_list.append (' channel-group ' + str(pc_number) + ' force mode active')
				output_list.append (' no shut')
				output_list.append ('')
				if vfc :
					CreateVFC(vfc_number,mod_begin,breakout_counter,port_number)
					vfc_number += 1	
			port_counter = port_counter + 1
			if y == pc_links :
				pc_number = pc_number + 1
				desc_counter = desc_counter + 1

		CreateOutput(output_list)		
					
	# Doing 40G to 4x10G breakout,  no vPC
	if breakout and not vpc:
		output_list = []
		if breakout_type == '40G' :
			breakout_ports = 5
		if breakout_type == '100G' :
			breakout_ports = 11

		for y in range (1,breakout_ports):
			if port_number > mod_ports :
				mod_begin = mod_begin +1
				port_number = 1
			if breakout_type == '40G' and breakout_counter == 4 :
				port_number = port_number + 1
				if port_number > mod_ports :
					mod_begin = mod_begin + 1
					port_number = 1
				breakout_counter = 1
			elif breakout_type == '100G' and breakout_counter == 10 :
				port_number = port_number + 1
				if port_number > mod_ports :
					mod_begin = mod_begin + 1
					port_number = 1
				breakout_counter = 1
			else :
				breakout_counter = breakout_counter + 1
			
			if port_counter < port_total :
				output_list.append ('interface Ethernet' + str(mod_begin) + '/' + str(port_number) + '/' + str(breakout_counter))
				CreateDesc(desc,desc_counter)
				PortMode(port_mode,port_vlans)
				output_list.append (' no shut')
				output_list.append ('')
				if vfc :
					CreateVFC(vfc_number,mod_begin,breakout_counter,port_number)
					vfc_number += 1
				
			desc_counter = desc_counter + 1
			port_counter = port_counter + 1

		CreateOutput(output_list)
										
	# No 4x10G breakout, doing vPC
	if vpc and not breakout:
		output_list = []
		CreatePC(pc_links,pc_number,vfc)
		CreateDesc(desc,desc_counter)
		PortMode(port_mode,port_vlans)
		if not fex_aa :
			output_list.append (' vpc ' + str(pc_number))
		output_list.append (' no shut')
		output_list.append ('')
			
		for z in range (1,pc_links+1) :
			if port_number > mod_ports :
				mod_begin = mod_begin + 1
				fex_number = fex_number + 1
				port_number = 1
			if port_counter < port_total :
				if fex_hifs :
					output_list.append ('interface Ethernet' + str(fex_number) + '/' + '1/' + str(port_number))
				else:
					output_list.append ('interface Ethernet' + str(mod_begin) + '/' + str(port_number))
				CreateDesc(desc,desc_counter)
				output_list.append (' channel-group ' + str(pc_number) + ' force mode active')
				output_list.append (' no shut')
				output_list.append ('')
				if vfc :
					CreateVFC(vfc_number,mod_begin,breakout_counter,port_number)
					vfc_number += 1
			if z == pc_links :
				pc_number = pc_number + 1
				desc_counter = desc_counter + 1

			port_number = port_number + 1
			port_counter = port_counter + 1

		CreateOutput(output_list)
				
	# No 4x10G breakout and no vPC
	if not breakout and not vpc:
		output_list = []
		if port_number > mod_ports :
			mod_begin = mod_begin + 1
			fex_number = fex_number + 1
			port_number = 1
		
		if fex_hifs :
			output_list.append ('interface Ethernet' + str(fex_number) + '/' + '1/' + str(port_number))
		else:
			output_list.append ('interface Ethernet' + str(mod_begin) + '/' + str(port_number))

		CreateDesc(desc,desc_counter)
		PortMode(port_mode,port_vlans)
		
		output_list.append (' no shut')
		output_list.append ('')
		if vfc :
			CreateVFC(vfc_number,mod_begin,breakout_counter,port_number)
			vfc_number += 1
		
		port_number = port_number + 1
		desc_counter = desc_counter + 1
		port_counter = port_counter + 1

		CreateOutput(output_list)
	
if output_file != '' :
	f.close()

				