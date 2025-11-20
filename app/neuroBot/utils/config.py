from typing import List

from neuroBot.configuration.config import BaseGeneration
from core.config import BaseGenerationDataModel, FieldGeneration


class TempClass(BaseGeneration):
    def __init__(self, **kwargs):
        pass


def create_base_generation_model(
    list_data: List,
):

    print(1111)
    array = []
    for base, data in list_data:
        obj = TempClass()
        obj.SERVICE_NAME = base.SERVICE_NAME
        obj.SERVICE_ID = base.SERVICE_ID
        obj.TEXT_PREFIX = base.TEXT_PREFIX
        obj.CALLBACK_PREFIX = base.CALLBACK_PREFIX
        obj.FOLDER_NAME = base.FOLDER_NAME
        obj.FOLDER_NAME_GENERATION = base.FOLDER_NAME_GENERATION

        for i in data:
            print(123, i.KEY)
            setattr(obj, i.KEY, i.VALUE)
        print(obj.ID_IMAGGA_AUTHORIZATION)
        print(obj)
