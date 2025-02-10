import os ,sys
import re
from Malware_Detection import File_Detection
import time

class ADS():
    def __init__(self,folderPath): # Enter Directory path.
        self.folderPath = folderPath #Path

    # List all paths of folders under perant directory
    def scan(self,top):
        try:
            dirs = [top]
            while dirs:
                dirpath = dirs.pop()
                with os.scandir(dirpath) as entries:
                    for entry in entries:
                        if entry.is_dir():
                            dirs.append(entry.path)
                            yield entry.path
                            #yield from self.scan(entry.path)
        except PermissionError:
            pass
    def SubDirectory(self):
        listPath = list()
        for filepath in self.scan(self.folderPath):
            listPath.append(filepath)
        listPath.append(self.folderPath)
        return listPath
        # listPath = list()
        # for dirpath, dirnames, filenames in os.walk(self.folderPath):
        #     # Print the path of each directory
        #     for dirname in dirnames:
        #         listPath.append(os.path.join(dirpath, dirname))
        # listPath.append(self.folderPath)  # here adding the path of folderPath to listPath
        # return listPath;

    def matchADSfiles(self,sub_dir): # return lists inside list [[],[],...]# ====> 4
        try:
            if os.path.exists(sub_dir):
                output = os.popen(f'dir /r "{sub_dir}"').read()
                pattern = r'(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2}\s+[AP]M)\s+' \
                          r'(\d{1,3},\d{1,3},\d{1,3}|\d{1,3},\d{1,3}|\d{1,3})+\s+([a-zA-Z0-9\s\.\-_]+\.{1}[a-zA-Z0-9\s\.\-_]{2,10})\s' \
                          r'+(\d{1,3},\d{1,3},\d{1,3}|\d{1,3},\d{1,3}|\d{1,3})\s+' \
                          r'([a-zA-Z0-9\s\.\-_]+\.{1}[a-zA-Z0-9\s\.\-_]{2,10}:[a-zA-Z0-9\s\.\-_]+\.{1}[a-zA-Z0-9\s\.\-_]{2,10})'
                match = re.compile(pattern, re.IGNORECASE).findall(output)
                if match != []:
                    if match != None:
                        listWithPath = list()
                        for group in match:
                            addpath = list(group)
                            addpath.append(sub_dir)
                            #group = tuple(addpath)
                            listWithPath.append(addpath)
                        return listWithPath;
                    else:
                        return []
                else:
                    return []
            else:
                return []
        except (FileNotFoundError,OSError):
            return []

    def List_All_ADS_Files(self,path):# ====> 3
        return self.matchADSfiles(path)

    #        [['03/25/2023', '10:19 PM', '1,593', 'Calculator.lnk', '27', 'Calculator.lnk:hidden2.txt','C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\myhiddenstuff'],
    #        ['03/10/2023', '02:03 AM', '986,847', 'Lake.jpg', '27', 'Lake.jpg:hidden.txt', 'C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\myhiddenstuff'],
    #        ['03/12/2023', '01:48 AM', '23', 'test.txt', '986,847', 'test.txt:Lake.jpg', 'C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\myhiddenstuff']]

    # list full path of ADS files
    def listpath(self,path):
        ADStable = self.List_All_ADS_Files(path)
        #        <<<<List_All_ADS_Files(path)>>>
        # sample=[['03/25/2023', '10:19 PM', '1,593', 'Calculator.lnk', '27', 'Calculator.lnk:hidden2.txt', 'C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\myhiddenstuff'],
        #        ['03/10/2023', '02:03 AM', '986,847', 'Lake.jpg', '27', 'Lake.jpg:hidden.txt', 'C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\myhiddenstuff'],
        #        ['03/12/2023', '01:48 AM', '23', 'test.txt', '986,847', 'test.txt:Lake.jpg', 'C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\myhiddenstuff']]
        #   C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\myhiddenstuff\\Calculator.lnk:hidden2.txt

        fullPathlist =list()
        for element in ADStable:
            fullPath = os.path.join(element[6], element[5]).replace("/", "\\")
            fullPathlist.append(fullPath)
        return fullPathlist;

    def listpath2(self,path):
        ADStable = self.List_All_ADS_Files(path)
        #        <<<<List_All_ADS_Files(path)>>>
        # sample=[['03/25/2023', '10:19 PM', '1,593', 'Calculator.lnk', '27', 'Calculator.lnk:hidden2.txt', 'C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\myhiddenstuff'],
        #        ['03/10/2023', '02:03 AM', '986,847', 'Lake.jpg', '27', 'Lake.jpg:hidden.txt', 'C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\myhiddenstuff'],
        #        ['03/12/2023', '01:48 AM', '23', 'test.txt', '986,847', 'test.txt:Lake.jpg', 'C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\myhiddenstuff']]
        #   C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\myhiddenstuff\\Calculator.lnk:hidden2.txt

        fullPathlist =list()
        for element in ADStable:
            fullPath = os.path.join(element[6], element[3]).replace("/", "\\")
            fullPathlist.append(fullPath)
        return fullPathlist;
    # ['C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\myhiddenstuff\\Calculator.lnk:hidden2.txt',
    #  'C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\myhiddenstuff\\Lake.jpg:hidden.txt',
    #  'C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\myhiddenstuff\\test.txt:Lake.jpg']

    # in this function will make malware & virus detection every file found that came from metadata()...
    def Detection_ADS_Files(self,path):# ====> 2
        check = File_Detection()

        ADStable = self.List_All_ADS_Files(path)
        detecte_result = list()
        for path in self.listpath(path):
            result = check.malware_checker(path)
            detecte_result.append(result)
            time.sleep(15)

        #ADStable = self.List_All_ADS_Files(path)
        #        [['03/25/2023', '10:19 PM', '1,593', 'Calculator.lnk', '27', 'Calculator.lnk:hidden2.txt','C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\myhiddenstuff'],
        #        ['03/10/2023', '02:03 AM', '986,847', 'Lake.jpg', '27', 'Lake.jpg:hidden.txt', 'C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\myhiddenstuff'],
        #        ['03/12/2023', '01:48 AM', '23', 'test.txt', '986,847', 'test.txt:Lake.jpg', 'C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\myhiddenstuff']]

        for index,element in enumerate(detecte_result):
            ADStable[index].append(element) #detecte_result[index]

        return ADStable;

    def get_final_result(self,path):# ====> 1
        All_ADS_files_list=self.Detection_ADS_Files(path)
        sorted_list = sorted(All_ADS_files_list, key=lambda x: x[0], reverse=True)
        return sorted_list;







class ADS_options:
    def __init__(self,filename):
        self.filename = filename #C:/Users/OJCYS/OneDrive/Desktop/NormalFile/important files/image.jpeg

    def addStream(self, Hidden_File_path): # the file you want to hide in filename
        #C:/Users/OJCYS/OneDrive/Desktop/NormalFile/important files/Important_Document.txt <<==ADS
        try:
            self.filename =self.filename.replace("/", "\\").strip()
            Hidden_File_path = Hidden_File_path.replace("/", "\\")
            hide_file = re.compile("[a-zA-Z0-9]+\.{1}[a-zA-Z0-9]{2,4}").search(Hidden_File_path).group()
            #hide_file = "Important_Document.txt"
            #C:/Users/OJCYS/OneDrive/Desktop/NormalFile/important files/Important_Document.txt
            if os.path.exists(self.filename) and os.path.exists(Hidden_File_path):
                os.popen(f'type "{Hidden_File_path}">"{self.filename}:{hide_file}"')
                #C:/Users/OJCYS/OneDrive/Desktop/NormalFile/important files/image.jpeg:Important_Document.txt
                return True
            else:
                return False
        except Exception as e:
            return False

    def extractStream(self,savePath):
        try:
            self.filename = self.filename.replace("/", "\\").strip()
            savePath = savePath.replace("/", "\\")
            if self.filename != '':
                os.popen(f'more <"{self.filename}"> "{savePath}"') # more < myfile.txt:hidden.exe >  savePath
                return True
            else:
                return False
        except Exception as e:
            return False

    def removeStream(self):
        try:
            if os.path.exists(self.filename):
                filename = self.filename.replace("/", "\\").strip()
                #os.remove(filename)
                os.popen(f'streams -d "{filename}"')
                #print(f"{self.filename} is Deleted.")
                return True
            else:
                return False
        except Exception as e:
            return False


#C:\Users\OJCYS\OneDrive\Desktop\NormalFile\myhiddenstuff\folder
# output ="C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\"
# ads=ADS_options(output)
# ads.matchADSfiles("C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\")
# print(ads.addStream("C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\important files\\comment.txt"))
#C:/Users/OJCYS/OneDrive/Desktop/NormalFile/important files/Detaild Material Module 1 Computer Forensics Fundamentals.pdf
#C:/Users/OJCYS/OneDrive/Desktop/NormalFile/important files/comment.txt