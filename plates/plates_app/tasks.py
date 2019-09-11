# coding: utf-8
from datetime import datetime
import urllib

from io import BytesIO

from PIL import Image
from celery import shared_task
import xml.etree.ElementTree as ET

from plates_app.models import NumberPlate


@shared_task(name="car model image retrieval")
def retrieve_image(model_name, plate_id):
    try:
        number_plate = NumberPlate.objects.get(id=plate_id)
        if not bool(number_plate.model_image):
            # retrieve file if no image
            endpoint = "http://www.carimagery.com/api.asmx/GetImageUrl?searchTerm={}".format(model_name)
            xml = urllib.request.urlopen(endpoint).read()
            tree = ET.parse(BytesIO(xml))
            root = tree.getroot()
            url = root.text
            # load file to get format
            image_file = Image.open(BytesIO(urllib.request.urlopen(url).read()))
            fmt = image_file.format
            image_file.close()
            # make new image name
            suffix = datetime.now().strftime("%y%m%d_%H%M%S")
            file_name = "%s_%s.%s" % (model_name, suffix, fmt)
            # save file to file field
            number_plate.model_image.save(file_name, urllib.request.urlopen(url))
            number_plate.save()
        else:
            return
    except Exception as e:
        raise e
