# Multi-server autoconnect in mIRC
pubdate: 2012-06-25 12:00:00

Press alt+r and enter the following:

    on *:START:{
      nick Raziel2p
      anick Raziel2p`
      emailaddr andreas@lutro.priv.no
      fullname Andreas
      server QuakeNet
      server -m irc.dal.net
      server -m EsperNet
    }
    on *:CONNECT:{
      if ($network == QuakeNet) {
        MSG Q@CServe.quakenet.org AUTH Raziel2p password
        MODE $me +x
      }
      elseif ($network == DalNET) {
        nick Raziel
        anick Raziel`
      }
    }