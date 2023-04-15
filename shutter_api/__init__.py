from flaskext.mysql import MySQL
from imagekitio import ImageKit

IMAGEKIT = ImageKit(
    private_key='private_SCH+JttARw6RRAs1chpVMob/5ds=',
    public_key='public_5DMySowL3WoFyoqlVACXhvjsuCQ=',
    url_endpoint="https://ik.imagekit.io/shutterAppULaval"
)

MYSQL = MySQL()
