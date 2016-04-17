# Copyright (C) 2016 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/ArkwoodAR)

class Features:

    # initialise
    def __init__(self, config_provider):

        # cache
        self.cache = {}

        # features
        self.media_cube = None
        self.secret_item = None

        if config_provider.media_cube:
            from mediacube import MediaCube
            self.media_cube = MediaCube()

        elif config_provider.secret_item:
            from secretitem import SecretItem
            self.secret_item = SecretItem()
    
    # manage cache
    def _manage_cache(self, cache_key, detection):

        # put detection in cache
        if all(detection):
            self.cache[cache_key] = detection

        # get detection from cache
        elif (cache_key in self.cache) and (self.cache[cache_key]):
            detection = self.cache[cache_key]
            self.cache[cache_key] = None

        # otherwise bin detection         
        else:
            detection = None  
          
        return detection

    # detect feature
    def detect(self, image_one, image_two):

        detection = None

        if self.media_cube:
            detection = self._manage_cache('mediacube', 
                                (self.media_cube.detect(image_one),
                                 self.media_cube.detect(image_two)))

        if self.secret_item:
            detection = self._manage_cache('secretitem', 
                                (self.secret_item.detect(image_one),
                                 self.secret_item.detect(image_two)))
        
        return detection

    # render feature
    def render(self, image, detection_item):

        if self.media_cube:
            self.media_cube.render(detection_item)

        elif self.secret_item:
            image = self.secret_item.render(image, detection_item)

        return image  


