import gettext
import os


def getLocStrings():
    currentDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "localization")
    all_l = os.listdir(os.path.join(currentDir))
    return gettext.translation('resource', currentDir, all_l).gettext

_ = getLocStrings()
