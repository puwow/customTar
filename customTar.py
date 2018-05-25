#-*- coding:utf-8 -*-
u'''结合os/tarfile模块客户化tar包类，以达到方便捆绑文件的目的'''
import os
import time
import tarfile
import re
import shutil
import datetime

class customTar:
    def __init__( self, tarFile=None, path=None, fileList=None, mode='r' ):
        self.tarFile = tarFile
        self.path = path
        self.fileList = fileList

    def tar( self, tarFile=None, path=None, fileList=None, cutPath=None, mode='w' ):
        u'''
        根据`fileList`文件清单在路径`path`下查找文件，将找到的结果文件
        去掉绝对路径后打包到以`tarFile`命名的tar包中。
        '''
        if tarFile is not None:
            self.tarFile = tarFile
        if path is not None:
            self.path = path
        if fileList is not None:
            self.fileList = fileList

        ext = os.path.splitext(self.tarFile)[1]
        if ext == '' or ext == None:
            self.tarFile = self.tarFile +".tar"
        tar = tarfile.open( self.tarFile, mode="w" )
        for item in self.fileList:
            if not re.search( r"%s"%(path), item ):
                item =  os.path.join( path, item ).replace("\\","/")
            arcname = item
            if cutPath is not None and cutPath != '':
                #正则中的变量要小心，如路径中包含\时，会被当做转义字符
                pat = re.compile( r"%s(.+)$"%(cutPath.replace("\\","/")) )
                result = re.match( pat, item )
                if result is not None:
                    arcname = result.groups()[0]
            tar.add( item, arcname )
        tar.close()

    def find( self, path=None, fileList=None, excludes=None, filters=True ):
        u'''
        根据`fileList`文件清单在`path`中查找文件，将找到的结果文件以迭代器
        的形式返回。注意：未找到的文件需要自己处理
        '''
        if path is not None:
            self.path = path
        if fileList is not None:
            self.fileList = fileList
        if os.path.exists( self.path ):
            for root, dirs, files in os.walk( self.path ):
                for item_file in files:
                    full_path_file = os.path.join( root, item_file ).replace("\\","/")
                    state=False
                    return_date=''
                    return_size='0 KB'
                    for item_fileList in self.fileList:
                        ret = False
                        #根据filters设置是否需要过滤文件
                        if filters is True:
                            ret = self.isFilter( full_path_file, excludes )
                        if ret is False:
                            pat = re.compile(r"%s$"%(item_fileList))
                            result = re.search( pat, full_path_file )
                            if result is not None and os.path.isfile(full_path_file):
                                state=True
                                st = os.stat( full_path_file )
                                file_date = datetime.datetime.fromtimestamp( st.st_mtime )
                                return_date = file_date.strftime("%Y-%m-%d %H:%M:%S")
                                return_size = customTar.calcSize( st.st_size )
                                yield (item_fileList, return_date, return_size, state )
    def find_auto( self, path=None, days=0, hours=0, minutes=0, seconds=0, excludes=None ):
        '''
        在`path`目录中查找`days`天内、`hours`小时内、`minutes`分钟内、`seconds`秒内的文件
        返回tuple迭代器，格式为(文件全路径, 文件最近一次修改时间, 文件大小，是否存在)
        '''
        if path is not None:
            self.path = path
        now_date = datetime.datetime.now()
        find_seconds = days*24*60*60 + hours*60*60 + minutes*60 + seconds

        if os.path.exists( self.path ) and os.path.isdir( self.path ):
            for root,dirs,files in os.walk( self.path ):
                for item_file in files:
                    full_path_file = os.path.join( root, item_file ).replace( "\\", "/" )
                    ret = self.isFilter( full_path_file, excludes )
                    if ret is False:
                        st = os.stat( full_path_file )
                        file_date = datetime.datetime.fromtimestamp( st.st_mtime )
                        dl = now_date - file_date

                        if dl.total_seconds() <= find_seconds:
                            yield (full_path_file.replace("\\","/"), file_date.strftime('%Y-%m-%d %H:%M:%S'), customTar.calcSize(st.st_size), True )
                        elif find_seconds == 0:
                            yield (full_path_file.replace("\\","/"), file_date.strftime('%Y-%m-%d %H:%M:%S'), customTar.calcSize(st.st_size), True )
    def isFilter( self, fname, excludes=None ):
        '''
        根据excludes判断文件是否应该被过滤掉，True-表示过滤， False-表示不过滤
        '''
        results = []
        if excludes is not None:
            for ftype,exclude in set(excludes):
                if ftype == 0:
                    pat = re.compile( r'/%s/'%(exclude) )
                elif ftype == 1:
                    pat = re.compile( r'/%s'%(exclude) )
                elif ftype == 2:
                    pat = re.compile( r'%s'%(exclude) )
                rst = re.search( pat, fname )
                if rst is None:
                    results.append( False )
                else:
                    results.append( True )
            if True in results:
                return True
            return False
        else:
            return False

    def find_filter( self, files=[], days=0, hours=0, minutes=0, seconds=0, excludes=None ):
        '''
        在`path`目录中查找`days`天内、`hours`小时内、`minutes`分钟内、`seconds`秒内的文件
        返回tuple迭代器，格式为(文件全路径, 文件最近一次修改时间, 文件大小)
        '''
        now_date = datetime.datetime.now()
        find_seconds = days*24*60*60 + hours*60*60 + minutes*60 + seconds

        if files:
            for fname, fdate, fsize, fstate in files:
                ret = self.isFilter( fname, excludes )
                if ret is False:
                    file_date = datetime.datetime.strptime( fdate, '%Y-%m-%d %H:%M:%S' )
                    dl = now_date - file_date

                    if dl.total_seconds() <= find_seconds:
                        yield (fname, fdate, fsize, fstate )
                    if find_seconds == 0:
                        yield (fname, fdate, fsize, fstate )

    @classmethod
    def calcSize( cls, num ):
        '''
        计算文件大小，返回最近单位的数值
        '''
        flag=['KB','MB','GB','TB','PB','EB','ZB','YB','BB']
        i=-1
        while True:
            num = num/1024.0
            i=i+1
            if num >= 1024.0:
                continue
            else:
                break
        return str(round(num,1))+" "+flag[i]

if __name__ == '__main__':
    ctar = customTar()
    fileList=['js/core/certificateBoss.js','bank.js']
    path="F:\\newmobileBank_RoboAdvisor\\"
    tarName = "abc.tar"
    #ctar.tar( tarName, path, fileList, cutPath=path )
    #ctar.tar_del(tarName, fileList )
    #print customTar.calcSize(90000000000)
