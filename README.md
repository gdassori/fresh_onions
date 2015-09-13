# Fresh onions

Grab fresh onions from pastebin.

A .onion links lurker script.

More proxies == More happyness!


                           /~
                     \  \ /**
                      \ ////
                      // //
                     // //
                   ///&//
                  / & /\ \
                /  & .,,  \
              /& %  :       \
            /&  %   :  ;     `\
           /&' &..%   !..    `.\
          /&' : &''" !  ``. : `.\
         /#' % :  "" * .   : : `.\
        I# :& :  !"  *  `.  : ::  I
        I &% : : !%.` '. . : : :  I
        I && :%: .&.   . . : :  : I
        I %&&&%%: WW. .%. : :     I
         \&&&##%%%`W! & '  :   ,'/
          \##f$oc#%% W &..'  #,'/
            \W&&##%%&&&&### %./
              \###j[\##//##}/
                 ++///~~\//_
                  \\ \ \ \  \_
                  /  /    \


### Dependencies

- setuptools 5.5.1
- python 3.4
- virtualenv
- libxml2, libxslt: http://stackoverflow.com/questions/5178416/pip-install-lxml-error
- lxml 3.4.4
- requests 2.7.0
- BeautifulSoup 4.4.0

### Setup

```sh
$ git clone https://github.com/gdassori/fresh_onions.git
$ cd fresh_onions
$ virtualenv -p python3.4 venv
$ venv/bin/pip install -r  requirements.txt
```

### Usage

```sh
$ venv/bin/python fresh_onion.py &
$ tail -f onion.log

2015-09-13 14:52:37 - onion - INFO - Starting pastebin monitoring for onion links
2015-09-13 14:52:37 - onion - INFO - Downloading proxies...
2015-09-13 14:52:38 - onion - INFO - New 202 proxies saved, total of 202 proxies listed
2015-09-13 14:53:16 - onion - INFO - Pastebin archive scraped 1 time, total 28 pastes parsed
2015-09-13 14:54:36 - onion - INFO - Pastebin archive scraped 2 times, total 40 pastes parsed
2015-09-13 14:55:06 - onion - ERROR - proxy | unavailable
2015-09-13 14:55:53 - onion - INFO - Onion link found on paste gvfV5kwg | http://3g2upl4pq6kufc4m.onion/
2015-09-13 14:55:53 - onion - INFO - Onion link found on paste gvfV5kwg | http://xmh57jrzrnw6insl.onion/
...
```