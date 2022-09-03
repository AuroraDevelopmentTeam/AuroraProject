class VkAudioException(Exception):
    pass


class AudioNotFoundException(VkAudioException):
    pass


class AudioNotAvailable(VkAudioException):
    pass
