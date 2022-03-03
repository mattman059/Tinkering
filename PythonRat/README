    ____        ____  ___  ______
   / __ \__  __/ __ \/   |/_  __/
  / /_/ / / / / /_/ / /| | / /   
 / ____/ /_/ / _, _/ ___ |/ /    
/_/    \__, /_/ |_/_/  |_/_/     
      /____/                     

------ Table of Contents ------
1. Installation
1.1 Server Installation
1.1.1 Starting the Server
1.2 Client Installation
1.2.1 Starting the Client

2. Server Execution
2.1 Connecting to a Client
2.2 Killing a remote Client
2.3 Exiting the Server

3. Tasking
3.1 Tasking via Server connection
3.2 Tasking via stored tasking file

4. TODO
--------------------------------------


----- 1. INSTALLATION -----

1.1 --- SERVER INSTALLATION ---
 - Copy server.py and server_class.py to the desired location
 - Identify the desired interface to host the server
      - Ex: 192.168.0.100, 10.0.0.10, etc.
 - Identify the desired port number to host the server
      - Ex: 58955, 1337, 4444, etc.
 - Modify server.py to specify your chosen interface:
      - s = Server("YOUR IP",YOUR_PORT)
      - Ex: s = Server("10.0.0.10", 4444)
 - Save your modifications.

1.1.1 --- STARTING THE SERVER
 - Start the server with: python3 server.py
 - You should see something similar to the following:
       ____        ____  ___  ______
     / __ \__  __/ __ \/   |/_  __/
    / /_/ / / / / /_/ / /| | / /   
   / ____/ /_/ / _, _/ ___ |/ /    
  /_/    \__, /_/ |_/_/  |_/_/     
        /____/                    
                                   
 -- SERVER INFORMATION-- :
 [+] SERVER IP: YOUR IP
 [+] SERVER PORT: YOUR PORT
 [+] SERVER WEB PORT: 8000 (or your WEB PORT)
 -------------------------------------
 PyRat Options: 
 1. Connect to Shell
 2. Kill Remote Implant
 
 3. Exit Server
 
 Choose your option: 


1.2 --- CLIENT INSTALLATION ---
 - Modify client.py to indicate your listening Server IP address and port:
      - server_addr = 'SERVER_IP'
        server_port = SERVER_PORT
 - Modify client.py to indicate the client's IP address and desired communication port:
      - c = Client(CLIENT_IP,COMM_PORT,server_addr,server_port)
      - Ex: c = Client('10.0.0.45',54321,server_addr,server_port)
 - Save your modifications.
 - Copy client.py, client_class.py, and capabilities.py to the remote client to a 
   directory where you have write access.

1.2.1 --- STARTING THE CLIENT ---
 - Start the client with: python3 client.py
 - You should see something similar to the following:

  Checking for tasks in 2 minutes...
 
 - *Note: These messages will be visible on the remote host. You can take them out for a 
        "quieter" RAT


----- 2. SERVER EXECUTION -----

2.1 --- CONNECTING TO A CLIENT ---
 - Inside the Server menu, choose option '1'
 - Enter the Client IP address as prompted
 - Enter the Client Port as prompted
 - You should see the following:

   Choose your option: 1
   Enter the target address: 
   1.2.3.4
   Enter the target port: 
   12345
   Connecting to 1.2.3.4:12345
 
  - If you are successful, you should see something similar to the following:

    Enter your command (QUIT to exit shell): 

2.2 --- KILLING A REMOTE CLIENT ---
  * WARNING : Make sure you really want to kill the remote client *
 - Inside the Server menu, choose option '2'
 - Enter the Client IP address as prompted
 - Enter the Client PORT as prompted
 - You should see the following:

   KILL RECV'D. KILLING NOW

2.3 --- EXITING THE SERVER ---
 - Inside the Server menu, choose option '3'
 - When prompted, decide if you would like to kill the remote server
      - If you choose to, enter 'Y' and follow the prompts. The result
        will be similar to 2.2 above.
      - If you do not wish to kill the remote client, select 'N'.
        * Note, the remote client will still attempt to connect to the server
          if you do not kill it

----- 3. TASKING -----

3.1 --- TASKING VIA SERVER CONNECTION ---
 - Follow the steps included for step 2.1 (Connecting to a Client).
 - Once at the command prompt, enter the desired system command (or QUIT to exit)
   The "<--" indicates "Send to Client". The "-->" indicates "Received from Client".

   <-- id
   --> uid=1000(dev) gid=1000(dev) groups=1000(dev),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),120(lpadmin),131(lxd),132(sambashare)

   Enter your command: 
   <-- whoami
   --> dev

 - On the client side, the following message is presented:

   Received C2 : TASK

 - Once finished, type QUIT to exit the shell.

 3.2 --- TASKING VIA STORED TASKS ---
 - On the server side, create a file named "tasks.txt"
 - Put all commands you wish to be run on the next connect within that file.
 - When the Client connects back at it's configured interval, the tasking will be executed.
 - Once the tasking is complete, the Client will connect again, pushing the results into
   a file called "task-completed". It will look similar to the following, but with your
   commands:

   ---------- whoami;id;uname -a ----------
   dev
   uid=1000(dev) gid=1000(dev) groups=1000(dev),4(adm),24(cdrom),27(sudo),30(dip),46
   (plugdev),120(lpadmin),131(lxd),13


----- 4. TODO -----
- use argparse to set up command line arguments (server/client)
- use configuration files to set up clients     (client)
- ignore old tasking                            (client)
- client registration (basic)                   (server/client)
- client registration (advanced)                (server/client/web)
- option to reconfigure client                  (server/client)
- prevent client from talking to dead server    (client)
