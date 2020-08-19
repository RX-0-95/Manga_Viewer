import re

class FileMatch():
    __version__ = 0.1
    
    @staticmethod
    def isJpg(filename):
        return bool(re.match(r".*\.jpg$",filename,re.I))    
    @staticmethod
    def isPng(filename):
        return bool(re.match(r".*\.png$",filename,re.I))  
    @staticmethod
    def isJpeg(filename):
        return bool(re.match(r".*\.jpeg$",filename,re.I))  
    @staticmethod
    def isImage(filename):
        return bool(re.match(r".*\.jpg$|.*\.png$|.*\.jpeg$",filename,re.I))  
    @staticmethod
    def isZip(filename):
        return bool(re.match(r".*\.zip$",filename,re.I))
    



if __name__ == "__main__":
    jpgfile = 'fdsafdsafd.JPG'
    notJpgfile = 'gdsag4454.xxx'
    print(fileMatch.isJpg(jpgfile))
    print(fileMatch.isJpg(notJpgfile))

    pngfile = '464545sdaf5435.png'
    notPngfile = '45fdsa^&.xxx'
    print(fileMatch.isPng(pngfile))
    print(fileMatch.isPng(notPngfile))


    jpegfile = '464545sdaf5435.jpeg'
    notJpegfile = '45fdsa^&.xxx'
    print(fileMatch.isJpeg(jpegfile))
    print(fileMatch.isJpeg(notJpegfile))

    print(fileMatch.isImage(jpegfile))
    print(fileMatch.isImage(notJpegfile))
    print(fileMatch.isImage(jpgfile))
    print(fileMatch.isImage(notJpgfile))
