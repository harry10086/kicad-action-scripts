#
#  FillAreaAction.py
#
#  Copyright 2017 JS Reynaud <js.reynaud@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
from __future__ import print_function
import pcbnew
import wx
from . import FillArea
from . import FillAreaDialog
import os

GRID_TYPE_LABEL_TO_VALUE = {
    u"板框边界": FillArea.FillArea.GRID_TYPE_BOARD_BOUNDS,
    u"绝对坐标 (0, 0)": FillArea.FillArea.GRID_TYPE_ABSOLUTE,
    u"网格原点": FillArea.FillArea.GRID_TYPE_GRID_ORIGIN,
}

FILL_TYPE_LABEL_TO_VALUE = {
    u"同心圆": FillArea.FillArea.FILL_TYPE_CONCENTRIC,
    u"轮廓": FillArea.FillArea.FILL_TYPE_OUTLINE,
    u"轮廓 (不含孔)": FillArea.FillArea.FILL_TYPE_OUTLINE_NO_HOLES,
    u"矩形": FillArea.FillArea.FILL_TYPE_RECTANGULAR,
    u"星形": FillArea.FillArea.FILL_TYPE_STAR,
}


def PopulateNets(anet, dlg):
    netnames = list(set([zone.GetNetname() for zone in pcbnew.GetBoard().Zones()]))
    netnames.sort()
    dlg.m_cbNet.Set(netnames)
    if anet is not None:
        index = dlg.m_cbNet.FindString(anet)
        dlg.m_cbNet.Select(index)
#


class FillAreaDialogEx(FillAreaDialog.FillAreaDialog):

    def onDeleteClick(self, event):
        return self.EndModal(wx.ID_DELETE)


class FillAreaAction(pcbnew.ActionPlugin):

    def defaults(self):
        self.name = "过孔缝合生成器"
        self.category = "修改 PCB"
        self.description = "为 PCB 区域生成过孔缝合"
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "./stitching-vias.png")
        self.show_toolbar_button = True

    def Run(self):
        a = FillAreaDialogEx(None)
        # a.m_SizeMM.SetValue("0.8")
        a.m_StepMM.SetValue("2.54")
        # a.m_DrillMM.SetValue("0.3")
        # a.m_Netname.SetValue("GND")
        # a.m_ClearanceMM.SetValue("0.2")
        a.m_bitmapStitching.SetBitmap(wx.Bitmap(os.path.join(os.path.abspath(os.path.dirname(__file__)), "stitching-vias-help.png")))
        self.board = pcbnew.GetBoard()
        self.boardDesignSettings = self.board.GetDesignSettings()
        a.m_SizeMM.SetValue(str(pcbnew.ToMM(self.boardDesignSettings.GetCurrentViaSize())))
        a.m_DrillMM.SetValue(str(pcbnew.ToMM(self.boardDesignSettings.GetCurrentViaDrill())))
        a.m_ClearanceMM.SetValue(str(pcbnew.ToMM(self.boardDesignSettings.GetSmallestClearanceValue())))
        a.SetMinSize(a.GetSize())

        PopulateNets("GND", a)
        modal_result = a.ShowModal()
        if modal_result == wx.ID_OK:
            wx.LogMessage('Via Stitching')
            if 1:  # try:
                fill = FillArea.FillArea()
                fill.SetStepMM(float(a.m_StepMM.GetValue().replace(',', '.')))
                fill.SetSizeMM(float(a.m_SizeMM.GetValue().replace(',', '.')))
                fill.SetDrillMM(float(a.m_DrillMM.GetValue().replace(',', '.')))
                fill.SetClearanceMM(float(a.m_ClearanceMM.GetValue().replace(',', '.')))
                # fill.SetNetname(a.m_Netname.GetValue())
                netname = a.m_cbNet.GetStringSelection()
                fill.SetNetname(netname)
                if a.m_Debug.IsChecked():
                    fill.SetDebug()
                fill.SetRandom(a.m_Random.IsChecked())
                fill.SetViaThroughAreas(a.m_viaThroughAreas.IsChecked())
                fill.SetGridType(GRID_TYPE_LABEL_TO_VALUE.get(a.m_cbGridType.GetStringSelection(), FillArea.FillArea.GRID_TYPE_BOARD_BOUNDS))
                fill.SetFillType(FILL_TYPE_LABEL_TO_VALUE.get(a.m_cbFillType.GetStringSelection(), FillArea.FillArea.FILL_TYPE_RECTANGULAR))
                fill.SetSameNetTracks(a.m_sameNetTracks.IsChecked())
                if a.m_only_selected.IsChecked():
                    fill.OnlyOnSelectedArea()
                fill.Run()
            else:  # except Exception:
                wx.MessageDialog(None, "Invalid parameter")
        elif modal_result == wx.ID_DELETE:
            if 1:  # try:
                fill = FillArea.FillArea()
                fill.SetNetname(a.m_cbNet.GetStringSelection())  # a.m_Netname.GetValue())
                if a.m_Debug.IsChecked():
                    fill.SetDebug()
                fill.DeleteVias()
                fill.Run()
            else:  # except Exception:
                wx.MessageDialog(None, "Invalid parameter for delete")
        else:
            print("Cancel")
        a.Destroy()


FillAreaAction().register()
