class BaseConfig(object):
    DEBUG = True
    TESTING = True
    
    HOSTNAME = "http://localhost:5000/minid"

    AWS_ACCESS_KEY_ID = ""
    AWS_SECRET_ACCESS_KEY = ""

    MINID_SERVER = "http://minid.bd2k.org/minid"
    MINID_EMAIL = ""
    MINID_CODE = ""

    CREATE_MINID = True	
    MINID_TEST = True

    BUCKET_NAME = "encode-bags"

class ProdConfig(BaseConfig):
    DEBUG = False
    TESTING = False

    HOSTNAME = "<HOSTNAME>"

    AWS_ACCESS_KEY_ID = ""
    AWS_SECRET_ACCESS_KEY = ""

    MINID_SERVER = "http://minid.bd2k.org/minid"
    MINID_EMAIL = ""
    MINID_CODE = ""
        
    CREATE_MINID = True
    MINID_TEST = True

    BUCKET_NAME = "encode-bags"


