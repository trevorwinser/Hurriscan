## First
Make sure you have the requirements.txt file downloaded, use this command in the VS Code terminal if it is not downloaded yet: pip install -r requirements.txt (use pip3 if you have python3 downloaded on your device)

## To launch the server
use this command in the VS Code terminal: python main.py (use python3 if you have python3 downloaded on your device)

## Open up a different terminal:

In order to add a user to the database in order to test functionality, use this command in your new terminal: 

macOS: curl -X POST -H "Content-Type: application/json" -d '{"username": "johnyn", "password": "133456", "email": "j@g.c"}' http://localhost:7070/admin/users

Windows: curl -i -X POST -H "Content-Type: application/json" -d "{"username": "johnyn", "password": "133456", "email": "j@g.c"}" http://localhost:7070/admin/users

## Now, launch admin-dashboard.html.

Edit the user using the username and password used in the previous curl command.

To test whether a user has been edited, run this command in your terminal: curl -X get http://localhost:7070/admin/users

	This should return a list with your user's updated information that was provided on the admin-dashboard.html webpage

Delete the user using the username that is now stored in the database, if you edited the user, make sure you use the new username.

To test whether a user has been deleted, run this command in your terminal: curl -X get http://localhost:7070/admin/users

    If you currently do not have any users stored in the database, your terminal should return: {"users":[]}