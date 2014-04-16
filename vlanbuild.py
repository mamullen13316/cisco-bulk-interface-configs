# This script will create bulk vlan configuration for switches running NX-OS

# vlan_id = The vlan number
# vlan_name = The name as well as the description used on SVIs
# fp_vlan = A boolean which indicates whether a vlan is a fabricpath vlan
# ip_address = The ip address which will be placed on the SVI
# routing_protocol = can be either OSPF, EIGRP, or blank
# ospf_area = The OSPF area number
# hsrp_ip = The HSRP IP address
# hsrp_version = 1 or 2
# mtu = interface mtu, leave blank for default
# file_name = the file that is looped through to obtain vlanid, name, and IP addressing
# fabricpath = boolean value which indicates whether a vlan is mode fabricpath
# switch_number = Set to 1 if this is the first switch,  2 if the second switch, and etc..
#                 Influences the IP address placed on the interface.  Default = 1.  

switch_number = 1
hsrp_version = 2
file_name = 'vlans.csv'
routing_protocol = 'EIGRP'
ospf_area = 0
mtu = 9216
fabricpath = 'TRUE'

# Create the command line arguments using the argparse module
 
import argparse
 
parser = argparse.ArgumentParser(description='''vlanbuild.py -- Version 1.0 --
This script will create bulk vlan and SVI configuration for switches running NX-OS.
Please send any errors/comments/suggestions to mamullen@cisco.com.''')
parser.add_argument('-switch',help='''A number indicating whether this is the 1st, 2nd, 3rd, etc. switch you are
 creating the configs for. It determines what the IP address will be on each SVI.  Ex.  If the IP subnet is 192.168.1.0/24
 and switch=1,  the IP assigned to the SVI will be 192.168.1.2/24.  If switch=2, the IP assigned to the SVI will be
 192.168.1.3/24.  The default is 1.''',required=False, default=1)
parser.add_argument('-inputfile',help='''The name of the file containing the VLAN and IP information.  The file must be a .CSV using the format: 
vlan ID, vlan name, IP subnet/mask.    
Example .CSV format:

100, Applications, 192.168.1.0/24

The default filename is vlans.csv and it must be in the same directory as this script.

''', required=False, default='vlans.csv')
parser.add_argument('-protocol',help='The routing protocol in use. Valid values are EIGRP or OSPF.  The default is None.',required=False, default='') 
parser.add_argument('-area',help='The OSPF area in use.  Only used if -protocol OSPF is specified.  The default is 0.', required=False, default=0 )
parser.add_argument('-mtu',help='The MTU to configure on SVIs. Leave off if keeping the default of 1500.', required=False, default='' )
parser.add_argument('-hsrp_version',help='The HSRP version to use. The default is 2.', required=False, default=2 )
parser.add_argument('-fabricpath', help='Set this flag to configure vlans as Fabricpath VLANs.',required=False, action="store_true", default=False ) 
parser.add_argument('-no_svi', help='Set this flag if you want to create VLANs but no SVIs',action="store_true",default=False )
parser.add_argument('-pim', help='Set this flag if you want to configure PIM sparse mode on the SVIs.',required=False, action="store_true",default=False )
parser.add_argument('-dhcp_relay', help='Configure helper addresses, separated by comma.', required=False, default='' )
parser.add_argument('-vlan_range',help='Set this flag to build an interface range command for the VLANs in the .CSV.  All other flags are ignored.', required=False,action="store_true",default=False )
parser.add_argument('-outputfile',help='Specify a filename to store the output.',required=False, default="" )

args = parser.parse_args()
switch_number = int(args.switch)
file_name = args.inputfile
routing_protocol = args.protocol
ospf_area = args.area
mtu = args.mtu
fabricpath = args.fabricpath
no_svi = args.no_svi
hsrp_version = args.hsrp_version
pim = args.pim
dhcp_relay = args.dhcp_relay
vlan_range = args.vlan_range
output_file = args.outputfile



## show values ##
print ("*****************************************************")
print ("Switch number: %s" % str(switch_number) )
print ("Input file name is: %s" % file_name )
print ("Routing protocol is %s" % routing_protocol )
print ("OSPF Area is: %s" % ospf_area )
print ("HSRP Version is: %s" % hsrp_version )
print ("MTU is: %s" % mtu )
print ("Configure VLANs for Fabricpath: %s" % fabricpath )
print ("Only configure VLANs: %s" % no_svi )
print ("Configure PIM Sparse Mode %s" % pim )
if dhcp_relay != "" :
	dhcp_list = list(dhcp_relay.split(','))
	for dhcp_server in dhcp_list :
		print ("DHCP Relay Address: %s" % dhcp_server  )
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


# This section creates an interface range command for all the vlans in the .CSV
# It is only executed when the command line argument -vlan_range is specified.

if vlan_range :
	output_list = []
	line_number=0
	with open(file_name) as a_file :
		for a_line in a_file :
			vlan,desc,ip = a_line.split(',')
			line_number += 1
			if line_number == 1 :
				int_range = 'interface vlan' + str(vlan)
			else :
				int_range = int_range + ',vlan' + str(vlan)
	output_list.append ('')
	output_list.append (int_range)
	ouput_list.append ('')
	CreateOutput(output_list)
	exit()



# First loop through each line in the file and generate the vlans
with open (file_name) as a_file:
	output_list = []
	for a_line in a_file:
		vlan_id, vlan_desc, ip_subnet = a_line.split(',')
		vlan_name = vlan_desc.replace(' ','_')
		vlan_name = vlan_name.replace('-_','')
				
		output_list.append ('vlan ' + vlan_id)
		output_list.append (' name ' + vlan_name)
		if fabricpath :
			output_list.append (' mode fabricpath')		
		output_list.append ('')
	CreateOutput(output_list)
# Stop if the user has specified the no_svi flag		
if no_svi :
	exit ()
		
# Loop through each line in the file and generate the SVIs
with open (file_name) as a_file:
	output_list = []
	for a_line in a_file:
		vlan_id, vlan_desc, ip_subnet = a_line.split(',')
		octet1, octet2, octet3, octet4 = ip_subnet.split('.')
		octet4,subnet_mask = octet4.split('/')
		hsrp_octet4 = int(octet4) + 1
		octet4 = int(octet4) + 1 + switch_number
		ip_address = octet1 + '.' + octet2 + '.' + octet3 + '.' + str(octet4) + '/' + subnet_mask.rstrip()	
		hsrp_ip = octet1 + '.' + octet2 + '.' + octet3 + '.' + str(hsrp_octet4)
			
		output_list.append ('interface vlan' + vlan_id)
		output_list.append (' description ' + vlan_desc)
		output_list.append (' ip address ' + ip_address)
		if dhcp_relay != "" :
			for dhcp_server in dhcp_list :
				output_list.append (" ip dhcp relay address " + dhcp_server)
		if routing_protocol.lower() == 'ospf' :
			output_list.append (' ip router ospf 1 area ' + str(ospf_area))
			output_list.append (' ip ospf passive-interface')
		if routing_protocol.lower() == 'eigrp' :
			output_list.append (' ip router eigrp 1')
			output_list.append (' ip eigrp passive-interface')
		if pim :
			output_list.append (' ip pim sparse-mode')
		if hsrp_version == 2 :
			output_list.append (' hsrp version 2')
		output_list.append (' hsrp ' + vlan_id)
		output_list.append ('  ip ' + hsrp_ip)
		if switch_number == 1 :
			output_list.append ('  priority 110')
			output_list.append ('  preempt')
		if mtu != '' :
			output_list.append (' mtu ' + str(mtu)) 	
		output_list.append (' no shut')
		output_list.append ('')
	CreateOutput(output_list)
		
if output_file != '' :
	f.close()		
		
		
		
 