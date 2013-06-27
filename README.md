#Reloaded

 Reloaded provides browser and editor independent live reloads.
 
 

##Installation
 After cloning this repository cd to its root and:
 
 ```bash
 $ ./install.sh
 ```
 
 This will download and install the required modules locally. This ensures
 reloaded will work both inside and outside virtualenvs.
 
##Usage
 
 
 Setting Reloaded up is very simple. Add the reloaded script to the page
 you are working on and use the reloaded data tag to specify which files
 Reloaded should monitor. When one of those files is modified Reloaded will
 reload the file (when it is a css file) or reload the page.
 
 
###Adding the reloader script to the page

The reloader server communicates with your browser using websockets.
Add the following script to the page to enable them:

 ```html
  <script src="http://localhost:9000/reloader/reloader.js" id="reloader-script" />
  
 ```
 
 ###Use the special data tag to specify which files Reloader should monitor
 
 After reloader.js has been loaded it will go through the page's DOM and
 look for elements with this data tag:
 
 	data-reloader-path='/path/to/file'

Reloaded won't work if it cannot find the file so make sure you only use absolute paths.
  
 ```html
 <!-- Example 1: -->
 <link href="/css/style.css" rel="stylesheet" data-reloader-path="/path/to/file" />
 
 <!-- Example 2: The html page itself: -->
 <html data-reloader-path="/abs/path/to/example.html">

```

###Running the reloader server

```bash
$ ./reloader.py 
```

Run:

```bash
$ ./reloader.py --help
```

for more configuration options


###Plugin support

As a proof of concept I wrote a very simple vim plugin. Look here
for more information: [vim-reloader](https://github.com/dbsr/vim-reloader)
