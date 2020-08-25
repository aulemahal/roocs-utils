from roocs_utils.parameter import (
    collection_parameter,
    area_parameter,
    time_parameter,
    level_parameter,
)


def parameterise(collection=None, area=None, level=None, time=None):

    if collection:
        collection = collection_parameter.CollectionParameter(collection)

    area = area_parameter.AreaParameter(area)
    time = time_parameter.TimeParameter(time)
    level = level_parameter.LevelParameter(level)

    return locals()
