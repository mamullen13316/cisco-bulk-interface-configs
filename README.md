These scripts will assist with creating bulk interface configurations for Cisco switches running NX-OS. Each is a separate script that can be run from the command line. This initial version has undergone minimal testing, please report any issues or send comments/suggestions to mamullen@cisco.com. 

1. interfacebuild.py - Creates interface configuration for a specified number of interfaces. 
2. fexbuild.py - Create FEX configuration for a specified number of FEXs. 
3. vlanbuild.py - Create VLANs and VLAN interfaces from a .CSV file containing the VLAN, VLAN naming, and IP addressing information. 

python3 interfacebuild.py
usage: interfacebuild.py [-h] -ports PORTS [-port_begin PORT_BEGIN]
                         [-module MODULE] [-module_ports MODULE_PORTS]
                         [-mode MODE] [-vlans VLANS] [-desc DESC]
                         [-desc_count DESC_COUNT] [-vpc] [-pc_links PC_LINKS]
                         [-pc_number PC_NUMBER] [-breakout]
                         [-breakout_type BREAKOUT_TYPE] [-fex]
                         [-fex_number FEX_NUMBER] [-vfc]
                         [-vfc_number VFC_NUMBER] [-fex_aa]
                         [-filename FILENAME]

python3 interface-build.py --help

interfacebuild.py -- Version 1.0 -- This script generates bulk interface
configuration for switches running NX-OS. Please send any
errors/comments/suggestions to mamullen@cisco.com.

optional arguments:

  -h, --help            show this help message and exit

  -ports PORTS          Total number of ports to be configured.

  -port_begin PORT_BEGIN
                        The port number to begin numbering. The default is 1.

  -module MODULE        The number of the module to start numbering. The
                        default is 1.

  -module_ports MODULE_PORTS
                        The number of ports on the module. The default is 48.

  -mode MODE            The switchport mode to be used. Valid values are
                        ACCESS or TRUNK

  -vlans VLANS          The vlan (access mode) or vlan list (trunk mode).
                        Default is no vlan list specified.

  -desc DESC            The description applied to each interface. If spaces
                        in the description, it must be enclosed in quotes.

  -desc_count DESC_COUNT
                        An incrementing number appended to the description
                        (ex. SERVER-1, SERVER-2...). This is the starting
                        value. The default value is 1

  -vpc                  Specify this flag to create port-channels and vPCs.

  -pc_links PC_LINKS    The number of links in a port-channel. The default is
                        2.

  -pc_number PC_NUMBER  The starting port-channel number.
  -breakout             Specify this flag to do 40G to 4x10G interface
                        breakout.

  -breakout_type BREAKOUT_TYPE
                        Specify 40G for 40G to 4x10G breakout, or 100G for
                        100G to 10x10G breakout.

  -fex                  Specify this flag to create FEX HIFs. Note that this
                        will not work with the breakout flag set.

  -fex_number FEX_NUMBER
                        Specify the starting FEX number. The default is 100.

  -vfc                  Specify this flag to create Virtual Fiber Channel
                        interfaces.

  -vfc_number VFC_NUMBER
                        The beginning VFC number. The default is 1.

  -fex_aa               Specify this flag if creating host vPCs on FEXs that
                        are dual-homed (aka. Active/Active). When specified,
                        configuration of a vpc number on the port-channel is
                        suppressed. See the section on Enhanced vPC in the
                        configuration guide for more information.

  -filename FILENAME    Specify a filename to store the output.


python3 fexbuild.py --help
usage: fexbuild.py [-h] [-module MODULE] [-port PORT] [-uplinks UPLINKS]
                   -fex_count FEX_COUNT [-module_ports MODULE_PORTS]
                   [-fex_number FEX_NUMBER] [-fex_increment FEX_INCREMENT]
                   [-breakout] [-fex_aa] [-fcoe] [-fcoe_even] [-fcoe_odd]
                   [-filename FILENAME]

fexbuild.py -- Version 1.0 -- This script will create FEXs and configure the
interfaces to be used for the fabric uplinks. Please send any
errors/comments/suggestions to mamullen@cisco.com.

optional arguments:

  -h, --help            show this help message and exit

  -module MODULE        The beginning module number to start creating fabric
                        links. The default is 1.

  -port PORT            The beginning port number to start creating fabric
                        links. The default is 1.

  -uplinks UPLINKS      The number of fabric uplinks to use for each FEX. The
                        default is 2.

  -fex_count FEX_COUNT  The number of FEXs you are creating. The default is 1.

  -module_ports MODULE_PORTS
                        The number of ports available on the module for
                        creating uplinks. The default is 48.

  -fex_number FEX_NUMBER
                        The beginning FEX number. The default is 100.

  -fex_increment FEX_INCREMENT
                        The number by which you want to increment the FEX
                        number. Useful for example if you want to put all the
                        odd FEXs on one side and even on the other. The
                        default is 1.

  -breakout             Specify this flag to do 40G to 4x10G interface
                        breakout.

  -fex_aa               Specify this flag if the FEXs will be dual homed to
                        two parent switches.

  -fcoe                 Specify this flag to configure fcoe on all FEXs.

  -fcoe_even            Specify this flag if you only want to configure fcoe
                        on the even numbered FEXs

  -fcoe_odd             Specify this flag if you only want to configure fcoe
                        on the odd numbered FEXs

  -filename FILENAME    Specify a filename to store the output.

python3 vlanbuild.py
usage: vlanbuild.py [-h] [-switch SWITCH] [-inputfile INPUTFILE]
                    [-protocol PROTOCOL] [-area AREA] [-mtu MTU]
                    [-hsrp_version HSRP_VERSION] [-fabricpath] [-no_svi]
                    [-pim] [-dhcp_relay DHCP_RELAY] [-vlan_range]
                    [-outputfile OUTPUTFILE]



optional arguments:

  -h, --help            show this help message and exit

  -switch SWITCH        A number indicating whether this is the 1st, 2nd, 3rd,
                        etc. switch you are creating the configs for. It
                        determines what the IP address will be on each SVI.
                        Ex. If the IP subnet is 192.168.1.0/24 and switch=1,
                        the IP assigned to the SVI will be 192.168.1.2/24. If
                        switch=2, the IP assigned to the SVI will be
                        192.168.1.3/24. The default is 1.

  -inputfile INPUTFILE  The name of the file containing the VLAN and IP
                        information. The file must be a .CSV using the format:
                        vlan ID, vlan name, IP subnet/mask. Example .CSV
                        format: 100, Applications, 192.168.1.0/24 The default
                        filename is vlans.csv and it must be in the same
                        directory as this script.

  -protocol PROTOCOL    The routing protocol in use. Valid values are EIGRP or
                        OSPF. The default is None.

  -area AREA            The OSPF area in use. Only used if -protocol OSPF is
                        specified. The default is 0.

  -mtu MTU              The MTU to configure on SVIs. Leave off if keeping the
                        default of 1500.

  -hsrp_version HSRP_VERSION
                        The HSRP version to use. The default is 2.

  -fabricpath           Set this flag to configure vlans as Fabricpath VLANs.

  -no_svi               Set this flag if you want to create VLANs but no SVIs

  -pim                  Set this flag if you want to configure PIM sparse mode
                        on the SVIs.

  -dhcp_relay DHCP_RELAY
                        Configure helper addresses, separated by comma.

  -vlan_range           Set this flag to build an interface range command for
                        the VLANs in the .CSV. All other flags are ignored.

  -outputfile OUTPUTFILE
                        Specify a filename to store the output.


