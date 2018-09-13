#-*- coding:utf-8 -*-

import os
import time
import shelve
import wx
import wx.lib.agw.aui as aui
from customTar import customTar
import wx.lib.agw.foldpanelbar as fpb
import wx.lib.scrolledpanel as scrolled
from Connection import Connection
import json


import random
import numpy as np
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

images=['images/filetype/default.png', 'images/filetype/html.png', 'images/filetype/css.png', 'images/filetype/js.png', \
        'images/filetype/json.png', 'images/filetype/png.png', 'images/filetype/dir.png', 'images/filetype/re.png']

SHE_DB = "she.db"

class CanvasPanel( wx.Panel ):
    def __init__( self, parent, id=wx.ID_ANY ):
        wx.Panel.__init__( self, parent=parent, id=id )
        self.figure = Figure(figsize=(8,3))
        self.axes = self.figure.add_subplot(111, projection="3d")
        self.canvas = FigureCanvas( self, -1, self.figure )
        self.sizer = wx.BoxSizer( wx.VERTICAL )
        self.sizer.Add( self.canvas, 1, wx.ALIGN_CENTER )
        self.SetSizer(self.sizer)
        self.draw()
        self.Fit()
    def draw( self ):
        x, y = np.random.rand( 2, 100 ) * 4
        hist, xedges, yedges = np.histogram2d(x, y, bins=4, range=[[0, 8], [0, 8]])

        xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25)
        xpos = xpos.flatten('F')
        ypos = ypos.flatten('F')
        zpos = np.zeros_like(xpos)
        
        # Construct arrays with the dimensions for the 16 bars.
        dx = 0.5 * np.ones_like(zpos)
        dy = dx.copy()
        dz = hist.flatten()
        self.axes.set_title('V3.1.7')
        
        self.axes.bar3d(xpos, ypos, zpos, dx, dy, dz, color=random.choice(['r','g','b']), zsort='average')

class RegDialog( wx.Dialog ):
    def __init__( self, parent, title=u'新用户注册', size=(480,360), style=wx.DEFAULT_DIALOG_STYLE, name="reg" ):
        wx.Dialog.__init__( self, parent=parent, title=title, size=size, style=style, name=name )
        panel = wx.Panel( self, id=wx.ID_ANY )
        vbox = wx.BoxSizer( wx.VERTICAL )
        image = wx.Image("images/design.png")
        image.Rescale(480,120)

        bmp_title = wx.StaticBitmap( panel, id=wx.ID_ANY, bitmap = image.ConvertToBitmap() )
        username = wx.TextCtrl( panel, id=wx.ID_ANY )
        password = wx.TextCtrl( panel, id=wx.ID_ANY, style=wx.TE_PASSWORD )
        password2 = wx.TextCtrl( panel, id=wx.ID_ANY, style=wx.TE_PASSWORD )
        realname = wx.TextCtrl( panel, id=wx.ID_ANY )
        btn_login = wx.Button( panel, id=wx.ID_OK, label=u'注册' )
        btn_close = wx.Button( panel, id=wx.ID_CANCEL, label=u'关闭' )

        hboxA = wx.BoxSizer( wx.HORIZONTAL )
        hboxA.Add( wx.StaticText( panel, -1 ), 1 )
        hboxA.Add( wx.StaticText(panel, -1, label=u'登 录 名:'), 1, wx.ALIGN_RIGHT|wx.ALIGN_CENTER )
        hboxA.Add( username, 2, wx.EXPAND )
        hboxA.Add( wx.StaticText( panel, -1 ), 1 )

        hboxB = wx.BoxSizer( wx.HORIZONTAL )
        hboxB.Add( wx.StaticText( panel, -1 ), 1 )
        hboxB.Add( wx.StaticText(panel, -1, label=u'登录密码:'), 1, wx.ALIGN_RIGHT|wx.ALIGN_CENTER )
        hboxB.Add( password, 2, wx.EXPAND )
        hboxB.Add( wx.StaticText( panel, -1 ), 1 )

        hboxC = wx.BoxSizer( wx.HORIZONTAL )
        hboxC.Add( wx.StaticText( panel, -1 ), 1 )
        hboxC.Add( wx.StaticText(panel, -1, label=u'密码确认:'), 1, wx.ALIGN_RIGHT|wx.ALIGN_CENTER )
        hboxC.Add( password2, 2, wx.EXPAND )
        hboxC.Add( wx.StaticText( panel, -1 ), 1 )

        hboxD = wx.BoxSizer( wx.HORIZONTAL )
        hboxD.Add( wx.StaticText( panel, -1 ), 1 )
        hboxD.Add( wx.StaticText(panel, -1, label=u'真实姓名:'), 1, wx.ALIGN_RIGHT|wx.ALIGN_CENTER )
        hboxD.Add( realname, 2, wx.EXPAND )
        hboxD.Add( wx.StaticText( panel, -1 ), 1 )

        hboxE = wx.BoxSizer( wx.HORIZONTAL )
        hboxE.Add( btn_login, 0, wx.RIGHT, 5 )
        hboxE.Add( btn_close, 0, wx.LEFT, 5 )

        vbox_m = wx.BoxSizer( wx.VERTICAL )
        vbox_m.Add( hboxA, 0, wx.EXPAND|wx.ALL, 5 )
        vbox_m.Add( hboxB, 0, wx.EXPAND|wx.ALL, 5 )
        vbox_m.Add( hboxC, 0, wx.EXPAND|wx.ALL, 5 )
        vbox_m.Add( hboxD, 0, wx.EXPAND|wx.ALL, 5 )

        vbox.Add( bmp_title, 0, wx.ALIGN_CENTER|wx.TOP, 0 )
        vbox.Add( vbox_m, 1, wx.EXPAND|wx.ALL, 5 )
        vbox.Add( hboxE, 0, wx.ALIGN_CENTER|wx.BOTTOM, 20 )

        panel.SetSizer( vbox )

class LoginDialog( wx.Dialog ):
    def __init__( self, parent, title=u'用户登录', size=(480,360), style=wx.DEFAULT_DIALOG_STYLE, name="login" ):
        wx.Dialog.__init__( self, parent=parent, title=title, size=size, style=style, name=name )
        panel = wx.Panel( self, id=wx.ID_ANY )
        vbox = wx.BoxSizer( wx.VERTICAL )
        image = wx.Image("images/design.png")
        image.Rescale(480,120)

        self.message = wx.StaticText( panel, id=wx.ID_ANY )
        self.message.SetForegroundColour("red")
        bmp_title = wx.StaticBitmap( panel, id=wx.ID_ANY, bitmap = image.ConvertToBitmap() )
        self.username = username = wx.TextCtrl( panel, id=wx.ID_ANY )
        self.password = password = wx.TextCtrl( panel, id=wx.ID_ANY, style=wx.TE_PASSWORD )
        btn_login = wx.Button( panel, id=wx.ID_OK, label=u'登录' )
        btn_close = wx.Button( panel, id=wx.ID_CANCEL, label=u'关闭' )

        hboxA = wx.BoxSizer( wx.HORIZONTAL )
        hboxA.Add( wx.StaticText( panel, -1 ), 1 )
        hboxA.Add( wx.StaticText(panel, -1, label=u'登 录 名:'), 1, wx.ALIGN_RIGHT|wx.ALIGN_CENTER )
        hboxA.Add( username, 2, wx.EXPAND )
        hboxA.Add( wx.StaticText( panel, -1 ), 1 )

        hboxB = wx.BoxSizer( wx.HORIZONTAL )
        hboxB.Add( wx.StaticText( panel, -1 ), 1 )
        hboxB.Add( wx.StaticText(panel, -1, label=u'登录密码:'), 1, wx.ALIGN_RIGHT|wx.ALIGN_CENTER )
        hboxB.Add( password, 2, wx.EXPAND )
        hboxB.Add( wx.StaticText( panel, -1 ), 1 )

        hboxC = wx.BoxSizer( wx.HORIZONTAL )
        hboxC.Add( btn_login, 0, wx.RIGHT, 5 )
        hboxC.Add( btn_close, 0, wx.LEFT, 5 )

        hboxD = wx.BoxSizer( wx.HORIZONTAL )
        hboxD.Add( wx.StaticText( panel, -1 ), 1 )
        hboxD.Add( self.message, 2, wx.EXPAND|wx.ALIGN_LEFT )
        hboxD.Add( wx.StaticText( panel, -1 ), 1 )

        vbox_m = wx.BoxSizer( wx.VERTICAL )
        vbox_m.Add( hboxA, 0, wx.EXPAND|wx.ALL, 5 )
        vbox_m.Add( hboxB, 0, wx.EXPAND|wx.ALL, 5 )

        vbox.Add( bmp_title, 0, wx.ALIGN_CENTER|wx.TOP, 0 )
        vbox.Add( vbox_m, 2, wx.EXPAND|wx.ALL, 5 )
        vbox.Add( hboxD, 1, wx.EXPAND|wx.ALIGN_CENTER|wx.BOTTOM, 20 )
        vbox.Add( hboxC, 1, wx.ALIGN_CENTER|wx.BOTTOM, 20 )

        self.Bind( wx.EVT_BUTTON, self.OnLogin, btn_login )

        panel.SetSizer( vbox )

    def OnLogin( self, event ):
        username = self.username.GetValue()
        password = self.username.GetValue()
        data = {"username":username, "password":password}
        conn = Connection()
        resp = conn.ajax( resource='/user', data=data )
        if resp.get("code") == 200:
            wx.MessageBox( resp.get("msg") )
        else:
            self.message.SetLabel( resp.get("msg") )

class PackDialog( wx.Dialog ):
    def __init__( self, parent, id=wx.ID_ANY, title=u'创建版本包', size=(480,360) ):
        wx.Dialog.__init__( self, parent=parent, id=id, title=title, size=size )

        panel = wx.Panel( self, -1 )

        title = wx.StaticText( panel, id=-1, label=u'创建空包' )
        lab_pack_uuid = wx.StaticText( panel, id=-1, label=u'包标识' )
        lab_pack_name = wx.StaticText( panel, id=-1, label=u'包名' )
        lab_pack_ver = wx.StaticText( panel, id=-1, label=u'版本号' )
        lab_pack_desc = wx.StaticText( panel, id=-1, label=u'包描述' )

        pack_uuid = wx.TextCtrl( panel, id=wx.ID_ANY )
        pack_name = wx.TextCtrl( panel, id=wx.ID_ANY )
        pack_ver = wx.TextCtrl( panel, id=wx.ID_ANY )
        pack_desc = wx.TextCtrl( panel, id=wx.ID_ANY )

        btn_create = wx.Button( panel, id=wx.ID_OK, label=u'创建' )
        btn_cancel = wx.Button( panel, id=wx.ID_CANCEL, label=u'取消' )

        bag = wx.GridBagSizer( 5, 5 )
        bag.AddMany([
            (lab_pack_uuid, (0,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.RIGHT, 5 ),(pack_uuid, (0,1), wx.DefaultSpan, wx.EXPAND),\
            (lab_pack_name, (1,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.RIGHT, 5 ),(pack_name, (1,1), wx.DefaultSpan, wx.EXPAND),\
            (lab_pack_ver,  (2,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.RIGHT, 5 ),(pack_ver,  (2,1), wx.DefaultSpan, wx.EXPAND),\
            (lab_pack_desc, (3,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.RIGHT, 5 ),(pack_desc, (3,1), wx.DefaultSpan, wx.EXPAND)
            ])

        bag.AddGrowableCol(1,1)
        bag.AddGrowableRow(3,1)

        hbox = wx.BoxSizer( wx.HORIZONTAL )
        hbox.AddMany([
            (btn_create, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.TOP, 10 ),
            (btn_cancel, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 10 )
            ])

        vbox = wx.BoxSizer( wx.VERTICAL )
        vbox.Add( title, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 10 )
        vbox.Add( bag, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 30 )
        vbox.Add( hbox, 0, wx.TOP|wx.ALIGN_CENTER|wx.BOTTOM, 30 )

        panel.SetSizer( vbox )

class CustomSlider( wx.Panel ):
    def __init__( self, parent, value=0, minValue=0, maxValue=1, label='' ):
        wx.Panel.__init__( self, parent=parent, id=wx.ID_ANY, size=(-1,32) )
        self.lab = wx.StaticText( self, id=wx.ID_ANY, label=label )
        self.slider = wx.Slider( self, id=wx.ID_ANY, value=value, \
                minValue=minValue, maxValue=maxValue, style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS|wx.SL_TOP|wx.SL_SELRANGE )
        box = wx.BoxSizer( wx.HORIZONTAL )
        box.Add( self.lab, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 0 )
        box.Add( self.slider, 1, wx.EXPAND|wx.TOP|wx.BOTTOM, 0 )
        self.SetSizer( box )
    def getControl(self, ctype="slider"):
        if ctype == "slider":
            return self.slider

class CustomComboBox( wx.Panel ):
    def __init__( self, parent, choices=[], label='' ):
        wx.Panel.__init__( self, parent=parent, id=wx.ID_ANY, size=(-1,32) )
        self.btn_path = wx.Button( self, id=wx.ID_ANY, label=label )
        self.ctrl_path = ctrl_path = wx.ComboBox( self, id=wx.ID_ANY, choices=choices )
        box = wx.BoxSizer( wx.HORIZONTAL )
        box.Add( self.ctrl_path, 1, wx.EXPAND|wx.TOP|wx.BOTTOM, 0 )
        box.Add( self.btn_path, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
        self.SetSizer( box )
    def getControl( self, ctype="combobox" ):
        if ctype == "combobox":
            return self.ctrl_path
        else:
            return self.btn_path

class InfoPanel( wx.Panel ):
    def __init__( self, parent, id=wx.ID_ANY, name='InfoPanel' ):
        wx.Panel.__init__( self, parent, id=id, name='InfoPanel' )
        images=["images/compile48.png","images/pack48.png","images/deploy48.png","images/autotest48.png"]
        arrowImage = "images/arrow32.png"

        i=0
        grid = wx.GridSizer( 1, 7, 5, 5 )
        for index in range(7):
            if index%2 == 1:
                bmp = wx.Bitmap( arrowImage, wx.BITMAP_TYPE_PNG )
            else:
                bmp = wx.Bitmap( images[i], wx.BITMAP_TYPE_PNG )
                i=i+1
            sb = wx.StaticBitmap( self, id=wx.ID_ANY, bitmap=bmp )
            grid.Add( sb, 0, wx.ALIGN_CENTER )

        hbox = wx.BoxSizer( wx.HORIZONTAL )
        hbox.Add( grid, 1, wx.EXPAND )
        hbox.Add( wx.StaticText( self, -1), 1, wx.EXPAND )

        self.SetSizer( hbox )
        grid.Fit(self)

class OperPanel( fpb.FoldPanelBar ):
    def __init__( self, parent, id=wx.ID_ANY, name='operPanel' ):
        fpb.FoldPanelBar.__init__( self, parent=parent, id=id, size=(-1,-1) )

        self.imageList = wx.ImageList( 16, 16 )
        for image in images:
            if os.path.exists( image ):
                bmp = wx.Bitmap( image, wx.BITMAP_TYPE_PNG )
                self.imageList.Add( bmp )

        self.files = []
        item = self.AddFoldPanel( u"项目设置", collapsed=True )

        self.ctrl_path = CustomComboBox( item, label=u'选择项目' )
        self.AddFoldPanelWindow( item, self.ctrl_path, fpb.FPB_ALIGN_WIDTH, 5, 5, 5 )

        item = self.AddFoldPanel( u"文件查找", collapsed=True )
        self.ctrl_days = CustomSlider( item,  maxValue=30, label=u'天' )
        self.ctrl_hours = CustomSlider( item, maxValue=23, label=u'时' )
        self.ctrl_minutes = CustomSlider( item, maxValue=59, label=u'分' )
        self.ctrl_seconds = CustomSlider( item, maxValue=59, label=u'秒' )

        self.AddFoldPanelWindow( item, self.ctrl_days, fpb.FPB_ALIGN_WIDTH, 5, 5, 5 )
        self.AddFoldPanelWindow( item, self.ctrl_hours, fpb.FPB_ALIGN_WIDTH, 5, 5, 5 )
        self.AddFoldPanelWindow( item, self.ctrl_minutes, fpb.FPB_ALIGN_WIDTH, 5, 5, 5 )
        self.AddFoldPanelWindow( item, self.ctrl_seconds, fpb.FPB_ALIGN_WIDTH, 5, 5, 5 )

        item = self.AddFoldPanel( u"文件过滤", collapsed=True )
        self.ctrl_list = wx.ListCtrl( item, id=wx.ID_ANY, style=wx.LC_REPORT|wx.LC_VRULES|wx.LC_HRULES )
        self.ctrl_list.InsertColumn( 0, u'过滤类型', format=wx.LIST_MASK_TEXT|wx.LIST_FORMAT_CENTER|wx.LIST_MASK_IMAGE, width=80 )
        self.ctrl_list.InsertColumn( 1 , u'过滤内容', width=120 )
        self.AddFoldPanelWindow( item, self.ctrl_list, fpb.FPB_ALIGN_WIDTH, 5, 5, 5 )
        self.ctrl_list.AssignImageList( self.imageList, wx.IMAGE_LIST_SMALL )

        item = self.AddFoldPanel( u"包状态", collapsed=False )
        canvas = CanvasPanel( item, id=wx.ID_ANY )
        self.AddFoldPanelWindow( item, canvas, fpb.FPB_ALIGN_WIDTH, 5, 5, 5 )

        self.Bind( wx.EVT_BUTTON, self.OnSelectPath, self.ctrl_path.getControl("button") )
        self.Bind( wx.EVT_SCROLL_CHANGED, self.OnSlider, self.ctrl_days.getControl("slider") )
        self.Bind( wx.EVT_SCROLL_CHANGED, self.OnSlider, self.ctrl_hours.getControl("slider") )
        self.Bind( wx.EVT_SCROLL_CHANGED, self.OnSlider, self.ctrl_minutes.getControl("slider") )
        self.Bind( wx.EVT_SCROLL_CHANGED, self.OnSlider, self.ctrl_seconds.getControl("slider") )
        self.Bind( wx.EVT_COMBOBOX, self.OnChangePath, self.ctrl_path.getControl("combobox") )
        self.Bind( wx.EVT_CONTEXT_MENU, self.OnList, self.ctrl_list )

        wx.CallAfter( self.ReadFromShe )

    def OnList( self, event ):
        if not hasattr( self, "deleteMenu" ):
            self.deleteMenu = wx.NewId()
            self.addDirMenu = wx.NewId()
            self.addFileMenu = wx.NewId()
            self.addCharMenu = wx.NewId()
            self.clearMenu = wx.NewId()
        menu = wx.Menu()

        menuAdd = wx.Menu()
        addDirMenu = wx.MenuItem( menuAdd, id=self.addDirMenu, text=u'过滤目录' )
        addFileMenu = wx.MenuItem( menuAdd, id=self.addFileMenu, text=u'过滤文件' )
        addCharMenu = wx.MenuItem( menuAdd, id=self.addCharMenu, text=u'过滤字符' )
        menuAdd.Append( addDirMenu )
        menuAdd.Append( addFileMenu )
        menuAdd.Append( addCharMenu )

        deleteMenu = wx.MenuItem( menu, id=self.deleteMenu, text=u'删除记录' )
        clearMenu = wx.MenuItem( menu, id=self.clearMenu, text=u'清空记录' )

        menu.Append( wx.ID_ANY, u'添加过滤', menuAdd )
        menu.Append( deleteMenu )
        menu.Append( clearMenu )

        self.Bind( wx.EVT_MENU, self.OnAddDir, id=self.addDirMenu )
        self.Bind( wx.EVT_MENU, self.OnAddFile, id=self.addFileMenu )
        self.Bind( wx.EVT_MENU, self.OnAddChar, id=self.addCharMenu )
        self.Bind( wx.EVT_MENU, self.OnDelete, id=self.deleteMenu )
        self.Bind( wx.EVT_MENU, self.OnClear, id=self.clearMenu )
        self.PopupMenu(menu)
        menu.Destroy()
    def OnAddDir( self, event ):
        dialog = wx.TextEntryDialog( wx.GetApp().GetTopWindow(), message=u'添加过滤的目录', caption=u'过滤条件', value='.svn')
        dialog.CenterOnParent()
        ret = dialog.ShowModal()
        if ret == wx.ID_OK:
            self.ctrl_list.Freeze()
            index = self.ctrl_list.GetItemCount()
            self.ctrl_list.InsertItem( index, '', imageIndex=6 )
            self.ctrl_list.SetItem(index, 1, dialog.GetValue() )
            self.ctrl_list.SetItemData( index, 0 )
            self.WriteToShe()
            self.LoadDataLocal()
            self.ctrl_list.Thaw()
    def OnAddChar( self, event ):
        dialog = wx.TextEntryDialog( wx.GetApp().GetTopWindow(), message=u'添加过滤的字符', caption=u'过滤条件', value='.svn')
        dialog.CenterOnParent()
        ret = dialog.ShowModal()
        if ret == wx.ID_OK:
            self.ctrl_list.Freeze()
            index = self.ctrl_list.GetItemCount()
            self.ctrl_list.InsertItem( index, '', imageIndex=7 )
            self.ctrl_list.SetItem(index, 1, dialog.GetValue() )
            self.ctrl_list.SetItemData( index, 2 )
            self.WriteToShe()
            self.LoadDataLocal()
            self.ctrl_list.Thaw()

    def OnAddFile( self, event ):
        dialog = wx.TextEntryDialog( wx.GetApp().GetTopWindow(), message=u'添加过滤的文件', caption=u'过滤条件', value='.svn')
        dialog.CenterOnParent()
        ret = dialog.ShowModal()
        if ret == wx.ID_OK:
            self.ctrl_list.Freeze()
            index = self.ctrl_list.GetItemCount()
            self.ctrl_list.InsertItem( index, '', imageIndex=0 )
            self.ctrl_list.SetItem(index, 1, dialog.GetValue() )
            self.ctrl_list.SetItemData( index, 1 )
            self.WriteToShe()
            self.LoadDataLocal()
            self.ctrl_list.Thaw()

    def OnDelete( self, event ):
        try:
            self.ctrl_list.Freeze()
            #删除过滤条目
            idx = -1
            idxs=[]
            while True:
                idx = self.ctrl_list.GetNextSelected(idx) 
                if idx == -1:
                    break
                idxs.append( idx )
            while idxs:
                dd = idxs.pop()
                self.ctrl_list.DeleteItem( dd )
            self.WriteToShe()
            self.LoadData()
        finally:
            self.ctrl_list.Thaw()

    def OnClear( self, event ):
        #清空过滤条目
        try:
            self.ctrl_list.freeze()
            self.ctrl_list.DeleteAllItems()
            self.WriteToShe()
            self.LoadData()
        finally:
            self.ctrl_list.Thaw()

    def ReadFromShe( self ):
        she = shelve.open(SHE_DB, flag="r" )
        try:
            for data, value in she['filter']:
                index = self.ctrl_list.GetItemCount()
                if data == 0:
                    self.ctrl_list.InsertItem( index, '', imageIndex = 6 )
                elif data == 1:
                    self.ctrl_list.InsertItem( index, '', imageIndex = 0 )
                else:
                    self.ctrl_list.InsertItem( index, '', imageIndex = 7 )
                self.ctrl_list.SetItem( index, 1, str(value) ) 
                self.ctrl_list.SetItemData( index, data )

            #项目记录
            if she.get('projects'):
                for project in she['projects']:
                    self.ctrl_path.getControl("combobox").Append( project )
        finally:
            she.close()

    def WriteToShe( self ):
        she = shelve.open(SHE_DB, writeback=True)
        try:
            she['filter']=self.GetExcludes()
        finally:
            she.close()

    def GetExcludes( self ):
        idx = -1
        excludes = []
        while True:
            idx = self.ctrl_list.GetNextItem( idx, wx.LIST_NEXT_ALL )
            if idx == -1:
                break
            value = self.ctrl_list.GetItemText( idx, 1 )
            data = self.ctrl_list.GetItemData( idx )
            excludes.append((data,value))
        return excludes

    def ReadShe( self, key ):
        she = shelve.open( SHE_DB, flag="r" )
        projects = []
        try:
            projects = she.get(key)
        finally:
            she.close()
        return projects

    def WriteShe( self, key, value ):
        she = shelve.open( SHE_DB, writeback=True )
        try:
            she[key]=value
        finally:
            she.close()

    def OnSlider( self, event ):
        path = self.ctrl_path.getControl("combobox").GetValue()
        self.LoadDataLocal()

    def OnSelectPath( self, event ):
        dialog = wx.DirDialog( parent=wx.GetApp().GetTopWindow(), message=u'选择路径', defaultPath="." )
        dialog.CenterOnParent()
        ret = dialog.ShowModal()
        if ret == wx.ID_OK:
            self.ctrl_path.getControl("combobox").SetValue( dialog.GetPath() )
            self.LoadData( dialog.GetPath() )
            tarPanel = wx.GetApp().GetTopWindow().FindWindowByName("tarPanel")
            tarPanel.EnableAll(True)
            projects = self.ReadShe( "projects" )
            while len(projects) >= 5:
                projects.pop()
            while dialog.GetPath() in projects:
                projects.remove( dialog.GetPath() )
            projects.insert( 0, dialog.GetPath() )
            self.WriteShe( "projects", projects )
        dialog.Destroy()

    def OnChangePath( self, event ):
        path = self.ctrl_path.getControl("combobox").GetValue()
        if path is not None and path != '' and os.path.isdir( path ):
            self.LoadData( path )
            projects = self.ReadShe( "projects" )
            while len(projects) >= 5:
                projects.pop()
            while path in projects:
                projects.remove( path )
            projects.insert( 0, path )
            self.WriteShe( "projects", projects )

    def LoadData( self, path=None ):
        #根据路径重新加载总文件并显示
        if path is None:
            path = self.ctrl_path.getControl("combobox").GetValue()
        if path is None or path == '' or not os.path.isdir( path ):
            wx.MessageBox(u"请设置正确的查找路径!")
            return
        tarPanel = wx.GetApp().GetTopWindow().FindWindowByName("tarPanel")
        tar = wx.GetApp().GetTopWindow().GetCustomTar()
        self.files = []
        if path is None:
            path = os.getcwd()
        excludes = self.GetExcludes()
        for item in tar.find_auto( path, excludes=excludes ):
            self.files.append( item )
        tarPanel.ShowData(self.files)

    def LoadDataLocal( self ):
        #根据总文件和条件过滤显示文件
        tarPanel = wx.GetApp().GetTopWindow().FindWindowByName("tarPanel")
        tar = wx.GetApp().GetTopWindow().GetCustomTar()
        temp_files=[]
        minutes = hours = days = seconds = 0
        days = self.ctrl_days.getControl("slider").GetValue()
        hours = self.ctrl_hours.getControl("slider").GetValue()
        minutes = self.ctrl_minutes.getControl("slider").GetValue()
        seconds = self.ctrl_seconds.getControl("slider").GetValue()
        statusBar = wx.GetApp().GetTopWindow().GetStatusBar()
        info = u'时间轴: '+str(days)+u' 天 ' + str(hours)+u' 时 ' + str(minutes) + u' 分 ' + str(seconds) +u' 秒 '
        statusBar.SetStatusText(info)
        excludes = self.GetExcludes()
        for item in tar.find_filter( self.files, days=days, hours=hours, minutes=minutes, seconds=seconds, excludes=excludes ):
            temp_files.append( item )
        tarPanel.ShowData( temp_files )

class MyFileDropTarget( wx.FileDropTarget ):
    def __init__( self, window ):
        wx.FileDropTarget.__init__( self )
        self.window = window
    def OnDropFiles( self, x, y, filenames ):
        tarPanel = wx.GetApp().GetTopWindow().GetTarPanel()
        operPanel = wx.GetApp().GetTopWindow().GetOperPanel()
        path = operPanel.ctrl_path.getControl("combobox").GetValue()
        if path == '':
            wx.MessageBox(u'需要先设定项目路径!')
            return
        files=[]
        for filename in filenames:
            with open( filename ) as fp:
                files = files + list(set([ x.replace("\\","/").replace("\n","") for x in fp.readlines() ]))
        tarPanel.LoadDataFiles( path, files, filters=True )
        tarPanel.EnableAll(False)
        return True
class TarPanel( wx.Panel ):
    def __init__( self, parent, id=wx.ID_ANY, name='tarPanel' ):
        wx.Panel.__init__( self, parent=parent, id=id, name=name )
        self.imageList = wx.ImageList( 16, 16 )
        for image in images:
            if os.path.exists( image ):
                bmp = wx.Bitmap( image, wx.BITMAP_TYPE_PNG )
                self.imageList.Add( bmp )

        self.ctrl_list = ctrl_list = wx.ListCtrl( self, id=wx.ID_ANY, style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES )
        dt = MyFileDropTarget( self.ctrl_list )
        self.ctrl_list.SetDropTarget( dt )
        ctrl_list.AssignImageList( self.imageList, wx.IMAGE_LIST_SMALL )
        ctrl_list.InsertColumn( 0, u'编号', format=wx.LIST_MASK_TEXT|wx.LIST_FORMAT_CENTER|wx.LIST_MASK_IMAGE, width=80 )
        ctrl_list.InsertColumn( 1, u'文件名', width=280 )
        ctrl_list.InsertColumn( 2, u'文件大小', width=120 )
        ctrl_list.InsertColumn( 3, u'修改日期', width=160 )

        vbox = wx.BoxSizer( wx.VERTICAL )
        vbox.Add( ctrl_list, 1, wx.EXPAND|wx.ALL, 3 )

        self.Bind( wx.EVT_CONTEXT_MENU, self.InitMenu, ctrl_list )

        self.tar = wx.GetApp().GetTopWindow().GetCustomTar()
        self.SetSizer( vbox )
        vbox.Fit( self )

    def InitMenu( self, event ):
        menu = wx.Menu()
        if not hasattr( self, 'impFileMenuId' ):
            self.impFileMenuId = wx.NewId()
            self.expFileMenuId = wx.NewId()
            self.expTarMenuId = wx.NewId()
            self.delFileMenuId = wx.NewId()
            self.clsFileMenuId = wx.NewId()
            self.uploadFileMenuId = wx.NewId()
            self.uploadAllMenuId = wx.NewId()

        impFileMenu = wx.MenuItem( menu, id=self.impFileMenuId, text=u'导入文件清单', helpString=u'支持.txt/.excel/.tar文件导入' )
        expFileMenu = wx.MenuItem( menu, id=self.expFileMenuId, text=u'导出文件清单', helpString=u'导出.txt文件' )
        expTarMenu = wx.MenuItem( menu, id=self.expTarMenuId, text=u'导出Tar包', helpString=u'生成tar包' )
        delFileMenu = wx.MenuItem( menu, id=self.delFileMenuId, text=u'删除记录', helpString=u'删除选定文件，支持多选' )
        clsFileMenu = wx.MenuItem( menu, id=self.clsFileMenuId, text=u'清空记录', helpString=u'清空列表框中的文档清单' )

        uploadFileMenu = wx.MenuItem( menu, id=self.uploadFileMenuId, text=u'上传文件清单', helpString=u'将文件清单上传到服务器' )
        uploadAllMenu = wx.MenuItem( menu, id=self.uploadAllMenuId, text=u'上传文件+', helpString=u'将文件清单上传到服务器' )

        menu.Append( delFileMenu )
        menu.Append( clsFileMenu )
        menu.AppendSeparator()
        menu.Append( impFileMenu )
        menu.Append( expFileMenu )
        menu.Append( expTarMenu )
        menu.AppendSeparator()
        menu.Append( uploadFileMenu )
        menu.Append( uploadAllMenu )

        self.Bind( wx.EVT_MENU, self.OnImportFile, id=self.impFileMenuId )
        self.Bind( wx.EVT_MENU, self.OnExportFile, id=self.expFileMenuId )
        self.Bind( wx.EVT_MENU, self.OnExportTar, id=self.expTarMenuId )
        self.Bind( wx.EVT_MENU, self.OnDeleteFile, id=self.delFileMenuId )
        self.Bind( wx.EVT_MENU, self.OnClearFile, id=self.clsFileMenuId )
        self.Bind( wx.EVT_MENU, self.OnUploadFile, id=self.uploadFileMenuId )
        self.Bind( wx.EVT_MENU, self.OnUploadAll, id=self.uploadAllMenuId )

        self.PopupMenu( menu )
        menu.Destroy()
    def OnUploadFile( self, event ):
        pass
    def OnUploadAll( self, event ):
        pass

    def ShowData( self, files ):
        #根据提供的文件显示到控件
        self.ctrl_list.Freeze()
        self.ctrl_list.DeleteAllItems()
        for fname, fdate, fsize, fstate in files:
            idx=0
            name, ext = os.path.splitext( fname )
            for image in images:
                pext, pname = os.path.splitext(os.path.basename(image))
                if "."+pext == ext:
                    idx = images.index(image)
                    break
            index = self.ctrl_list.GetItemCount()
            self.ctrl_list.InsertItem( index, str(index+1), imageIndex=idx )
            self.ctrl_list.SetItem( index, 1, fname )
            self.ctrl_list.SetItem( index, 2, str(fsize) )
            self.ctrl_list.SetItem( index, 3, fdate )
            self.ctrl_list.SetItemData( index, fstate )
            if fstate is False:
                self.ctrl_list.SetItemTextColour(index, "red")
        self.ctrl_list.Thaw()
    def LoadDataFiles( self, path, files, filters=True ):
        #根据指定路径和文件列表显示文件
        operPanel = wx.GetApp().GetTopWindow().FindWindowById(wx.GetApp().GetTopWindow().GetPanelById())
        tar = wx.GetApp().GetTopWindow().GetCustomTar()
        temp_files = []
        excludes = operPanel.GetExcludes()
        for item in tar.find( path, files, excludes=excludes, filters=filters ):
            temp_files.append( item )

        for oitem in files:
            if oitem not in [ x[0] for x in temp_files ]:
                temp_files.append( (oitem, '-', '-', False) )
        self.ShowData( temp_files )
    def OnImportFile( self, event ):
        #从文件导入清单
        operPanel = wx.GetApp().GetTopWindow().FindWindowById(wx.GetApp().GetTopWindow().GetPanelById())
        dialog = wx.FileDialog( wx.GetApp().GetTopWindow(), message="导入文件清单", \
                wildcard="Text Files(*.txt)|*.txt|Excel Files(*.xls)|*.xls", style=wx.FD_OPEN )
        dialog.CenterOnParent()
        ret = dialog.ShowModal()
        if ret == wx.ID_OK:
            filename = dialog.GetPath()
            path = operPanel.ctrl_path.getControl("combobox").GetValue()
            if path == '' or path is None or os.path.exists( path ) is False:
                wx.MessageBox(u'请指定正确的查找路径!')
                return
            with open( filename ) as fp:
                operPanel.files = list(set([ x.replace("\\","/").replace("\n","") for x in fp.readlines() ]))
                self.LoadDataFiles( path, operPanel.files, filters=False )
            operPanel.ctrl_list.SetFocus
            self.EnableAll( flag = False )
    def EnableAll( self, flag=True ):
        operPanel = wx.GetApp().GetTopWindow().FindWindowById(wx.GetApp().GetTopWindow().GetPanelById())
        operPanel.ctrl_days.Enable(flag)
        operPanel.ctrl_hours.Enable(flag)
        operPanel.ctrl_minutes.Enable(flag)
        operPanel.ctrl_seconds.Enable(flag)
        operPanel.ctrl_list.Enable(flag)

    def OnExportFile( self, event ):
        #导出文件清单
        idx = -1
        dialog = wx.FileDialog( wx.GetApp().GetTopWindow(), message="保存文件清单", \
                wildcard="Text Files(*.txt)|*.txt|Excel Files(*.xls)|*.xls", style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT )
        dialog.CenterOnParent()
        ret = dialog.ShowModal()
        if ret == wx.ID_OK:
            filename = dialog.GetPath()
            if not os.path.splitext(filename)[1]:
                filename = filename +".txt"
            with open( filename, "w" ) as fp:
                while True:
                    idx = self.ctrl_list.GetNextItem( idx )
                    if idx == -1:
                        break
                    val = self.ctrl_list.GetItemText( idx, 1 )
                    fp.write(val+"\n")
            wx.MessageBox(u"导出成功!")
    def OnExportTar( self, event ):
        #导出Tar包
        operPanel = wx.GetApp().GetTopWindow().FindWindowById(wx.GetApp().GetTopWindow().GetPanelById())
        path = operPanel.ctrl_path.getControl("combobox").GetValue()
        if path == '' or path == None or os.path.isdir( path ) is False:
            wx.MessageBox(u"请设置正确的查找路径!")
            return
        tempFiles = []
        notFound = True
        index = -1
        while True:
            index = self.ctrl_list.GetNextItem( index )
            if index == -1:
                break
            notFound = self.ctrl_list.GetItemData( index )
            if notFound is False:
                tempFiles=[]
                break
            val = self.ctrl_list.GetItemText( index, 1 )
            tempFiles.append( val )
        if notFound == False:
            wx.MessageBox(u'请处理未找到文件!')
            return
        idx = -1
        dialog = wx.FileDialog( wx.GetApp().GetTopWindow(), message="导出TAR包", \
                wildcard="TAR Files(*.tar)|*.tar", style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT )
        dialog.CenterOnParent()
        ret = dialog.ShowModal()
        if ret == wx.ID_OK:
            tarFile = dialog.GetPath()
            self.tar.tar( tarFile, path, tempFiles, cutPath=path )
    def OnDeleteFile( self, event ):
        #删除文件
        idx = -1
        idxs=[]
        while True:
            idx = self.ctrl_list.GetNextSelected(idx) 
            if idx == -1:
                break
            idxs.append( idx )
        while idxs:
            dd = idxs.pop()
            self.ctrl_list.DeleteItem( dd )
            self.ctrl_list.Refresh()
        if self.ctrl_list.GetItemCount() == 0:
            operPanel = wx.GetApp().GetTopWindow().FindWindowById(wx.GetApp().GetTopWindow().GetPanelById())
            self.EnableAll()
            operPanel.LoadData()
    def OnClearFile( self, event ):
        #清空文件
        operPanel = wx.GetApp().GetTopWindow().FindWindowById(wx.GetApp().GetTopWindow().GetPanelById())
        self.ctrl_list.DeleteAllItems()
        self.EnableAll()
        operPanel.LoadData()


class DemoFrame( wx.Frame ):
    def __init__( self, parent=None, id=wx.ID_ANY, title=u'tar包管理', size=(800,600), style=None ):
        wx.Frame.__init__( self, parent=parent, id=id, title=title, size=size, style=style )
        self.SetMinSize((800,600))
        self.tar = customTar()

        mainPanel = wx.Panel( self )
        #mainPanel = scrolled.ScrolledPanel( self )
        #mainPanel.SetVirtualSize( 1000, 1000 )
        #mainPanel.SetScrollRate( 20, 20 )

        self.cPanel = cPanel = TarPanel( mainPanel, name='tarPanel' )
        self.rPanel = rPanel = OperPanel( mainPanel, id=wx.NewId(), name='operPanel' )
        self.tPanel = tPanel = InfoPanel( mainPanel, id=wx.NewId(), name='infoPanel' )

        self.mgr = aui.AuiManager()
        self.mgr.SetManagedWindow( mainPanel )
        self.mgr.AddPane( rPanel, aui.AuiPaneInfo().Right().
                Layer(2).
                BestSize((360,-1)).
                MinSize(360,-1).
                Caption(u'控制面板').
                Floatable(True).
                FloatingSize((360,480)).
                CloseButton(False).
                Name(u"包管理工具") )
        self.mgr.AddPane( tPanel, aui.AuiPaneInfo().Top().Name("InfoPanel").
                Layer(2).
                BestSize(-1,60).
                MinSize(-1,60).
                Floatable(False).
                CloseButton(False).
                CaptionVisible(False).
                PaneBorder(False).
                Name(u'信息面板'))
        self.mgr.AddPane( cPanel, aui.AuiPaneInfo().CenterPane().Name("MainPanel") )

        statusBar = self.CreateStatusBar(number=1, id=0 )
        statusBar.SetStatusText(u'欢迎使用本工具')
              
        self.mgr.Update()
        self.mgr.SetAGWFlags( self.mgr.GetAGWFlags()^aui.AUI_MGR_TRANSPARENT_DRAG )
        self.InitMenu()
    def GetCustomTar( self ):
        return self.tar
    def GetOperPanel( self ):
        return self.rPanel
    def GetTarPanel( self ):
        return self.cPanel
    def GetPanelById( self ):
        return self.rPanel.GetId()
    def InitMenu( self ):
        menuBar = wx.MenuBar()
        #系统菜单
        sys_menu = wx.Menu()
        sys_menu_login = wx.MenuItem( sys_menu, id=wx.NewId(), text=u'登录', helpString=u'登录获取更多功能' )
        sys_menu_reg = wx.MenuItem( sys_menu, id=wx.NewId(), text=u'注册', helpString=u'注册用户' )
        sys_menu_logout = wx.MenuItem( sys_menu, id=wx.NewId(), text=u'注销', helpString=u'登出系统' )
        sys_menu.Append( sys_menu_login )
        sys_menu.Append( sys_menu_reg )
        sys_menu.Append( sys_menu_logout )
        menuBar.Append( sys_menu, u'系统' )

        #版本管理
        ver_menu = wx.Menu()
        ver_menu_create = wx.MenuItem( ver_menu, id=wx.NewId(), text=u'创建空包', helpString=u'创建一个空包' )
        ver_menu_modify = wx.MenuItem( ver_menu, id=wx.NewId(), text=u'版本包维护', helpString=u'维护版本包' )
        ver_menu_flist = wx.MenuItem( ver_menu, id=wx.NewId(), text=u'包清单', helpString=u'维护版本包中的文件清单' )
        ver_menu_story = wx.MenuItem( ver_menu, id=wx.NewId(), text=u'包故事', helpString=u'维护版本包中的用户故事' )
        ver_menu.Append( ver_menu_create )
        ver_menu.Append( ver_menu_modify )
        ver_menu.Append( ver_menu_flist )
        ver_menu.Append( ver_menu_story )
        menuBar.Append( ver_menu, u'版本包管理' )

        self.SetMenuBar( menuBar )

        self.Bind( wx.EVT_MENU, self.OnLogin, sys_menu_login )
        self.Bind( wx.EVT_MENU, self.OnReg, sys_menu_reg )
        self.Bind( wx.EVT_MENU, self.OnCreatePack, ver_menu_create )
        self.Bind( wx.EVT_MENU, self.OnModifyPack, ver_menu_modify )
        self.Bind( wx.EVT_MENU, self.OnFileManager, ver_menu_flist )
        self.Bind( wx.EVT_MENU, self.OnStoryManager, ver_menu_story )

    def OnLogin( self, event ):
        dialog = LoginDialog( self )
        dialog.CenterOnParent()
        ret = dialog.ShowModal()
        dialog.Destroy()
    def OnReg( self, event ):
        dialog = RegDialog( self )
        dialog.CenterOnParent()
        ret = dialog.ShowModal()
        if ret == wx.ID_OK:
            wx.MessageBox("Hello, everyone")
        dialog.Destroy()
    def OnCreatePack( self, event ):
        dialog = PackDialog( self, -1 )
        dialog.CenterOnParent()
        ret = dialog.ShowModal()
        if ret == wx.ID_OK:
            wx.MessageBox("Create Dialog")
        dialog.Destroy()
    def OnModifyPack( self, event ):
        pass
    def OnFileManager( self, event ):
        pass
    def OnStoryManager( self, event ):
        pass

if __name__ == '__main__':
    app = wx.App()
    frame = DemoFrame(style=wx.DEFAULT_FRAME_STYLE)
    app.SetTopWindow( frame )
    frame.CenterOnParent()
    frame.Maximize(True)
    frame.Show()
    app.MainLoop()
