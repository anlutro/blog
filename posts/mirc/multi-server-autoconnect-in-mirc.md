# Multi-server autoconnect in mIRC
pubdate: 2012-06-25 12:00:00 +0100
tags: mIRC
public: false

Press alt+r and enter the following:

    on *:START:{
      nick mynick
      anick mynick`
      emailaddr me@example.com
      fullname My Name
      server QuakeNet
      server -m Freenode
    }
    on *:CONNECT:{
      if ($network == OneNetwork) {
        MSG Q@CServe.quakenet.org AUTH mynick password
        MODE $me +x
      }
      elseif ($network == Freenode) {
        nick othernick
        anick othernick`
      }
    }