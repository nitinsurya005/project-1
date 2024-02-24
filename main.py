# from biller import *
# from converter import *
from docx import *
from PIL import ImageTk, Image
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.shared import Pt
from docx2pdf import convert
import os
from sqlite3 import *
# import threading
from datetime import *
from time import strftime
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label as Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
from datetime import datetime
from kivy.graphics import Color, Rectangle, Line
import sys


class num2word:
    def __init__(self, number):
        self.ones = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
        self.teens = ['Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen',
                      'Nineteen']
        self.tens = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
        self.word = self.convert_to_currency(number) + ' Rupees Only'

    def convert_less_than_thousand(self, num):
        if num == 0:
            return ''
        elif num < 10:
            return self.ones[num]
        elif num < 20:
            return self.teens[num - 10]
        elif num < 100:
            return self.tens[num // 10] + ' ' + self.convert_less_than_thousand(num % 10)
        else:
            return self.ones[num // 100] + ' Hundred ' + self.convert_less_than_thousand(num % 100)

    def convert_to_currency(self, num):
        if num == 0: return 'Zero'
        result = ''
        crore = num // 10000000
        lakh = (num // 100000) % 100
        thousand = (num // 1000) % 100
        rest = num % 1000

        if crore: result += self.convert_less_than_thousand(crore) + ' Crore '
        if lakh: result += self.convert_less_than_thousand(lakh) + ' Lakh '
        if thousand: result += self.convert_less_than_thousand(thousand) + ' Thousand '
        if rest: result += self.convert_less_than_thousand(rest)

        return result.strip()


class StringVar:
    def __init__(self, initial_value=''):
        self._value = initial_value
        self._callbacks = []

    def get(self):
        return self._value

    def set(self, value):
        try:
            value = str(value)
        except:
            raise TypeError
        self._value = value
        self._notify_callbacks()

    def trace(self, callback):
        self._callbacks.append(callback)

    def _notify_callbacks(self):
        for callback in self._callbacks:
            callback()


class IntVar:
    def __init__(self, initial_value=0):
        self._value = initial_value
        self._callbacks = []

    def get(self):
        return self._value

    def set(self, value):
        try:
            value = int(value)
        except:
            raise TypeError
        self._value = value
        self._notify_callbacks()

    def trace(self, callback):
        self._callbacks.append(callback)

    def _notify_callbacks(self):
        for callback in self._callbacks:
            callback()


class Variable:
    def __init__(self, initial_value=''):
        self._value = initial_value
        self._callbacks = {}
        self.i = 0

    def get(self):
        return self._value

    def set(self, value):
        self._value = value
        self._notify_callbacks()

    def trace(self, callback):
        self._callbacks[self.i] = callback
        self.i += 1
        return self.i - 1

    def trace_remove(self, id):
        l = self._callbacks.items()
        self._callbacks = {}
        for i, j in l:
            if i != id: self._callbacks[i] = j

    def _notify_callbacks(self):
        for callback in self._callbacks.values():
            callback()


class MyFloatLayout(FloatLayout):
    def __init__(self, bg='#000000', **kwargs):
        super(MyFloatLayout, self).__init__(**kwargs)
        bg = bg.lower()[1:]
        rr = [bg[0], bg[1]]
        gg = [bg[2], bg[3]]
        bb = [bg[4], bg[5]]
        r = g = b = 0
        d = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12,
             'd': 13, 'e': 14, 'f': 15}
        for i, j in zip(rr, [16, 1]): r += d[i] * j
        for i, j in zip(gg, [16, 1]): g += d[i] * j
        for i, j in zip(bb, [16, 1]): b += d[i] * j
        r /= 255
        g /= 255
        b /= 255
        with self.canvas.before:
            Color(r, g, b, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class MyGridLayout(GridLayout):
    def __init__(self, bg='#000000', **kwargs):
        super(MyGridLayout, self).__init__(**kwargs)
        bg = bg.lower()[1:]
        rr = [bg[0], bg[1]]
        gg = [bg[2], bg[3]]
        bb = [bg[4], bg[5]]
        r = g = b = 0
        d = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12,
             'd': 13, 'e': 14, 'f': 15}
        for i, j in zip(rr, [16, 1]): r += d[i] * j
        for i, j in zip(gg, [16, 1]): g += d[i] * j
        for i, j in zip(bb, [16, 1]): b += d[i] * j
        r /= 255
        g /= 255
        b /= 255
        with self.canvas.before:
            Color(r, g, b, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class MyBoxLayout(BoxLayout):
    def __init__(self, bg='#000000', **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)
        bg = bg.lower()[1:]
        rr = [bg[0], bg[1]]
        gg = [bg[2], bg[3]]
        bb = [bg[4], bg[5]]
        r = g = b = 0
        d = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12,
             'd': 13, 'e': 14, 'f': 15}
        for i, j in zip(rr, [16, 1]): r += d[i] * j
        for i, j in zip(gg, [16, 1]): g += d[i] * j
        for i, j in zip(bb, [16, 1]): b += d[i] * j
        r /= 255
        g /= 255
        b /= 255
        with self.canvas.before:
            Color(r, g, b, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class Table1(ScrollView):
    def __init__(self, bg='#000000', cols=1, **kwargs):
        super(Table1, self).__init__(**kwargs)
        self.tbl = MyGridLayout(bg=bg, cols=cols, size_hint_y=None)
        self.tbl.bind(minimum_height=self.tbl.setter('height'))
        self.add_widget(self.tbl)
        self.cols = cols


class Table(MyBoxLayout):
    def __init__(self, bg1='#000000', bg2=1, bg3=1, cols=1, **kwargs):
        if bg2 == 1: bg2 = bg1
        if bg3 == 1: bg3 = bg1
        self.cols = cols
        super(Table, self).__init__(bg=bg1, orientation='vertical', **kwargs)
        self.h = MyGridLayout(bg=bg2, cols=cols, size_hint_y=None)
        self.h.bind(minimum_height=self.h.setter('height'))
        self.add_widget(self.h)
        self.t = Table1(bg3, cols)
        self.add_widget(self.t)
        self.tbl = self.t.tbl


class MyTextInput(TextInput):
    def __init__(self, textvariable='', bg='#000000', fg='#ffffff', **kwargs):
        bg = bg.lower()[1:]
        rr = [bg[0], bg[1]]
        gg = [bg[2], bg[3]]
        bb = [bg[4], bg[5]]
        r = g = b = 0
        d = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12,
             'd': 13, 'e': 14, 'f': 15}
        for i, j in zip(rr, [16, 1]): r += d[i] * j
        for i, j in zip(gg, [16, 1]): g += d[i] * j
        for i, j in zip(bb, [16, 1]): b += d[i] * j
        r /= 255
        g /= 255
        b /= 255
        bgc = (r, g, b, 1)
        fg = fg.lower()[1:]
        rr = [fg[0], fg[1]]
        gg = [fg[2], fg[3]]
        bb = [fg[4], fg[5]]
        r = g = b = 0
        d = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12,
             'd': 13, 'e': 14, 'f': 15}
        for i, j in zip(rr, [16, 1]): r += d[i] * j
        for i, j in zip(gg, [16, 1]): g += d[i] * j
        for i, j in zip(bb, [16, 1]): b += d[i] * j
        r /= 255
        g /= 255
        b /= 255
        fgc = (r, g, b, 1)
        super(MyTextInput, self).__init__(background_color=bgc, foreground_color=fgc, **kwargs)

        def on_text_change(instance, value):
            textvariable.set(str(value))

        def set_text():
            self.text = str(textvariable.get())

        if textvariable != '':
            textvariable.trace(set_text)
            self.bind(text=on_text_change)


class MyCheckBox(CheckBox):
    def __init__(self, variable='', **kwargs):
        super(MyCheckBox, self).__init__(**kwargs)

        def fun(checkbox, value): variable.set(value)

        def set_fun(): self.active = variable.get()

        if variable != '':
            variable.trace(set_fun)
            self.bind(active=fun)


class MyButton(Button):
    def __init__(self, bg='#ffffff', fg='#000000', **kwargs):
        bg = bg.lower()[1:]
        rr = [bg[0], bg[1]]
        gg = [bg[2], bg[3]]
        bb = [bg[4], bg[5]]
        r = g = b = 0
        d = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12,
             'd': 13, 'e': 14, 'f': 15}
        for i, j in zip(rr, [16, 1]): r += d[i] * j
        for i, j in zip(gg, [16, 1]): g += d[i] * j
        for i, j in zip(bb, [16, 1]): b += d[i] * j
        r /= 255
        g /= 255
        b /= 255
        bgc = (r, g, b, 1)
        fg = fg.lower()[1:]
        rr = [fg[0], fg[1]]
        gg = [fg[2], fg[3]]
        bb = [fg[4], fg[5]]
        r = g = b = 0
        d = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12,
             'd': 13, 'e': 14, 'f': 15}
        for i, j in zip(rr, [16, 1]): r += d[i] * j
        for i, j in zip(gg, [16, 1]): g += d[i] * j
        for i, j in zip(bb, [16, 1]): b += d[i] * j
        r /= 255
        g /= 255
        b /= 255
        fgc = (r, g, b, 1)
        super().__init__(background_color=bgc, color=fgc, **kwargs)


class MyLabel(Label):
    def __init__(self, textvariable='', text='', style='', fun='', id='', bg='#000000', fg='#000000', **kwargs):
        super(MyLabel, self).__init__(**kwargs, markup=1)

        def set_text():
            self.text = f"{style}{str(textvariable.get())}"
            self.fgch()

        if text != '': self.text = text
        if textvariable != '':
            self.text = str(textvariable.get())
            textvariable.trace(set_text)
        else:
            self.text = text
        self.fun = fun
        self.style = style
        self.id = id
        self.bg = bg
        self.fg = fg
        self.bgch()
        self.fgch()

    def fgch(self):
        if 'color=' in self.text:
            i = self.text.index('[color=')
            self.text = self.text[:i] + self.text[i + 15:]
        self.text = f'[color={self.fg}]{self.style}{self.text}'

    def bgch(self):
        bg = self.bg.lower()[1:]
        rr = [bg[0], bg[1]]
        gg = [bg[2], bg[3]]
        bb = [bg[4], bg[5]]
        r = g = b = 0
        d = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12,
             'd': 13, 'e': 14, 'f': 15}
        for i, j in zip(rr, [16, 1]): r += d[i] * j
        for i, j in zip(gg, [16, 1]): g += d[i] * j
        for i, j in zip(bb, [16, 1]): b += d[i] * j
        r /= 255
        g /= 255
        b /= 255
        with self.canvas.before:
            self.canvas.before.clear()
            Color(r, g, b, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.fun != '':
                self.fun(self)
            return True
        return super().on_touch_down(touch)


class MyApp(App):
    def build(self):
        self.o = os.getcwd()
        if '/' in self.o and '\\' in self.o:
            x = self.o
            a = ''
            for i in range(len(x)):
                if x[i] != '\\':
                    a += x[i]
                else:
                    a += '/'
            self.o = a
        self.db = self.o.rstrip('\Files') + '\\Files\\addbook.db'
        if '/' in self.db and '\\' in self.db:
            x = self.db
            a = ''
            for i in range(len(x)):
                if x[i] != '\\':
                    a += x[i]
                else:
                    a += '/'
            self.db = a
        self.add = Variable()
        self.gstin = Variable()
        self.stnam = Variable()
        self.stcod = Variable()
        self.invno = Variable()
        self.date = Variable()
        self.delnote = Variable()
        self.mot = Variable()
        self.bon = Variable()
        self.bdate = Variable()
        self.ddno = Variable()
        self.dndate = Variable()
        self.dispthr = Variable()
        self.dest = Variable()
        self.bol = Variable()
        self.vno = Variable()
        self.sba = IntVar()
        self.sbat = Variable()
        self.traces = []
        self.shipadd = Variable()
        self.shipad = Variable()
        self.sgstin = Variable()
        self.sstnam = Variable()
        self.sstcod = Variable()
        self.billadd = Variable()
        self.billad = Variable()
        self.bgstin = Variable()
        self.bstnam = Variable()
        self.bstcod = Variable()
        self.tod = Variable()
        self.sno = Variable()
        self.item = Variable()
        self.hsn = Variable()
        self.qty = Variable()
        self.rate = Variable()
        self.uom = Variable()
        self.amt = Variable()
        self.sno1 = Variable()
        self.item1 = Variable()
        self.hsn1 = Variable()
        self.qty1 = Variable()
        self.rate1 = Variable()
        self.uom1 = Variable()
        self.amt1 = Variable()
        self.sno2 = Variable()
        self.item2 = Variable()
        self.hsn2 = Variable()
        self.qty2 = Variable()
        self.rate2 = Variable()
        self.uom2 = Variable()
        self.amt2 = Variable()
        self.sno3 = Variable()
        self.item3 = Variable()
        self.hsn3 = Variable()
        self.qty3 = Variable()
        self.rate3 = Variable()
        self.uom3 = Variable()
        self.amt3 = Variable()
        self.sno4 = Variable()
        self.item4 = Variable()
        self.hsn4 = Variable()
        self.qty4 = Variable()
        self.rate4 = Variable()
        self.uom4 = Variable()
        self.amt4 = Variable()
        self.sno5 = Variable()
        self.item5 = Variable()
        self.hsn5 = Variable()
        self.qty5 = Variable()
        self.rate5 = Variable()
        self.uom5 = Variable()
        self.amt5 = Variable()
        self.amt6 = Variable()
        self.amtw = Variable()
        self.tamt = Variable()
        self.cgstp = Variable()
        self.cgst = Variable()
        self.sgstp = Variable()
        self.sgst = Variable()
        self.igstp = Variable()
        self.igst = Variable()
        self.invt = Variable()

        self.vl = [self.invno, self.date, self.delnote, self.mot, self.bon, self.bdate, self.ddno, self.dndate,
                   self.dispthr, self.dest, self.bol, self.vno, self.sgstin, self.shipadd, self.sstnam, self.sstcod,
                   self.billadd, self.bgstin, self.bstnam, self.bstcod, self.tod, self.sno, self.item, self.hsn,
                   self.qty, self.rate, self.uom, self.amt, self.sno1, self.item1, self.hsn1, self.qty1, self.rate1,
                   self.uom1, self.amt1, self.sno2, self.item2, self.hsn2, self.qty2, self.rate2, self.uom2, self.amt2,
                   self.sno3, self.item3, self.hsn3, self.qty3, self.rate3, self.uom3, self.amt3, self.sno4, self.item4,
                   self.hsn4, self.qty4, self.rate4, self.uom4, self.amt4, self.sno5, self.item5, self.hsn5, self.qty5,
                   self.rate5, self.uom5, self.amt5, self.amt6, self.amtw, self.tamt, self.cgstp, self.cgst, self.sgstp,
                   self.sgst, self.igstp, self.igst, self.invt]
        self.tvl = {'self.invno': self.invno, 'self.date': self.date, 'self.delnote': self.delnote,
                    'self.mot': self.mot, 'self.bon': self.bon, 'self.bdate': self.bdate, 'self.shipadd': self.shipadd,
                    'self.billadd': self.billadd, 'self.ddno': self.ddno, 'self.dndate': self.dndate,
                    'self.dispthr': self.dispthr, 'self.dest': self.dest, 'self.bol': self.bol, 'self.vno': self.vno,
                    'self.sgstin': self.sgstin, 'self.sstnam': self.sstnam, 'self.sstcod': self.sstcod,
                    'self.bgstin': self.bgstin, 'self.bstnam': self.bstnam, 'self.bstcod': self.bstcod,
                    'self.tod': self.tod, 'self.sno': self.sno, 'self.item': self.item, 'self.hsn': self.hsn,
                    'self.qty': self.qty, 'self.rate': self.rate, 'self.uom': self.uom, 'self.amt': self.amt,
                    'self.sno1': self.sno1, 'self.item1': self.item1, 'self.hsn1': self.hsn1, 'self.qty1': self.qty1,
                    'self.rate1': self.rate1, 'self.uom1': self.uom1, 'self.amt1': self.amt1, 'self.sno2': self.sno2,
                    'self.item2': self.item2, 'self.hsn2': self.hsn2, 'self.qty2': self.qty2, 'self.rate2': self.rate2,
                    'self.uom2': self.uom2, 'self.amt2': self.amt2, 'self.sno3': self.sno3, 'self.item3': self.item3,
                    'self.hsn3': self.hsn3, 'self.qty3': self.qty3, 'self.rate3': self.rate3, 'self.uom3': self.uom3,
                    'self.amt3': self.amt3, 'self.sno4': self.sno4, 'self.item4': self.item4, 'self.hsn4': self.hsn4,
                    'self.qty4': self.qty4, 'self.rate4': self.rate4, 'self.uom4': self.uom4, 'self.amt4': self.amt4,
                    'self.sno5': self.sno5, 'self.item5': self.item5, 'self.hsn5': self.hsn5, 'self.qty5': self.qty5,
                    'self.rate5': self.rate5, 'self.uom5': self.uom5, 'self.amt5': self.amt5, 'self.amt6': self.amt6,
                    'self.amtw': self.amtw, 'self.tamt': self.tamt, 'self.cgstp': self.cgstp, 'self.cgst': self.cgst,
                    'self.sgstp': self.sgstp, 'self.sgst': self.sgst, 'self.igstp': self.igstp, 'self.igst': self.igst,
                    'self.invt': self.invt}
        for i in self.tvl.keys():
            if i in ['self.sba', 'self.shipadd', 'self.sgstin', 'self.sstnam', 'self.sstcod', 'self.billadd',
                     'self.bgstin', 'self.bstnam', 'self.bstcod', 'self.sno1', 'self.item1', 'self.hsn1', 'self.uom1',
                     'self.amt1', 'self.sno2', 'self.item2', 'self.hsn2', 'self.uom2', 'self.amt2', 'self.sno3',
                     'self.item3', 'self.hsn3', 'self.uom3', 'self.amt3', 'self.sno4', 'self.item4', 'self.hsn4',
                     'self.uom4', 'self.amt4', 'self.sno5', 'self.item5', 'self.hsn5', 'self.uom5', 'self.amt5',
                     'self.qty1', 'self.rate1', 'self.qty2', 'self.rate2', 'self.qty3', 'self.rate3', 'self.qty4',
                     'self.rate4', 'self.qty5', 'self.rate5', 'self.cgstp', 'self.sgstp', 'self.igstp']:
                var = self.tvl[i]
                var.trace(self.fun(i))
        self.sba.trace(self.sba_fun)
        self.sba.set(0)

        for i, j in zip([[self.shipadd, self.sgstin, self.sstnam, self.sstcod],
                         [self.billadd, self.bgstin, self.bstnam, self.bstcod]], [self.sba_funs, self.sba_funb]):
            for k in i: self.traces.append(k.trace(j))

        for i in range(1, 6):
            self.tvl[f"self.sno{i}"].set(str(i) + '.')

        self.fts = 20

        def time(n=1):
            dt = datetime.now()
            x = str(dt).split(' ')
            d = x[0]
            p = d.split('-')
            d = p[2] + '/'
            d += p[1]
            d += '/'
            d += p[0]
            self.dtv.set(d)
            string = strftime('%I:%M:%S %p')
            self.tmv.set(string)
            for i in [mark, datl]: i.fgch()

        self.shy = [0, 0.0285627450980392, 0.0285627450980392, 0.0285627450980392, 0.03501764705882353,
                    0.008019607843137254, 0.02552941176470589, 0.015084313725490195]
        for i in range(len(self.shy)): self.shy[i] += 0.015031372549019608 / (len(self.shy) - 1)
        master = MyGridLayout(cols=1, padding=25)
        x = 0.65 if sys.platform != 'win32' else 0.8
        y = 0.1
        h = MyFloatLayout(bg='#feff06', size_hint=(1, y))
        h.add_widget(
            Label(font_size=self.fts + 35, text='[color=#6a006a][b]SRT TRADER BILLING SYSTEM[/b][/color]', markup=True,
                  size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.75}))
        h.add_widget(Label(font_size=self.fts + 35, text='[color=#6a006a][b]TAX INVOICE[/b][/color]', markup=True,
                           size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.25}))
        fg = '#ff2222'
        bg = '#aaaaff'
        dtf = MyBoxLayout(bg=bg, orientation='vertical', size_hint=(0.2, 0.5), pos_hint={'x': 0, 'y': 0})
        h.add_widget(dtf)
        self.dtv, self.tmv = Variable(), Variable()
        datl = MyLabel(font_size=self.fts + 10, text='Date', textvariable=self.dtv, style='[b]', bg=bg, fg=fg,
                       size_hint=(1, 1 / 2), pos_hint={'x': 0, 'y': 0, 'center_x': 0.5, 'center_y': 0.25})
        mark = MyLabel(font_size=self.fts + 10, text='Time', textvariable=self.tmv, style='[b]', bg=bg, fg=fg,
                       size_hint=(1, 1 / 2), pos_hint={'center_x': 0.5, 'center_y': 0.75})
        for i in [mark, datl]: i.fgch()
        dtf.add_widget(datl)
        dtf.add_widget(mark)
        Clock.schedule_interval(time, 1)
        master.add_widget(h)

        self.bg1 = '#242323'
        self.bg2 = '#4d1d31'
        self.fg2 = '#f26c95'
        self.bg3 = '#003341'
        self.fg3 = '#68e0ff'
        self.bg4 = '#123d15'
        self.fg4 = '#78c57e'

        details = MyBoxLayout(bg=self.bg1, orientation='vertical', size_hint_y=x)

        row1 = MyGridLayout(bg=self.bg1, cols=3, size_hint=(1, self.shy[1]))
        l = Label(font_size=self.fts + 4,
                  text=f'[color={self.fg3}][b][size={self.fts + 15}]SRT TRADER[/b][/size]\nNo.45-A, PUDUPALAYAM,\nKAMARAJ NAGAR,\nMUTHUR. 63805\nGSTIN/UIN     : 33AJIPT8805B1Z9\nSTATE NAME : TAMIL NADU, CODE : 33',
                  halign='left', valign='middle', markup=True, height=210,
                  size_hint=(0.41437908496732026143790849673203, None))
        l.bind(size=l.setter('text_size'))
        row1.add_widget(l)

        row11 = MyBoxLayout(bg=self.bg1, orientation='vertical', size_hint=(0.29281045751633986928104575163399, 1))
        for i, j in zip(['Invoice No.', 'Delivery Note', 'Buyer\'s Order No.'], [self.invno, self.delnote, self.bon]):
            l = Label(font_size=self.fts + 3, text=f"[b][color={self.fg2}]{i}[/color]", markup=1, halign='left',
                      valign='middle', height=40, size_hint=(1, None))
            l.bind(size=l.setter('text_size'))
            row11.add_widget(l)
            row11.add_widget(MyTextInput(bg=self.bg2, fg=self.fg2, textvariable=j, font_size=self.fts + 3, hint_text=i,
                                         multiline=False, height=40, size_hint=(1, None)))

        row12 = MyBoxLayout(bg=self.bg1, orientation='vertical', size_hint=(0.29281045751633986928104575163399, 1))
        for i, j in zip(['Date', 'Mode/Terms of Payment', 'Date'], [self.date, self.mot, self.bdate]):
            l = Label(font_size=self.fts + 3, text=f"[b][color={self.fg2}]{i}[/color]", markup=1, halign='left',
                      valign='middle', height=40, size_hint=(1, None))
            l.bind(size=l.setter('text_size'))
            row12.add_widget(l)
            row12.add_widget(MyTextInput(bg=self.bg2, fg=self.fg2, textvariable=j, font_size=self.fts + 3, hint_text=i,
                                         multiline=False, height=40, size_hint=(1, None)))
        row1.add_widget(row11)
        row1.add_widget(row12)

        row2 = MyGridLayout(bg=self.bg1, cols=3, size_hint=(1, self.shy[2]))

        row21 = MyBoxLayout(bg=self.bg1, orientation='vertical', height=210,
                            size_hint=(0.41437908496732026143790849673203, 1))
        l = Label(font_size=self.fts + 5, markup=1, text=f'[color={self.fg3}][b]Consignee (Ship to)[b]', height=30,
                  size_hint=(1, None))
        l.bind(size=l.setter('text_size'))
        row21.add_widget(l)
        row21.add_widget(MyTextInput(bg=self.bg3, fg=self.fg3, textvariable=self.shipadd, font_size=self.fts + 3,
                                     hint_text='Shipping Address', height=120, multiline=True, size_hint=(1, None)))

        row211 = MyGridLayout(bg=self.bg1, cols=2, height=40, size_hint=(1, None))
        row211.add_widget(
            Label(font_size=self.fts + 3, markup=1, text=f'[color={self.fg3}]GSTIN/UIN       :', width=170,
                  size_hint=(None, 1 / 2)))
        row211.add_widget(MyTextInput(bg=self.bg3, fg=self.fg3, textvariable=self.sgstin, font_size=self.fts + 3,
                                      hint_text='GSTIN/UIN', height=40, size_hint=(1, None), multiline=False))
        row212 = MyGridLayout(bg=self.bg1, cols=4, height=40, size_hint=(1, None))
        row212.add_widget(
            Label(font_size=self.fts + 3, markup=1, text=f'[color={self.fg3}]State Name      :', width=170,
                  size_hint=(None, 1)))
        row212.add_widget(MyTextInput(bg=self.bg3, fg=self.fg3, textvariable=self.sstnam, font_size=self.fts + 3,
                                      hint_text='State Name', height=40, size_hint=(1, None), multiline=False))
        row212.add_widget(
            Label(font_size=self.fts + 3, markup=1, text=f'[color={self.fg3}]Code :', width=70, size_hint=(None, 1)))
        row212.add_widget(
            MyTextInput(bg=self.bg3, fg=self.fg3, textvariable=self.sstcod, font_size=self.fts + 3, hint_text='Cde',
                        height=40, width=50, size_hint=(None, None), multiline=False))
        row21.add_widget(row211)
        row21.add_widget(row212)

        row22 = MyBoxLayout(bg=self.bg1, orientation='vertical', height=210,
                            size_hint=(0.29281045751633986928104575163399, None))
        for i, j in zip(['Dispatch Doc No.', 'Dispatched Through', 'Bill of Landing/LR-RR No.'],
                        [self.ddno, self.dispthr, self.bol]):
            l = Label(font_size=self.fts + 3, text=f"[b][color={self.fg2}]{i}[/color]", markup=1, halign='left',
                      valign='middle', height=40, size_hint=(1, None))
            l.bind(size=l.setter('text_size'))
            row22.add_widget(l)
            row22.add_widget(MyTextInput(bg=self.bg2, fg=self.fg2, textvariable=j, font_size=self.fts + 3, hint_text=i,
                                         multiline=False, height=40, size_hint=(1, None)))

        row23 = MyBoxLayout(bg=self.bg1, orientation='vertical', height=210,
                            size_hint=(0.29281045751633986928104575163399, None))
        for i, j in zip(['Delivery Note Date', 'Destination', 'Motor Vehicle No.'], [self.dndate, self.dest, self.vno]):
            l = Label(font_size=self.fts + 3, text=f"[b][color={self.fg2}]{i}[/color]", markup=1, halign='left',
                      valign='middle', height=40, size_hint=(1, None))
            l.bind(size=l.setter('text_size'))
            row23.add_widget(l)
            row23.add_widget(MyTextInput(bg=self.bg2, fg=self.fg2, textvariable=j, font_size=self.fts + 3, hint_text=i,
                                         multiline=False, height=40, size_hint=(1, None)))
        row2.add_widget(row21)
        row2.add_widget(row22)
        row2.add_widget(row23)

        row3 = MyGridLayout(bg=self.bg1, cols=2, size_hint=(1, self.shy[3]))

        row31 = MyBoxLayout(bg=self.bg1, orientation='vertical', height=210,
                            size_hint=(0.41437908496732026143790849673203, 1))
        row311 = MyBoxLayout(bg=self.bg1, orientation='horizontal', height=30, size_hint=(1, None))
        l = Label(font_size=self.fts + 5, text=f'[color={self.fg3}][b]Buyer (Bill to)[b][/color]', markup=True,
                  size_hint=(0.4085365853658536585365853658537, 1))
        l.bind(size=l.setter('text_size'))
        row311.add_widget(l)

        def fun(name=1):
            self.sba.set(not self.sba.get())

        row311.add_widget(MyLabel(font_size=self.fts + 5, halign='right', valign='middle', text='[b]Same as Above[/b]',
                                  textvariable=self.sbat, bg=self.bg1, fg=self.fg3, fun=fun,
                                  size_hint=(0.40536585365853658536585365853659, 1)))
        # row311.add_widget(MyLabel(textvariable=self.sbat,bg=self.bg1,fg=self.fg3,size_hint=(0.14878048780487804878048780487805,1)))
        row31.add_widget(row311)
        row31.add_widget(MyTextInput(bg=self.bg3, fg=self.fg3, textvariable=self.billadd, font_size=self.fts + 3,
                                     hint_text='Billing Address', height=120, multiline=True, size_hint=(1, None)))
        row312 = MyGridLayout(bg=self.bg1, cols=2, height=40, size_hint=(1, None))
        row312.add_widget(
            Label(font_size=self.fts + 3, markup=1, text=f'[color={self.fg3}]GSTIN/UIN       :', width=170,
                  size_hint=(None, 1 / 2)))
        row312.add_widget(MyTextInput(bg=self.bg3, fg=self.fg3, textvariable=self.bgstin, font_size=self.fts + 3,
                                      hint_text='GSTIN/UIN', height=40, size_hint=(1, None), multiline=False))
        row313 = MyGridLayout(bg=self.bg1, cols=4, height=40, size_hint=(1, None))
        row313.add_widget(
            Label(font_size=self.fts + 3, markup=1, text=f'[color={self.fg3}]State Name      :', width=170,
                  size_hint=(None, 1)))
        row313.add_widget(MyTextInput(bg=self.bg3, fg=self.fg3, textvariable=self.bstnam, font_size=self.fts + 3,
                                      hint_text='State Name', height=40, size_hint=(1, None), multiline=False))
        row313.add_widget(
            Label(font_size=self.fts + 3, markup=1, text=f'[color={self.fg3}]Code :', width=70, size_hint=(None, 1)))
        row313.add_widget(
            MyTextInput(bg=self.bg3, fg=self.fg3, textvariable=self.bstcod, font_size=self.fts + 3, hint_text='Cde',
                        height=40, width=50, size_hint=(None, None), multiline=False))
        row31.add_widget(row312)
        row31.add_widget(row313)

        row32 = MyBoxLayout(bg=self.bg1, orientation='vertical', height=210,
                            size_hint=(0.29281045751633986928104575163399 * 2, None))
        l = Label(font_size=self.fts + 5, text=f'[color={self.fg2}][b]Terms of Delivery[/b]', markup=True, height=30,
                  size_hint=(1, None))
        l.bind(size=l.setter('text_size'))
        row32.add_widget(l)
        row32.add_widget(MyTextInput(bg=self.bg2, fg=self.fg2, textvariable=self.tod, font_size=self.fts + 3,
                                     hint_text='Terms of Delivery', height=200, multiline=True, size_hint=(1, None)))

        row3.add_widget(row31)
        row3.add_widget(row32)

        row4 = MyGridLayout(rows=7, bg=self.bg1, cols=7, size_hint=(1, self.shy[4]))
        for i, j in zip(["Sno", 'ITEM/DESCRIPTION', 'HSN/SAC', 'QUANTITY', 'RATE', 'UOM', "AMOUNT"],
                        [0.04298356510745891, 0.37168141592920356, 0.10366624525916561, 0.1264222503160556,
                         0.0695322376738306, 0.07964601769911504, 0.20606826801517067]):
            l = Label(font_size=self.fts + 3, halign='center', valign='middle', markup=1,
                      text=f"[color={self.fg4}][b]{i}", size_hint=(j, 1 / 7))
            l.bind(size=l.setter('text_size'))
            row4.add_widget(l)
        for i, k in zip(range(5), [[self.sno1, self.item1, self.hsn1, self.qty1, self.rate1, self.uom1, self.amt1],
                                   [self.sno2, self.item2, self.hsn2, self.qty2, self.rate2, self.uom2, self.amt2],
                                   [self.sno3, self.item3, self.hsn3, self.qty3, self.rate3, self.uom3, self.amt3],
                                   [self.sno4, self.item4, self.hsn4, self.qty4, self.rate4, self.uom4, self.amt4],
                                   [self.sno5, self.item5, self.hsn5, self.qty5, self.rate5, self.uom5, self.amt5]]):
            for j in range(7):
                if j == 0:
                    l = Label(font_size=self.fts + 3, halign='center', valign='middle', markup=1,
                              text=f"[color={self.fg4}][b]{i + 1}.", size_hint=(
                        [0.04298356510745891, 0.37168141592920356, 0.10366624525916561, 0.1264222503160556,
                         0.0695322376738306, 0.07964601769911504, 0.20606826801517067][j], 1 / 7))
                    l.bind(size=l.setter('text_size'))
                    row4.add_widget(l)
                else:
                    row4.add_widget(MyTextInput(bg=self.bg4, fg=self.fg4, textvariable=k[j], font_size=self.fts + 3,
                                                hint_text=f"{['Sno.', 'ITEM/DESCRIPTION', 'HSN/SAC', 'QUANTITY', 'RATE', 'UOM', 'AMOUNT'][j]}{i + 1}",
                                                size_hint=(
                                                [0.04298356510745891, 0.37168141592920356, 0.10366624525916561,
                                                 0.1264222503160556, 0.0695322376738306, 0.07964601769911504,
                                                 0.20606826801517067][j], 1 / 7), multiline=False))
        for i, j in zip(['Sno.', 'ITEM/DESCRIPTION', 'HSN/SAC', 'QUANTITY', 'RATE', 'UOM', 'AMOUNT'],
                        [0.04298356510745891, 0.37168141592920356, 0.10366624525916561, 0.1264222503160556,
                         0.0695322376738306, 0.07964601769911504, 0.20606826801517067]):
            if i == 'AMOUNT':
                row4.add_widget(
                    MyLabel(bg=self.bg1, textvariable=self.amt6, style=f'[color={self.fg4}][b]', font_size=self.fts + 3,
                            size_hint=(j, 1 / 7)))
            elif i != 'UOM':
                l = Label(font_size=self.fts + 3, text='', size_hint=(j, 1 / 7))
                l.bind(size=l.setter('text_size'))
                row4.add_widget(l)
            else:
                a = Label(font_size=self.fts + 3, halign='right', valign='middle', markup=1,
                          text=f'[color={self.fg4}][b]TOTAL', size_hint=(j, 1 / 7))
                a.bind(size=l.setter('text_size'))
                row4.add_widget(a)

        row5 = MyBoxLayout(bg=self.bg1, orientation='vertical', size_hint=(1, self.shy[5]))
        row5.add_widget(Label(font_size=self.fts + 5, halign='left', valign='middle', markup=1,
                              text=f'[color={self.fg4}][b]Amount Chargeable (in words)[/b][/color]',
                              size_hint=(0.34, 1 / 2)))
        row5.add_widget(
            MyLabel(bg=self.bg1, textvariable=self.amtw, font_size=self.fts + 5, style=f'[color={self.fg4}]',
                    size_hint=(1, 1 / 2)))

        row6 = MyGridLayout(bg=self.bg1, cols=2, size_hint=(1, self.shy[6]))

        row61 = MyGridLayout(bg=self.bg1, cols=2, size_hint=(0.3464968152866242, 1))

        row611 = MyGridLayout(bg=self.bg1, cols=1, size_hint=(1, 1 / 5))
        l = Label(font_size=self.fts + 3, markup=1, text=f'[color={self.fg4}][b]Taxable Amount', halign='right',
                  valign='middle', size_hint=(1, 1))
        l.bind(size=l.setter('text_size'))
        row611.add_widget(l)

        row612 = MyGridLayout(bg=self.bg1, cols=3, size_hint=(1, 1 / 5))
        l = Label(font_size=self.fts + 3, markup=1, text=f'[color={self.fg4}][b]SGST', halign='right', valign='middle',
                  size_hint=(3.5 / 6, 1))
        l.bind(size=l.setter('text_size'))
        row612.add_widget(l)
        row612.add_widget(
            MyTextInput(bg=self.bg4, fg=self.fg4, textvariable=self.sgstp, font_size=self.fts + 3, hint_text='SGST',
                        size_hint=(2 / 6, 1), multiline=0))
        row612.add_widget(
            Label(font_size=self.fts + 3, markup=1, text=f'[color={self.fg4}][b]%', size_hint=(0.5 / 6, 1)))

        row613 = MyGridLayout(bg=self.bg1, cols=3, size_hint=(1, 1 / 5))
        l = Label(font_size=self.fts + 3, markup=1, text=f'[color={self.fg4}][b]CGST', halign='right', valign='middle',
                  size_hint=(3.5 / 6, 1))
        l.bind(size=l.setter('text_size'))
        row613.add_widget(l)
        row613.add_widget(
            MyTextInput(bg=self.bg4, fg=self.fg4, textvariable=self.cgstp, font_size=self.fts + 3, hint_text='CGST',
                        size_hint=(2 / 6, 1), multiline=0))
        row613.add_widget(
            Label(font_size=self.fts + 3, markup=1, text=f'[color={self.fg4}][b]%', size_hint=(0.5 / 6, 1)))

        row614 = MyGridLayout(bg=self.bg1, cols=3, size_hint=(1, 1 / 5))
        l = Label(font_size=self.fts + 3, markup=1, text=f'[color={self.fg4}][b]IGST', halign='right', valign='middle',
                  size_hint=(3.5 / 6, 1))
        l.bind(size=l.setter('text_size'))
        row614.add_widget(l)
        row614.add_widget(
            MyTextInput(bg=self.bg4, fg=self.fg4, textvariable=self.igstp, font_size=self.fts + 3, hint_text='IGST',
                        size_hint=(2 / 6, 1), multiline=0))
        row614.add_widget(
            Label(font_size=self.fts + 3, markup=1, text=f'[color={self.fg4}][b]%', size_hint=(0.5 / 6, 1)))

        row615 = MyGridLayout(bg=self.bg1, cols=1, size_hint=(1, 1 / 5))
        l = Label(font_size=self.fts + 3, markup=1, text=f'[color={self.fg4}][b]INVOICE TOTAL', halign='right',
                  valign='middle', size_hint=(1, 1))
        l.bind(size=l.setter('text_size'))
        row615.add_widget(l)

        row61.add_widget(row611)
        row61.add_widget(
            MyLabel(bg=self.bg1, textvariable=self.amt6, font_size=self.fts + 3, halign='left', valign='middle',
                    style=f'[color={self.fg4}][b]'))

        row61.add_widget(row612)
        row61.add_widget(
            MyLabel(bg=self.bg1, textvariable=self.sgst, font_size=self.fts + 3, halign='left', valign='middle',
                    style=f'[color={self.fg4}][b]'))

        row61.add_widget(row613)
        row61.add_widget(
            MyLabel(bg=self.bg1, textvariable=self.cgst, font_size=self.fts + 3, halign='left', valign='middle',
                    style=f'[color={self.fg4}][b]'))

        row61.add_widget(row614)
        row61.add_widget(
            MyLabel(bg=self.bg1, textvariable=self.igst, font_size=self.fts + 3, halign='left', valign='middle',
                    style=f'[color={self.fg4}][b]'))

        row61.add_widget(row615)
        row61.add_widget(
            MyLabel(bg=self.bg1, textvariable=self.invt, font_size=self.fts + 3, halign='left', valign='middle',
                    style=f'[color={self.fg4}][b]'))

        l = Label(font_size=self.fts + 5,
                  text='[b][color=#9a79c7]Bank : CANARA BANK, MANGALAPATTI Branch\nA/C. No. 1352261010289 IFSC No. CNRB0001352[/b]',
                  markup=True, halign='right', valign='bottom', size_hint=(0.6535031847133758, 1))
        l.bind(size=l.setter('text_size'))
        row6.add_widget(row61)
        row6.add_widget(l)

        row7 = MyGridLayout(bg=self.bg1, cols=2, size_hint=(1, self.shy[7]))
        x = 0.6286624203821656
        l = Label(font_size=self.fts + 3,
                  text='[color=#4271ff]Declaration\nWe declare that this invoice shows the actual price of the\ngoods described and that all particular are true and correct.',
                  markup=True, halign='left', valign='middle', size_hint=(x, 1))
        l.bind(size=l.setter('text_size'))
        row7.add_widget(l)
        l = Label(font_size=self.fts + 5, text='[color=#4271ff]for [b]SRT TRADER[/b]\n \nAuthorized Signatory',
                  markup=True, halign='right', valign='middle', size_hint=(1 - x, 1))
        l.bind(size=l.setter('text_size'))
        row7.add_widget(l)

        details.add_widget(row1)
        details.add_widget(row2)
        details.add_widget(row3)
        details.add_widget(row4)
        details.add_widget(row5)
        details.add_widget(row6)
        details.add_widget(row7)

        # con=connect(self.db)
        # cur=con.cursor()
        # cur.execute('select * from addbook order by sno')
        # rows=cur.fetchall()
        # con.close()

        manage = MyGridLayout(cols=1, size_hint_y=1 - x - y)
        xx = 0.65
        self.tbl = t = Table(cols=5, size_hint_y=xx, bg1='#003333', bg2='#330033')
        shy = [0.05746242774566474, 0.17653179190751446, 0.30057803468208094, 0.17809248554913296, 0.2243352601156069]
        for i, j in zip(['Sno.', 'COMPANY', 'ADDRESS', 'GSTIN', 'STATE & CODE'], shy):
            t.h.add_widget(
                Label(font_size=self.fts + 5, text=f'[color=#77cccc][b]{i}', markup=1, size_hint=(j, None), height=50))
        self.display()

        btf = MyGridLayout(cols=3, size_hint_y=1 - xx)
        bg1 = '#00009b'
        fg2 = '#4747ff'
        bg2 = '#9b0000'
        fg2 = '#ff4747'
        bg3 = '#009b00'
        fg3 = '#47ff47'

        def dmy():
            pass

        for i, j, k, l in zip(
                ['SET SHIPPING ADD.', 'SET BILLING ADD.', 'CLEAR', 'ADD CONSIGNEE', 'ADD BUYER', 'CREATE BILL'],
                [bg1, bg1, bg2, bg1, bg1, bg3], [fg2, fg2, fg2, fg2, fg2, fg3],
                [self.sset, self.bset, self.clr, self.snew, self.bnew, self.crt]):
            b = MyButton(text=f'[b]{i}', markup=1, bg=j, fg=k, font_size=self.fts + 10)
            b.bind(on_press=l)
            btf.add_widget(b)

        manage.add_widget(t)
        manage.add_widget(btf)

        master.add_widget(details)
        master.add_widget(manage)
        self.clr()
        return master

    def crt(self, name=1):
        print(self.listmaker())
        return
        # self.biller = threading.Thread(target=biller, args=(self.listmaker(), self.o.rstrip('\Files'), self.clr))
        # self.biller.start()

    def display(self):
        con = connect(self.db)
        cur = con.cursor()
        cur.execute('select * from addbook order by sno')
        rows = cur.fetchall()
        con.close()
        shy = [0.05746242774566474, 0.17653179190751446, 0.30057803468208094, 0.17809248554913296, 0.2243352601156069]
        tbl = self.tbl.tbl
        tbl.clear_widgets()
        for i in range(len(rows)):
            for j, k in zip(range(5), shy):
                l = MyLabel(fun=self.gt, font_size=self.fts + 3, bg='#003333', fg='#cccc77', text=f'{str(rows[i][j])}',
                            id=i, size_hint=(k, None), height=120, halign='center', valign='middle')
                l.bind(size=l.setter('text_size'))
                tbl.add_widget(l)

    def gt(self, label):
        c = self.tbl.cols
        a = len(self.tbl.tbl.children) / c
        child = self.tbl.tbl.children
        l = [[] for i in range(int(a))]
        for i in range(int(a)):
            for j in range(c): l[i].append(child[i * c + j])
        l = l[::-1]
        v = []
        id = label.id
        for i in l[id][::-1]:
            bg = i.bg
            y = i.text.index('[color=')
            fg = i.text[y:y + 15]
            print(fg)
            t = i.text[:y] + i.text[y + 15:]
            v.append(t)
            i.text = f'[color={bg}]' + t
            i.bg = fg.strip('[color=').strip(']')
            i.bgch()
        v = v[1:]
        self.add.set(v[0] + '\n' + v[1])
        self.gstin.set(v[2])
        a = v[3].split()
        n = ''
        for i in a[:-1]: n += f'{i} '
        n.strip()
        self.stnam.set(n)
        self.stcod.set(v[3])
        l.pop(id)
        for i in l:
            for j in i:
                j.text = fg + j.text[len('[color=#cccc77]'):]
                j.bg = bg
                j.bgch()

    def snof(self):
        con = connect(self.db)
        cur = con.cursor()
        cur.execute('select * from addbook order by sno')
        rows = cur.fetchall()
        con.close()
        if len(rows) != 0:
            return int(rows[-1][0]) + 1
        else:
            return 1

    def sset(self, n):
        for i, j in zip([self.add, self.gstin, self.stnam, self.stcod],
                        [self.shipadd, self.sgstin, self.sstnam, self.sstcod]): j.set(i.get())

    def bset(self, n):
        for i, j in zip([self.add, self.gstin, self.stnam, self.stcod],
                        [self.billadd, self.bgstin, self.bstnam, self.bstcod]): j.set(i.get())

    def snew(self, n):
        for i in ['self.shipadd', 'self.sgstin', 'self.sstnam', 'self.sstcod']:
            if self.tvl[i].get() == '': return
        sname = self.shipadd.get().split('\n')[0]
        sadd = ''
        for i in self.shipadd.get().split('\n')[1:]:
            sadd += f'{i}\n'
        sadd.strip('\n')
        sgs = self.sgstin.get()
        sstc = self.sstnam.get() + ' ' + self.sstcod.get()
        # con=connect(self.db)
        # cur=con.cursor()
        # cur.execute(f"insert into addbook values({self.snof()},'{sname}','{sadd}','{sgs}','{sstc}')")
        # con.commit()
        # con.close()
        self.display()

    def bnew(self, n):
        for i in ['self.billadd', 'self.bgstin', 'self.bstnam', 'self.bstcod']:
            if self.tvl[i].get() == '': return
        list = []
        bname = self.billadd.get().split('\n')[0]
        badd = ''
        for i in self.billadd.get().split('\n')[1:]:
            badd += f'{i}\n'
        badd.strip('\n')
        bgs = self.bgstin.get()
        bstc = self.bstnam.get() + ' ' + self.bstcod.get()
        # con=connect(self.db)
        # cur=con.cursor()
        # cur.execute(f"insert into addbook values({self.snof()},'{bname}','{badd}','{bgs}','{bstc}')")
        # con.commit()
        # con.close()
        self.display()

    def sba_funs(self):
        if not self.sba.get(): return
        a = 0
        for i, j in zip([self.shipadd, self.sgstin, self.sstnam, self.sstcod],
                        [self.billadd, self.bgstin, self.bstnam, self.bstcod]):
            j.trace_remove(self.traces[a])
            j.set(i.get())
            self.traces[a] = j.trace(self.sba_funb)
            a += 1

    def sba_funb(self):
        if not self.sba.get(): return
        a = 4
        for i, j in zip([self.shipadd, self.sgstin, self.sstnam, self.sstcod],
                        [self.billadd, self.bgstin, self.bstnam, self.bstcod]):
            i.trace_remove(self.traces[a])
            i.set(j.get())
            self.traces[a] = i.trace(self.sba_funs)
            a += 1

    def sba_fun(self):
        self.sbat.set(f"[b]{'' if self.sba.get() else 'Not '}Same as Above[/b]")
        for i, j in zip([self.shipadd, self.sgstin, self.sstnam, self.sstcod],
                        [self.billadd, self.bgstin, self.bstnam, self.bstcod]): j.set(i.get())

    def fun(self, nam):
        if nam in ['self.item1', 'self.item2', 'self.item3', 'self.item4', 'self.item5']:
            return lambda: self.itemj(nam)
        elif nam in ['self.hsn1', 'self.hsn2', 'self.hsn3', 'self.hsn4', 'self.hsn5']:
            return lambda: self.hsnj(nam)
        elif nam in ['self.qty1', 'self.qty2', 'self.qty3', 'self.qty4', 'self.qty5']:
            return lambda: self.qtyj(nam)
        elif nam in ['self.rate1', 'self.rate2', 'self.rate3', 'self.rate4', 'self.rate5']:
            return lambda: self.ratej(nam)
        elif nam in ['self.uom1', 'self.uom2', 'self.uom3', 'self.uom4', 'self.uom5']:
            return lambda: self.uomj(nam)
        elif nam in ['self.cgstp', 'self.sgstp', 'self.igstp']:
            return lambda: self.gsteval(nam)
        elif nam in ['self.shipadd', 'self.sgstin', 'self.sstnam', 'self.sstcod']:
            return lambda: self.saddeval(nam)
        elif nam in ['self.billadd', 'self.bgstin', 'self.bstnam', 'self.bstcod']:
            return lambda: self.baddeval(nam)
        else:
            return lambda: self.nn()

    def saddeval(self, name):
        a = self.shipadd.get() + '\n'
        for i in ['self.sgstin', 'self.sstnam', 'self.sstcod']:
            if i == 'self.sgstin':
                if self.tvl[i].get() != '':
                    a += 'GSTIN/UIN    : '
                else:
                    continue
            elif i == 'self.sstnam':
                a += 'State Name   : '
            elif i == 'self.sstcod':
                a += 'Code : '
            a += self.tvl[i].get()
            if i == 'self.sstnam':
                a += ', '
            if i != 'self.sstnam' and i != 'self.sstcod': a += '\n'
        self.shipad.set(a)

    def baddeval(self, name):
        a = self.billadd.get() + '\n'
        for i in ['self.bgstin', 'self.bstnam', 'self.bstcod']:
            if i == 'self.bgstin':
                if self.tvl[i].get() != '':
                    a += 'GSTIN/UIN    : '
                else:
                    continue
            if i == 'self.bstnam':
                a += 'State Name   : '
            elif i == 'self.bstcod':
                a += 'Code : '
            a += self.tvl[i].get()
            if i == 'self.bstnam':
                a += ', '
            if i != 'self.bstnam' and i != 'self.bstcod': a += '\n'
        self.billad.set(a)

    def eval(self, name):
        a = name[-1]
        if str(self.tvl[f"self.qty{a}"].get()) != '' and str(self.tvl[f"self.rate{a}"].get()) != '':
            self.tvl[f"self.amt{a}"].set(
                round((float(self.tvl[f"self.qty{a}"].get()) * float(self.tvl[f"self.rate{a}"].get())) / 10) * 10)

        else:
            self.tvl[f"self.amt{a}"].set('')

        b = 0
        for i in range(1, 6):
            if self.tvl[f"self.amt{i}"].get() != '': b += float(self.tvl[f"self.amt{i}"].get())
        self.amt6.set(round(b / 10) * 10)

        for i in ['c', 's', 'i']:
            if self.tvl[f"self.{i}gstp"].get() != '' and self.amt6.get() != '' and self.amt6.get() != 0:
                b += float(self.tvl[f"self.{i}gstp"].get()) * 0.01 * float(self.amt6.get())
                self.tvl[f"self.{i}gst"].set(
                    round((float(self.tvl[f"self.{i}gstp"].get()) * 0.01 * float(self.amt6.get())) / 10) * 10)

        if str(self.tvl[f"self.qty{a}"].get()) != '' and str(self.tvl[f"self.rate{a}"].get()) != '':
            self.invt.set(round(b / 10) * 10)
            w = num2word(self.invt.get())
            self.amtw.set(w.word)

    def itemj(self, name):
        a = ''
        for i in ['self.item1', 'self.item2', 'self.item3', 'self.item4', 'self.item5']:
            if self.tvl[i].get() != '':
                a += str(self.tvl[i].get())
                a += '\n'
        a = a[:-1]
        self.amtj()
        self.item.set(a)

    def hsnj(self, name):
        a = ''
        for i in ['self.hsn1', 'self.hsn2', 'self.hsn3', 'self.hsn4', 'self.hsn5']:
            if self.tvl[i].get() != '':
                a += str(self.tvl[i].get())
                a += '\n'
        a = a[:-1]
        self.amtj()
        self.hsn.set(a)

    def qtyj(self, name):
        a = ''
        for i in ['self.qty1', 'self.qty2', 'self.qty3', 'self.qty4', 'self.qty5']:
            if self.tvl[i].get() != '':
                a += str(self.tvl[i].get())
                a += '\n'
        a = a[:-1]
        self.qty.set(a)
        self.eval(name)
        self.amtj()

    def ratej(self, name):
        a = ''
        for i in ['self.rate1', 'self.rate2', 'self.rate3', 'self.rate4', 'self.rate5']:
            if self.tvl[i].get() != '':
                a += str(self.tvl[i].get())
                a += '\n'
        a = a[:-1]
        self.rate.set(a)
        self.eval(name)
        self.amtj()

    def uomj(self, name):
        a = ''
        for i in ['self.uom1', 'self.uom2', 'self.uom3', 'self.uom4', 'self.uom5']:
            if self.tvl[i].get() != '':
                a += str(self.tvl[i].get())
                a += '\n'
        a = a[:-1]
        self.uom.set(a)
        self.amtj()

    def amtj(self):
        b = ''
        v = ['self.amt1', 'self.amt2', 'self.amt3', 'self.amt4', 'self.amt5']
        for i in range(1, 6):
            if self.tvl[v[i - 1]].get() != '':
                b += f"{i}."
                b += '\n'
        b = b[:-1]
        self.sno.set(b)
        a = ''
        for i in ['self.amt1', 'self.amt2', 'self.amt3', 'self.amt4', 'self.amt5']:
            if self.tvl[i].get() != '':
                a += str(self.tvl[i].get())
                a += '\n'
        a = a[:-1]
        self.amt.set(a)

    def gsteval(self, name):
        a = name[5]
        if self.amt6.get() != 0 and self.amt6.get() != '':
            if self.tvl[f"self.{a}gstp"].get() != 0 and self.tvl[f"self.{a}gstp"].get() != '':
                self.tvl[f"self.{a}gst"].set(
                    round((float(self.tvl[f"self.{a}gstp"].get()) * 0.01 * float(self.amt6.get())) / 10) * 10)
            else:
                self.tvl[f"self.{a}gst"].set('-')
        b = 0
        for i in ['c', 's', 'i']:
            if self.tvl[f"self.{i}gstp"].get() != '' and self.amt6.get() != '' and self.amt6.get() != 0:
                b += float(self.tvl[f"self.{i}gstp"].get()) * 0.01 * float(self.amt6.get())
                self.tvl[f"self.{i}gst"].set(
                    round((float(self.tvl[f"self.{i}gstp"].get()) * 0.01 * float(self.amt6.get())) / 10) * 10)
        if self.amt6.get() != '':
            self.invt.set(round((float(self.amt6.get()) + b) / 10) * 10)
            w = num2word(self.invt.get())
            self.amtw.set(w.word)

    def nn(self):
        pass

    def getdt(self, dt=1, mode=1):
        curdate = date.today()
        x = 0
        if dt == 1: dt, x = str(curdate).split('-'), 1
        mon = {'01': 'JAN', '02': 'FEB', '03': 'MAR', '04': 'APR', '05': 'MAY', '06': 'JUN', '07': 'JUL', '08': 'AUG',
               '09': 'SEPT', '10': 'OCT', '11': 'NOV', '12': 'DEC'}
        if x == 1:
            if mode == 1:
                return dt[2] + '-' + mon[dt[1]] + '-' + dt[0][2:]
            else:
                return dt[2] + '/' + dt[1] + '/' + dt[0]
        else:
            dt = dt.split('/')
            return dt[0] + '-' + mon[dt[1]] + '-' + dt[2][2:]

    def clr(self, n=1):
        for i in [self.add, self.gstin, self.stnam, self.stcod]:
            i.set('')

        for i in self.tvl.keys():
            self.tvl[i].set('')

        self.sba.set(0)

        self.sstnam.set('Tamil Nadu')
        self.sstcod.set('33')
        self.bstnam.set('Tamil Nadu')
        self.bstcod.set('33')

        for i in range(1, 6):
            self.tvl[f"self.sno{i}"].set(str(i) + '.')

        a = open(self.o.rstrip('\Files') + '/Files/nos.txt', 'r')
        self.invno.set(a.read())

        self.date.set(self.getdt(mode=2))

    def listmaker(self):
        list = [self.invno, self.date, self.delnote, self.mot, self.bon, self.bdate,
                self.shipadd, self.ddno, self.dndate, self.dispthr, self.dest,
                self.bol, self.vno, self.billadd, self.tod, self.sno, self.item,
                self.hsn, self.qty, self.rate, self.uom, self.amt, self.amt6, self.amtw,
                self.cgstp, self.cgst, self.sgstp, self.sgst, self.igstp, self.igst, self.invt]
        values = []
        for i in range(len(list)):
            if i not in [len(list) - x for x in range(2, 8)]:
                values.append(list[i].get())
            else:
                if list[i].get() != '':
                    values.append(list[i].get())
                else:
                    values.append('-')
        values[1] = self.getdt(self.date.get(), 2)
        return values


if __name__ == '__main__':
    MyApp().run()
