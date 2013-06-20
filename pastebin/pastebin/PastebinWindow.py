# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2013 Manish Sharma manish09.iitroorkee@gmail.com
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 2, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import os
from gi.repository import GLib # pylint: disable=E0611

import gettext
from gettext import gettext as _
gettext.textdomain('pastebin')

from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('pastebin')

from pastebin_lib import Window
from pastebin.AboutPastebinDialog import AboutPastebinDialog
from pastebin.PreferencesPastebinDialog import PreferencesPastebinDialog

# See pastebin_lib.Window.py for more details about how this class works
class PastebinWindow(Window):
    __gtype_name__ = "PastebinWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(PastebinWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutPastebinDialog
        self.PreferencesDialog = PreferencesPastebinDialog

        # Code for other initialization actions should be added here.

    def on_button1_clicked(self, widget, data=None):
        print "create button called"
        self.ui.entry1.set_text("")
        buff = self.ui.textview1.get_buffer()
        buff.set_text("")

    def on_button2_clicked(self, widget, data=None):
        #get the title for the note
        title = self.ui.entry1.get_text()
        if title.find(" ") != -1:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK_CANCEL, "Warning on Title")
            dialog.format_secondary_text("Do not place spaces in title")
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                print "WARN dialog closed by clicking OK button"
            elif response == Gtk.ResponseType.CANCEL:
                print "WARN dialog closed by clicking CANCEL button"

            dialog.destroy()

            return

        #get the string
        buff = self.ui.textview1.get_buffer()
        start_iter = buff.get_start_iter()
        end_iter = buff.get_end_iter()
        text = buff.get_text(start_iter, end_iter, True)

        #create the filename
        data_dir = "pastebin/pastebinnotsync"
        filename = os.path.join(data_dir, title)
        filename=filename+".txt"

        #write the data
        GLib.mkdir_with_parents(data_dir, 0o700)
        GLib.file_set_contents(filename, text)
        print "save"            

    def on_button3_clicked(self, widget, data=None):
        print "open button action called"
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print "Open clicked"
            filename=dialog.get_filename()
            filetitle=os.path.basename(filename)
            self.ui.entry1.set_text(filetitle)

            print filename
            text = GLib.file_get_contents(filename)
            buff = self.ui.textview1.get_buffer()
            buff.set_text(text[1])
        elif response == Gtk.ResponseType.CANCEL:
            print "Cancel clicked"

        dialog.destroy()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("Python files")
        filter_py.add_mime_type("text/x-python")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)


