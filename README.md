# kings-landing
Our software engineering project :/
 
 
We are officially in Beta!

TODO
 
 * Do a shit ton of testing

NOTE
 * `view_boarding_pass.py` is depracated. Use `valar_morghulis.py` instead.

Usage

 * Download the repo.
 * Move the `images` folder into the `static` folder
 * Setup for Terminal Software: `python valar_morghulis.py <terminal> <gate>`
 * `terminal` and `gate` are necessary command line arguments corresponding to the location where the system is deployed.
 * Setup for main website: `python all_men_must_serve.py <master_ip> <fake>`, on another system.
 * `master_ip` and `fake` are necessary command line arguments
 * `master_ip` should be the IP address of the system where the terminal software `valar_morghulis.py` is served.
   Though you can probaby get away with some garbage value if it is strictly for testing.
 * `fake` should be 1 if you plan to fake the OTP else 0
 * The public facing website will be served at the static IP of the server at port 5000
 
 Requirements
 
  * Python2
  * Flask
  * SQLite3
  * requests
  * pyqrcode
  * pypng
   
  
