import os

RECEIVERS = os.environ['RECEIVERS'] if 'RECEIVERS' in os.environ else 'edmond.zhu@parcelx.io'
SENDER = os.environ['SENDER'] if 'SENDER' in os.environ else ""
EMAIL_HOST = os.environ['EMAIL_HOST'] if 'EMAIL_HOST' in os.environ else "smtp.mxhichina.com"
MAIL_SMTP_PORT = os.environ['MAIL_SMTP_PORT'] if 'MAIL_SMTP_PORT' in os.environ else 25
EMAIL_USER = os.environ['EMAIL_USER'] if 'EMAIL_USER' in os.environ else "no-reply@parcelx.io"
EMAIL_PWD = os.environ['EMAIL_PWD'] if 'EMAIL_PWD' in os.environ else ""

PARCELX_DB_HOST = os.environ['PARCELX_DB_HOST'] if 'PARCELX_DB_HOST' in os.environ else "parcelxmysql.mysql.database.azure.com"
PARCELX_DB_USER = os.environ['PARCELX_DB_USER'] if 'PARCELX_DB_USER' in os.environ else "azureuser@parcelxmysql"
PARCELX_DB_PWD = os.environ['PARCELX_DB_PWD'] if 'PARCELX_DB_PWD' in os.environ else ""
PARCELX_DB_PORT = os.environ['PARCELX_DB_PORT'] if 'PARCELX_DB_PORT' in os.environ else 3306

try:
    from local_settings import *
except ImportError:
    pass
