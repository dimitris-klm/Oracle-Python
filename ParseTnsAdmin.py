import json
import re
import os


class Connection:

    def __init__(self, path=None):
        """
        If the user chooses a different tns_admin.ora file than the one found in TNS_ADMIN environment variable then,
        the class should be instantiated with the path parameter.
        """

        if path is None:
            try:
                self.tns_admin_loc = os.environ.get("TNS_ADMIN") + "\\tnsnames.ora"
            except Exception:
                raise Exception("Cannot find TNS_ADMIN as system variable")
        else:
            self.tns_admin_loc = path
        return

    def get_connections(self):
        """
        This method returns all the connections that are found in the "tnsnames.ora"
        return: All the connections as a json type object
        """

        path_tns_admin = self.tns_admin_loc

        tns_file = ""
        list_of_params = ["HOST", "SID", "SERVICE_NAME", "PORT"]
        all_databases = {}

        try:
            tnsnames = open(path_tns_admin, "r")
        except IOError as err:
            raise IOError("Cannot find tnsnames.ora in TNS_ADMIN location")
        else:
            for row in tnsnames:
                tns_file += row

        parsed_text = re.sub(r"#[^\n]*\n", "\n", tns_file)  # remove comments
        parsed_text = re.sub(r"( *\n *)+", "\n", parsed_text.strip())  # remove excess blank lines

        databases = []
        start = 0
        buffer = 0
        
        while buffer < len(parsed_text):
            num_of_parenthesis = 0
            buffer = parsed_text.find("(")  # find first parenthesis
            while buffer < len(parsed_text):
                if parsed_text[buffer] == "(":
                    num_of_parenthesis += 1
                elif parsed_text[buffer] == ")":
                    num_of_parenthesis -= 1
                buffer += 1
                if num_of_parenthesis == 0:  # if the variable is equal to 0, all parenthesis were found
                    break

            databases.append(parsed_text[start:buffer].strip())
            parsed_text = parsed_text[buffer:]
            buffer = 0  # Reset buffer for next tns entry

        for item in databases:
            clean_text = item.replace(" ", "").replace("\n", "")
            try:
                database_name = re.match(r"(\w+.\w+)?=", clean_text).group().strip("=")
            except Exception as err:
                print(err)
                return
                
            connection_string = clean_text.replace(database_name, "").strip("=")
            conn_details = {}
            for param in list_of_params:
                try:
                    conn_details[param] = re.search(rf"{param}=(.*?)\)", connection_string, re.IGNORECASE).group(1)
                except AttributeError:
                    conn_details[param] = None

            conn_details["DSN"] = connection_string
            all_databases[database_name] = conn_details
            
        json_object_db = json.dumps(all_databases, indent=4)

        return json_object_db

    def get_conn_details(self, conn_name=None):
        """
        This method returns the connection details of a specific connection name that is passed as a parameter
        return: The connection details as dict
        """

        if conn_name is None:
            raise TypeError
        else:
            try:
                conn = json.loads(self.get_connections())[conn_name]
            except KeyError:
                return None

        return conn

    def get_host(self, conn_name=None):
        """
        This method returns the host name of a specific connection name that is passed as a parameter
        return: The host name or IP as string
        """
        
        if conn_name is None:
            raise TypeError
        else:
            try:
                conn = json.loads(self.get_connections())[conn_name]
            except KeyError:
                return None
        
        return conn["HOST"]
    
    def get_port(self, conn_name=None):
        """
        This method returns the port number of a specific connection name that is passed as a parameter
        return: The port number as string
        """
        
        if conn_name is None:
            raise TypeError
        else:
            try:
                conn = json.loads(self.get_connections())[conn_name]
            except KeyError:
                return None
        
        return conn["PORT"]

    def get_sid(self, conn_name=None):
        """
        This method returns the sid of a specific connection name that is passed as a parameter
        return: The SID as string
        """
        
        if conn_name is None:
            raise TypeError
        else:
            try:
                conn = json.loads(self.get_connections())[conn_name]
            except KeyError:
                return None
        
        return conn["SID"]

    def get_service_name(self, conn_name=None):
        """
        This method returns the service name of a specific connection name that is passed as a parameter
        return: The Service Name as string
        """
        
        if conn_name is None:
            raise TypeError
        else:
            try:
                conn = json.loads(self.get_connections())[conn_name]
            except KeyError:
                return None
        
        return conn["SERVICE_NAME"]

    def get_dsn(self, conn_name=None):
        """
        This method returns the full DSN connection string of a specific connection name that is passed as a parameter
        return: The DSN connection as string
        """

        if conn_name is None:
            raise TypeError("The connection name is a mandatory argument")
        else:
            try:
                conn = json.loads(self.get_connections())[conn_name]
            except KeyError:
                return None

        return conn["DSN"]
