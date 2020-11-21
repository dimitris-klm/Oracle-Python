# Oracle-Python

#### A script that parses the tnsnames.ora file and returns all the useful information a user might need to connect to an Oracle db. The script is basically a class which when instantiated looks for TNS_ADMIN environment variable in the system. If the variable exists it looks for the tnsnames.ora file and parses it.

#### There are several methods in the class that can return, depending on the needs, specific information regarding the connections.
* get_connections()
* get_conn_details()
* get_host()
* get_port()
* get_sid()
* get_service_name()
* get_dsn()

#### Note that if the TNS_ADMIN environment variable is not set or the user wnats to use a different file then there is the option of passing the path of the .ora file when instantiating the class.
