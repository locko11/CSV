
from celery import shared_task
from time import sleep
from .models import Schema

@shared_task
def mul(x):
    print('hello')
    sleep(x)
    print("""
              ------------------------------------------------
                       .   *   ..  . *  *
                     *  * @()Ooc()*   o  .
                         (Q@*0CG*O()  ___
                        |\_________/|/ _ \
                        |  |  |  |  | / | |
                        |  |  |  |  | | | |
                        |  |  |  |  | | | |
                        |  |  |  |  | | | |
                        |  |  |  |  | | | |
                        |  |  |  |  | \_| |
                        |  |  |  |  |\___/  
                        |\_|__|__|_/|
                         \_________/
              ------------------------------------------------
              """)

    return 'hello'


print(Schema)
