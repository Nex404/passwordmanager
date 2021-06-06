# A passwordmanager for private usage

## Disclamer
This passwordmanager is just a small project by me. I tried to make this save, but you can have a more secure password manager out there.   

## Project Details
I used the hasher lib for hashing password. The master passwords are not saved in clear text.   
The account credentials are stored in a db file. This db file has 3 variables each line.   
The variables are username, hashed password and salt.    
   
For every user there is a db for his/her accounts. These .db files are always encrypted.   
When the files need to be used, they gonna be decrypted, red from and encrypted again.   
Normaly no one can clone the decrypted file in the time the pc is processing it.   
   
I created a GUI. In the final folder is the finalized project.

## Requirements
hashlib   
sqlite3   
cryptography   
   
All other libs should be preinstalled.   

Installation:
```
pip3 install -r "requirements.txt"
```