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
 
 
###Add the reloaded script to the page

The reloaded server communicates with your browser using websockets.
Add the following script to the page to enable them:

 ```html
  <script src="http://localhost:9000/reloaded/reloaded.js" id="reloaded-script">
  
 ```
 
###Use the special data tag to specify which files reloaded should monitor
 
 After reloaded.js has been loaded it will go through the page's DOM and
 look for elements with this data tag:
 
 	data-reloaded-path='/path/to/file'
 
 For reloaded's file monitor to work you need to specify the full, absolute
 path to the file here.
  
 ```html
 <!-- Example 1: -->
 <link href="/css/style.css" rel="stylesheet" data-reloaded-path="/path/to/file" />
 
 <!-- Example 2: The html page itself: -->
 <html data-reloaded-path="/abs/path/to/example.html">

```

###Running the reloaded server

```bash
$ ./reloaded.py 
```

Run:

```bash
$ ./reloaded.py --help
```

for more configuration options
