import os, yt_dlp
from time import sleep as s

class dlLogger:
    def debug(self, msg):
        print(msg)
        
    def info(self, msg):
        pass

    def warning(self, msg):
        pass
    
    def error(self, msg):
        print(msg)
        raise Exception(msg)

class DLv2:
    yesOrNo = {"y" : True, "n" : False, "" : False}
    formatOptionCheck = {"0" : True, "1" : True, "2" : True, "3" : True, "4" : True, "5" : True, "6" : True, "7" : True, "8" : True}
    qualityOptionCheck = {"0" : True, "1" : True, "2" : True, "3" : True, "4" : True}

    formatToEXT = ["", "4320", "2460", "1440", "1080", "720", "480", "mp3", "wav"]
    qualityToBitrate = ["", "320", "256", "192", "128", "64"]

    qualityOption = ""
    formatOption = ""
    saveLocation = ""

    url = []

    def __init__(self) -> None:
        self.Main()

    def dl(self, opt, iter):
        try:
            yt_dlp.YoutubeDL(opt).download(iter)
        except Exception:
            pass

    def Main(self):
        os.chdir(str(os.path.dirname(__file__) + "\\"))

        print("Advanced mode? (y/n: default n)")
        advancedMode = self.yesOrNo[input(">>> ")]

        while True:
            print("0 - Best, 1 - 8K, 2 - 4K, 3 - 1440p, 4 - 1080p, 5 - 720p, 6 - 480p, 7 - MP3, 8 - WAV")
            check = input(">>> ")
            if self.formatOptionCheck[check]:
                self.formatOption = int(check)
                break
        
        if advancedMode:
            while True:
                print("0 - Best, 1 - 320kbps, 2 - 256kbps, 3 - 192kbps, 4 - 128kbps, 5 - 64kbps")
                check = input(">>> ")
                if self.qualityOptionCheck[check]:
                    self.qualityOption = int(check)
                    break

            print("Enter a url, then press enter and repeat until you have entered all URLs.\nWhen the last URL has been input, press enter with the input space blank")# Advanced mode multi url entering
            self.url.append(str(input(">>> ")))
            while True:
                check = str(input(">>> "))
                if check == "":
                    break
                else:
                    self.url.append(check)

            while True:
                print("Where would you like to save your file(s)?\nPlease enter a full path to an existing folder or press enter for default location. (Default is Downloads\\YTDL)")
                check = input(">>> ")
                if os.path.exists(check):
                    self.saveLocation = check
                    break
                elif check == "":
                    self.saveLocation = os.path.join(os.path.expanduser("~"), "Downloads\\YTDL")
                    break

        else:
            self.qualityOption = 2
            self.saveLocation = os.path.join(os.path.expanduser("~"), "Downloads\\YTDL")

            print("Enter the URL")
            self.url.append(input(">>> "))


        if self.formatOption == 7 or self.formatOption == 8:
            if self.qualityOption == 0:
                options = {"format" : "ba*", "outtmpl" : self.saveLocation + r"\%(title)s-%(id)s.%(ext)s", "postprocessors" : [{"key" : "FFmpegExtractAudio", "preferredcodec" : "{}".format(self.formatToEXT[self.formatOption])}], "logger" : dlLogger()}
                for i in self.url:
                    self.dl(options, i)
            else:
                options = {"format" : "ba*[abr<={}]".format(self.qualityToBitrate[self.qualityOption]), "outtmpl" : self.saveLocation + r"\%(title)s-%(id)s.%(ext)s", "postprocessors" : [{"key" : "FFmpegExtractAudio", "preferredcodec" : "{}".format(self.formatToEXT[self.formatOption]), "preferredquality" : "{}".format(self.qualityToBitrate[self.qualityOption])}], "logger" : dlLogger()}
                for i in self.url:
                    self.dl(options, i)

        elif not self.formatOption == 0:
            if self.qualityOption == 0:
                options = {"format" : "bv*[height<={}]+ba".format(self.formatToEXT[self.formatOption]), "outtmpl" : self.saveLocation + r"\%(title)s-%(id)s.%(ext)s", "postprocessors" : [{"key" : "FFmpegVideoRemuxer", "preferedformat" : "mp4",}], "logger" : dlLogger()}
                for i in self.url:
                    self.dl(options, i)
            else:
                options = {"format" : "bv*[height<={}]+ba[abr<={}]".format(self.formatToEXT[self.formatOption], self.qualityToBitrate[self.qualityOption]), "outtmpl" : self.saveLocation + r"\%(title)s-%(id)s.%(ext)s", "postprocessors" : [{"key" : "FFmpegVideoRemuxer", "preferedformat" : "mp4",}], "logger" : dlLogger()}
                for i in self.url:
                    self.dl(options, i)
        else:
            if self.qualityOption == 0:
                options = {"format" : "bv*+ba", "outtmpl" : self.saveLocation + r"\%(title)s-%(id)s.%(ext)s", "postprocessors" : [{"key" : "FFmpegVideoRemuxer", "preferedformat" : "mp4",}], "logger" : dlLogger()}
                for i in self.url:
                    self.dl(options, i)
            else:
                options = {"format" : "bv*+ba[abr<={}]".format(self.qualityToBitrate[self.qualityOption]), "outtmpl" : self.saveLocation + r"\%(title)s-%(id)s.%(ext)s", "postprocessors" : [{"key" : "FFmpegVideoRemuxer", "preferedformat" : "mp4",}], "logger" : dlLogger()}
                for i in self.url:
                    self.dl(options, i)

        print("Your file(s) have been saved at {}".format(self.saveLocation))
        s(5)

DLv2()