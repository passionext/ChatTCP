Version 1.0 update:
  - Added Cryptography to the code. Now it is mandatory to first generate the pair of keys for the communication through the generate_key.py. After that, the keys are stored in the main directory and the code will automatically find them by their default name,
  - Now it is possible to re-enter the username in case of any typo error,
  - The majority of code has been convertend into Python Class,

Known Issues:
- Limited number of sending and receving characters due to RSA Encryption with 2048 bits key,
- For now, there is no possibility to send file due to Thread usage,
- A bette way to handle error should be implemented.
- A way to subscribe to the server should be implemented. For now, it is possible to add user only manually.

Libraries used:
- csv
- rsa
- socket
- threading
