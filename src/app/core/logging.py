import logging

import logging
logging.basicConfig(
    level=logging.info,
    format='%(asctime)s - %(levelname)-8s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    handlers=[
        logging.FileHandler("application.log"),  
        logging.StreamHandler()  
    ]
)

logger = logging.getLogger("app")
