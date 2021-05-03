import bbb

import os
import urllib
import tkinter
import requests

from PIL import Image, ImageTk
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM


def gettheme():
    theme = {}
    theme['fg'] = 'white'
    theme['bg'] = '#0E0F13'
    theme['font'] = 'Yu Gothic UI Light'
    theme['light'] = '#008AE6'
    return theme

win = tkinter.Tk()
win.title('BBB Tools')
win.config(bg=gettheme()['bg'])
#win.geometry('500x400')

url_info = tkinter.Label(win,
    fg=gettheme()['fg'],
    bg=gettheme()['bg'],
    font=(gettheme()['font'], 20),
    text='Input presentation URL below:',
    relief='flat',
)

url_info.pack()
#globals()['urlinfo_widget'] = url_info


url_input = tkinter.Entry(win,
    fg=gettheme()['fg'],
    bg=gettheme()['light'],
    font=(gettheme()['font'], 24),
    relief='flat',
)

url_input.pack()

def start(info_widget):
    start_button.destroy()
    url = url_input.get()
    globals()['url_base'] = url
    url_input.destroy()
    slide_num = len(bbb.getslides(url))
    globals()['slide_num'] = int(url.split('/')[-1])
    globals()['slide_count'] = slide_num

    slide_img = tkinter.Label(win)
    slide_img.pack()
    #globals()['img_widget'] = slide_img

    def load(info_widget, img_widget):
        #globals()['urlinfo_widget'] = globals()['urlinfo_widget'].config(text='Slide ' + url.split('/')[-1] + '/' + str(globals()['slidenum']))
        url = globals()['url_base']
        url = '/'.join(url.split('/')[:-1]) + '/' + str(globals()['slide_num'])
        info_widget.config(text='Slide ' + str(globals()['slide_num']) + '/' + str(globals()['slide_count']))

        img_data = urllib.request.urlopen(url.replace('svg', 'png'))
        with open('temp.png', 'wb') as f:
            f.write(img_data.read())
        
        img = Image.open(os.getcwd().replace('\\', '/') + '/temp.png')
        wpercent = (500/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((500, hsize), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        # Now, those 3 lines do the same, but
        # I just want to be safe xD 
        img_widget['image'] = img
        img_widget.config(image=img)
        img_widget.image = img
        
    def last_slide(info_widget, img_widget):
        if globals()['slide_num'] > 1:
            globals()['slide_num'] -= 1
            load(info_widget, img_widget=img_widget)

    def next_slide(info_widget, img_widget):
        if globals()['slide_num'] != globals()['slide_count']:
            globals()['slide_num'] += 1
            load(info_widget, img_widget=img_widget)

    control_frame = tkinter.Frame(
        bd=0,
        bg=gettheme()['bg'],
        relief='flat',
    )
    control_frame.pack()

    last_button = tkinter.Button(control_frame,
        fg=gettheme()['fg'],
        bg=gettheme()['bg'],
        font=(gettheme()['font'], 24),
        text='◀',
        relief='flat',
        command=lambda: last_slide(info_widget, slide_img),
        activebackground=gettheme()['bg'],
        activeforeground=gettheme()['light']
    )

    last_button.pack(side='left')

    next_button = tkinter.Button(control_frame,
        fg=gettheme()['fg'],
        bg=gettheme()['bg'],
        font=(gettheme()['font'], 24),
        text='▶',
        relief='flat',
        command=lambda: next_slide(info_widget, slide_img),
        activebackground=gettheme()['bg'],
        activeforeground=gettheme()['light']
    )

    next_button.pack(side='right')

    load(info_widget, slide_img)

start_button = tkinter.Button(win,
    fg=gettheme()['fg'],
    bg=gettheme()['bg'],
    font=(gettheme()['font'], 24),
    text='Start',
    relief='flat',
    command=lambda: start(url_info),
    activebackground=gettheme()['light'],
    activeforeground=gettheme()['fg']
)

start_button.pack()
win.mainloop()
