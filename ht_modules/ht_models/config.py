import os
from ht_config import ConfigDev, ConfigProd, ConfigLocal

match os.environ.get('FLASK_ENV'):
    case 'dev':
        config = ConfigDev()
        print('- ht_models/config: Development')
    case 'prod':
        config = ConfigProd()
        print('- ht_models/config: Production')
    case _:
        config = ConfigLocal()
        print('- ht_models/config: Local')
    