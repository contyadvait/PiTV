from PIL import Image
import customtkinter
import tkinter.font as tkFont
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer

FR_PRIVATE  = 0x10
FR_NOT_ENUM = 0x20

def loadfont(fontpath, private=True, enumerable=False):
    '''
    Makes fonts located in file `fontpath` available to the font system.

    `private`     if True, other processes cannot see this font, and this
                  font will be unloaded when the process dies
    `enumerable`  if True, this font will appear when enumerating fonts

    See https://msdn.microsoft.com/en-us/library/dd183327(VS.85).aspx

    '''
    # This function was taken from
    # https://github.com/ifwe/digsby/blob/f5fe00244744aa131e07f09348d10563f3d8fa99/digsby/src/gui/native/win/winfonts.py#L15
    # This function is written for Python 2.x. For 3.x, you
    # have to convert the isinstance checks to bytes and str
    if isinstance(fontpath, str):
        pathbuf = create_string_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExA
    elif isinstance(fontpath, unicode):
        pathbuf = create_unicode_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExW
    else:
        raise TypeError('fontpath must be of type str or unicode')

    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
    numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
    return bool(numFontsAdded)


customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("720x480")

def button_function():
    print("button pressed")

my_image = customtkinter.CTkImage(light_image=Image.open("wallpaper.png"),
                                  dark_image=Image.open("wallpaper.png"),
                                  size=(1920, 1080))

image_label = customtkinter.CTkLabel(app, image=my_image, text="")
image_label.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

font = tkFont.Font(family=load_font("Urbanist.ttf"))
text = customtkinter.CTkLabel(app, text="Welcome to PiTV!", font=(font, 48))
text.configure(text_color="white", bg_color="black")
text.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

app.mainloop()