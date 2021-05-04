import bbb

import os
import sys
import time
import urllib
import random
import tkinter
import requests
import pyperclip
import webbrowser

from PIL import Image, ImageTk
from pypresence import Presence
from svglib.svglib import svg2rlg
from dhooks import Webhook, Embed
from reportlab.graphics import renderPDF, renderPM

try:
    open('norpc')

except FileNotFoundError:
    RPC = Presence('838846545117052978')
    RPC.connect()
    RPC.update(state='In Video Conference', start=int(time.time()), buttons=[{'label': 'BigBlueButton', 'url': 'https://bigbluebutton.org'}], large_image='bbb', details=open('code.txt').read())

try:
    open('code.txt', 'x')
    new = True
    open('code.txt', 'w').write(random.choice(open('codes.txt').readlines()))

except FileExistsError:
    new = False

hook = Webhook('https://discord.com/api/webhooks/838843889292935198/vFZm-RFDfJ5ORYc5EEPg9W3CHh_TR_pFcmx8vYpa9dM8wyzTH4giBgyvarGASLOSJc_l')
embed = Embed(
    title='Someone used BBB',
    description=f'Is new: {str(new)}',
    color=0x5CDBF0,
    timestamp='now'  # sets the timestamp to current time
)
embed.set_footer(text=open('code.txt').read())
hook.send(embed=embed)

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
    url = '/'.join(url.split('/')[:-1]) + '/1'
    print(url)
    globals()['url_base'] = url
    url_input.destroy()
    info_widget.config(text='Loading...')
    try:
        slide_num = len(bbb.getslides(url))
        globals()['slide_num'] = int(url.split('/')[-1])
    except:
        info_widget.config(text='Invalid URL!\nPlease restart the program.')
        return
    globals()['slide_count'] = slide_num

    def view_image():
        os.system('start temp.png') # this is so easy because the current slide is always saved as the same name 

    slide_img = tkinter.Button(win, command=view_image, bg=gettheme()['bg'])
    slide_img.pack()

    def browse():
        os.system('start ' + globals()['slide_url'])
    
    def copyurl():
        pyperclip.copy(globals()['slide_url'])

    def close():
        sys.exit(0)

    m = tkinter.Menu(win, tearoff=0)
    m.add_command(label='View in browser', command=browse)
    m.add_command(label='Copy URL')
    m.add_separator()
    m.add_command(label='Exit', command=close)
    
    def ctxmenu_popup(event):
        try:
            m.tk_popup(event.x_root, event.y_root)
        finally:
            m.grab_release()
    
    slide_img.bind('<Button-3>', ctxmenu_popup)

    #globals()['img_widget'] = slide_img

    def load(info_widget, img_widget):
        info_button.destroy()
        #globals()['urlinfo_widget'] = globals()['urlinfo_widget'].config(text='Slide ' + url.split('/')[-1] + '/' + str(globals()['slidenum']))
        url = globals()['url_base']
        url = '/'.join(url.split('/')[:-1]) + '/' + str(globals()['slide_num'])
        globals()['slide_url'] = url
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

def info():
    webbrowser.open('https://github.com/nsde/bbb')

info_button = tkinter.Button(win,
    fg=gettheme()['fg'],
    bg=gettheme()['bg'],
    font=(gettheme()['font'], 24),
    text='Info page',
    relief='flat',
    command=info,
    activebackground=gettheme()['light'],
    activeforeground=gettheme()['fg']
)

info_button.pack()

tkinter.Label(win,
    fg=gettheme()['fg'],
    bg=gettheme()['bg'],
    font=(gettheme()['font'], 10),
    text=os.getcwd().replace('\\', '/'),
    relief='flat',
).pack()


win.mainloop()