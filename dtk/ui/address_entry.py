#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2013 Deepin, Inc.
#               2013 Zhai Xiang
# 
# Author:     Zhai Xiang <zhaixiang@linuxdeepin.com>
# Maintainer: Zhai Xiang <zhaixiang@linuxdeepin.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from theme import ui_theme
from utils import (color_hex_to_cairo, alpha_color_hex_to_cairo, 
                   cairo_disable_antialias, cairo_state, get_content_size)
from draw import draw_text
import gobject
import gtk
import pango

class IpAddressEntry(gtk.VBox):
    def __init__(self, address = "",  width = 120, height = 22, token = "."):
        gtk.VBox.__init__(self)

        self.address = address

        self.set_size_request(width, height)
        self.token = token

        self.connect("expose-event", self.__on_expose)

    def set_address(self, address):
        self.address = address
        self.queue_draw()

    def set_token(self, token):
        self.token = token
        self.queue_draw()

    def __on_expose(self, widget, event):
        cr = widget.window.cairo_create()                                       
        rect = widget.allocation 
        x, y, w, h = rect.x, rect.y, rect.width, rect.height
        token_spacing = 10
        ip_addr = []
        if self.address != "":
            ip_addr = [t for t in self.address.split(self.token)]
        '''
        ipv4 max value is 255
        '''
        ipv4_max = 255
        '''
        but what about ipv6?
        '''
        ipv6_max = "ffff"
        ip_addr_len = len(ip_addr)
        i = 0
        
        '''
        check Ip Address format validate, it is better to use regex, but regex is too heavy...
        '''
        if self.token != "." and self.token != ":" and ip_addr_len != 0 and ip_addr_len != 4 and ip_addr_len != 6:
            print "Ip Address format is wrong!"
            return

        '''
        draw background
        '''
        with cairo_disable_antialias(cr):                                           
            cr.set_line_width(1)                                                    
            cr.set_source_rgb(*color_hex_to_cairo(
                ui_theme.get_color("combo_entry_frame").get_color()))
            cr.rectangle(x, y, w, h)                   
            cr.stroke()                                                             
                                                                                
            cr.set_source_rgba(*alpha_color_hex_to_cairo(
                (ui_theme.get_color("combo_entry_background").get_color(), 0.9)))            
            cr.rectangle(x, y, w - 1, h - 1)       
            cr.fill()        
        
        '''
        draw ip address and token
        '''
        ip_max_width, ip_max_height = get_content_size(str(ipv4_max))
        if ip_addr_len == 6:
            ip_max_width, ip_max_height = get_content_size(ipv6_max)
        while i < ip_addr_len:
            draw_text(cr, 
                      ip_addr[i], 
                      x + i * (ip_max_width + token_spacing), 
                      y, 
                      ip_max_width, 
                      h, 
                      alignment = pango.ALIGN_RIGHT)
            
            if i != ip_addr_len - 1:
                draw_text(cr, 
                          self.token, 
                          x + (i + 1) * ip_max_width + i * token_spacing, 
                          y, 
                          token_spacing, 
                          h, 
                          alignment = pango.ALIGN_CENTER)
            
            i += 1
