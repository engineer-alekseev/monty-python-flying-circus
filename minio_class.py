from minio import Minio
from dataclasses import dataclass
from configparser import ConfigParser
import logging

@dataclass
class Minio_client:
    filename:str = 'config.ini'
    def __post_init__(self)->None:
        """
        Initializes the Minio_client class.
        
        Reads the configuration file 'config.ini' to get the required 
        configuration values for the Minio client. Sets up logging with the 
        specified log file. Creates a Minio client with the configuration 
        values. Checks if the specified bucket exists and creates it if it 
        doesn't. Logs the initialization and bucket creation events.
        """
        # Read the configuration file
        cfg:ConfigParser = ConfigParser()
        cfg.read('config.ini')
        # Get the required configuration values
        server:str = cfg.get('minio','server')
        access_key:str = cfg.get('minio','access_key')
        secret_key:str = cfg.get('minio','secret_key')
        self.bucket:str = cfg.get('minio','bucket')
        log_file:str = cfg.get('minio','log_file')

        # logging initialize
        FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(format=FORMAT,
                            level=logging.INFO, 
                            filename=log_file,
                            filemode="w")
                      
        # Create a Minio client with the configuration values
        self.client:Minio = Minio(
            endpoint=server,
            access_key=access_key,
            secret_key=secret_key
        )
        logging.info("Class Minio_client initialized")  

        # Check if the bucket exists
        found:bool = self.client.bucket_exists(self.bucket)
        if not found: 
            # Create the bucket if it doesn't exist
            logging.info("Bucket not exists: %s", self.bucket)  
            self.client.make_bucket(self.bucket)
        else:
            logging.info("Bucket '%s' already exists",self.bucket)
        

    def object_exists(self, filename:str)->bool:
        """
        Check if an object with the given filename exists in the bucket.
        Args:
            filename (str): The name of the object to check.
        Returns:
            bool: True if the object exists, False otherwise.
        """ 
        try:
             # Use the stat_object method of the client to check if the object exists
            self.client.stat_object(self.bucket,filename)
        except:
            # If an exception is raised, return False
            return False
        return True

    def get_file(self,filename:str)->bytes:
        """
        Get the content of the object.
        Args:
            filename (str): The name of the file.
        Returns:
            bytes: The content of the object.
        Raises:
            None.
        """
        # Get the content of the object
        if self.object_exists(filename):
            content:bytes = self.client.get_object(self.bucket,filename)
            return content.data
        else:
            logging.warning("Object not exists: %s", filename)
            return b''
        
    def put_file(self,filename:str,content:str)->None:
        """
        Put the content of the object.
        Args:
            filename (str): The name of the file.
            content (str): The content of the object.
        Returns:
            None.
        Raises:
            None.
        """
        # Put the content of the object
        if not self.object_exists(filename):
            self.client.fput_object(self.bucket,filename,content,content_type="image/gif",)
        else:
            logging.warning("Object already exists: %s", filename)
    def remove_file(self,filename:str)->None:
         if self.object_exists(filename):
            self.client.remove_object(self.bucket,filename)

if __name__ == "__main__":
    m = Minio_client('config.ini')
    for i in range(1,9):
        m.put_file(f'cat{i}.gif',f'images/cat{i}.gif')
    
