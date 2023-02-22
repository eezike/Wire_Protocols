# Wire Protocol & RPCs

Emeka Ezike & Victor Goncalves

[Engineering Notebook](https://docs.google.com/document/d/1MT0ylai_91mFQ5CmxLvrGMrPvLOp5NmYkVy64lfWpCk/edit?usp=sharing)

**Getting Started:**

 1. Clone the repository [here](https://github.com/eezike/Wire_Protocols)
 2. Note, there are two folders in the repo: ordinary deals with the wire protocol code and grpc deals with gRPC
 3. Ensure that the most recent version of Python is downloaded [here](https://www.python.org/downloads/)
 4. Ensure that gRPC is downloaded for Python using the following commands
	 5. pip install grpcio
	 6. pip install grpcio-tools
 5. We use Tkinter for the GUI, so download it with the following command:
	 6. pip install tk
 6. **Lastly, we use port 50051 as default in each server file**
	 

**Part 1: Wire Protocol**
Steps:
 1. cd ordinary
 2. For the server run: python ./server.py
	 3. Should print the server IP and port no. Keep track of these
 3. For each client run: python ./app.py
	 4. Connect to the IP and port as listed above
	 5. Register for an account or log in w/a username and password
	 6. Once logged in, select the user you are trying to send a message to via dropdown, type the message, then hit send
	 7. If desired, delete the account when finished. 
	 8. Note: have at least two clients running in two separate terminals

**Part 2: gRPC**
Similar steps as above:
 1. cd grpc
 2. For the server run: python ./server.py
	 3. Should print the server IP and port no. Keep track of these.
 3. For each client run: python ./app.py
	 4. Connect to the IP and port as listed above
	 5. Register for an account or log in w/a username and password
	 6. Once logged in, select the user you are trying to send a message to via dropdown, type the message, then hit send
	 7. If the account has been created, but is not visible in the dropdown menu, click "reset options" to update the dropdown.
	 8. If desired, delete the account when finished. 
	 9. Note: have at least two clients running in two separate terminals
 4. For running unit tests, just run python ./unit_tests.py 
	 5. Note: don't run this for the demo as we reset the database to account for testing.
