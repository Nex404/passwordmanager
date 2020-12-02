# A passwordmanager for private usage

## Disclamer
This passwordmanager is just a smal project by me. I tried to make this save, but you can have a more secure password manager out there.   

## Project Details
I used the hasher lib for hashing password. The master passwords are not saved in clear text.   
The account credentials are stored in an extra file. This file has 3 variables each line.   
The variables are the username, the hashed password and the salt. The file is written in byte mode because the salt is alwayse in byte format.   
   
For every user there is a db for his/her accounts. These .db files are always decrypted.   
When the files need to be used, they gonna be encrypted, red from and decrypted again.   
Normaly no one can clone the decrypted file in the time the pc is processing it.   
   
I also created a small UI or better menu, so everyone can interact with the pw manager.   

## Requirements
hashlib   
sqlite3   
cryptography   
   
All other libs should be preinstalled.   

Installation:
```
pip3 install -r "requirements.txt"
```