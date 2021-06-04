from mininet.node import Node
from mininet.log import info

class HostOnly( Node ): 

	def __init__( self, name, localIntf=Hone, flush=False, inNamespace=False, **params): 
	
		super( HostOnly, self ).__init__( name, inNamespace, **params )
		self.locallntf = locallntf 
		self.flush = flush 
	
	def setManualConfig( self, intf ):

	        cfile = '/etc/network/interfaces'
        	line = '\niface %s inet manual\n' % intf
	        try:
	            with open( cfile ) as f:
        	        config = f.read()
	        except IOError:
	            config = ''
	        if ( line ) not in config:
	            info( '*** Adding "' + line.strip() + '" to ' + cfile + '\n' )
	            with open( cfile, 'a' ) as f:
	                f.write( line )
	            self.cmd( 'service network-manager restart || netplan apply' )

    def config( self, **params ):

        if not self.localIntf:
            self.localIntf = self.defaultIntf()

        self.setManualConfig( self.localIntf )

        super( HostOnly, self).config( **params )

hosts = { 'hostonly' : HostOnly }