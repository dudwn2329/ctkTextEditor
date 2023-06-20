import datetime
import tkinter as tk

from ttkbootstrap.constants import *
import customtkinter as ctk
from PIL import Image
import os

fontName = '맑은 고딕'
default_font_size = 14
fontColor = '#333'
fontBackground = '#FFFFFF'

basicfont = ("맑은 고딕", default_font_size,)


# text editor reference: https://www.thepythoncode.com/article/create-rich-text-editor-with-tkinter-python
class Memo(ctk.CTkFrame):
    def __init__(self, parent, memoItem=None, memoId=None, **kwargs):
        ctk.CTkFrame.__init__(self, parent, **kwargs)
        self.titleVar = tk.StringVar()
        self.dateVar = tk.StringVar()
        self.isChanged = False
        self.memoId = memoId
        self.parent = parent
        self.memoItem = memoItem
        self.text_frame = ctk.CTkFrame(self, fg_color="transparent", bg_color="transparent", width=350, height=320, border_width=0)
        self.text_frame.propagate(True)
        # 앱 종료 시 함수 실행
        self.parent.protocol("WM_DELETE_WINDOW", self.on_close)
        # 서식 지정 단축키 설정, italic과 overstrike는 다른 단축키와 겹쳐 버그 발생해서 비활성화
        self.parent.bind_all('<Control-b>', lambda tagName: self.tagToggle('bold'))
        #self.parent.bind_all('<Control-i>', lambda tagName: self.tagToggle('italic'))
        self.parent.bind_all('<Control-u>', lambda tagName: self.tagToggle('underline'))
        #self.parent.bind_all('<Control-t>', lambda tagName: self.tagToggle('overstrike'))

        # 위젯 생성, 스크롤바 추가
        self.text = tk.Text(self.text_frame, relief=FLAT, borderwidth=0, width=300, height=320, font=basicfont, foreground="#333",
                            insertwidth=1, insertbackground='black', insertborderwidth=1, undo=True, tabs=24)
        self.text.bind("<KeyRelease>", self.onInput)
        scrollbar = ctk.CTkScrollbar(self.text_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.text.configure(yscrollcommand=scrollbar.set)

        # 태크타입(서식) 정의
        self.tagTypes = None
        self.initTagTypes()

        # header
        header = ctk.CTkFrame(self.text_frame, height=60, fg_color="white", corner_radius=0)
        header.pack(side="top", fill="x", pady=0)

        # 상단 좌측 구역
        header_left = ctk.CTkFrame(header, fg_color="white", corner_radius=0, height=60, width=350)
        date_label = ctk.CTkLabel(header_left, font=ctk.CTkFont(family=fontName, size=12, weight='bold'),
                                  text_color="#15A2B6", textvariable=self.dateVar, height=15)
        title_entry = ctk.CTkEntry(header_left, font=(fontName, 20, 'bold'),
                                   textvariable=self.titleVar, border_width=0, fg_color="white", height=15,
                                   placeholder_text="제목")
        title_entry.bind("<KeyRelease>", self.onInput)
        date_label.pack(side=TOP, anchor="w", padx=5, pady=(10, 0))

        title_entry.pack(side=LEFT, ipady=2, fill=X, expand=True)
        header_left.pack(side=LEFT, padx=5, fill=X, expand=True)

        # 상단 우측 구역
        header_right = ctk.CTkFrame(header, fg_color="white", corner_radius=0, height=60, width=50)
        bold_button = StyleButton(header_right, "delete", command=lambda: self.deleteNote())
        bold_button.pack(side=BOTTOM, anchor="e")
        header_right.pack(side=RIGHT, fill=Y)

        # 서식 버튼 바
        formattingbar = tk.Frame(self, padx=2)

        # 서식 버튼
        bold_button = StyleButton(formattingbar, "bold", command=lambda: self.tagToggle("bold"))
        italic_button = StyleButton(formattingbar, "italic", command=lambda: self.tagToggle("italic"))
        underline_button = StyleButton(formattingbar, "underline", command=lambda: self.tagToggle("underline"))
        strike_button = StyleButton(formattingbar, "strike", command=lambda: self.tagToggle("overstrike"))
        plus_button = StyleButton(formattingbar, "plus", command=self.biggerFont)
        minus_button = StyleButton(formattingbar, "minus", command=self.smallerFont)

        bold_button.pack(side="left", padx=2, pady=4)
        italic_button.pack(side="left", padx=2, pady=4)
        underline_button.pack(side="left", padx=2, pady=4)
        strike_button.pack(side="left", padx=2, pady=4)
        plus_button.pack(side="right", padx=2, pady=4)
        minus_button.pack(side="right", padx=2, pady=4)

        formattingbar.pack(side="bottom", fill="x", pady=0)

        self.text_frame.pack(side="bottom", expand=True)
        self.text.pack(side="left", fill="both", padx=10, pady=10)
        #self.loadMemo()

    def initTagTypes(self):
        # 태그조합 chatGpt로 생성함
        self.tagTypes = {
            'bold': {'font': (fontName, default_font_size, 'bold'), 'foreground': '#333'},
            'italic': {'font': (fontName, default_font_size, 'italic'), 'foreground': '#333'},
            'underline': {'font': (fontName, default_font_size, 'underline'), 'foreground': '#333'},
            'overstrike': {'font': (fontName, default_font_size, 'overstrike'), 'foreground': '#333'},
            'bold italic': {'font': (fontName, default_font_size, 'bold italic'), 'foreground': '#333'},
            'bold underline': {'font': (fontName, default_font_size, 'bold underline'), 'foreground': '#333'},
            'bold overstrike': {'font': (fontName, default_font_size, 'bold overstrike'), 'foreground': '#333'},
            'italic underline': {'font': (fontName, default_font_size, 'italic underline'), 'foreground': '#333'},
            'italic overstrike': {'font': (fontName, default_font_size, 'italic overstrike'), 'foreground': '#333'},
            'overstrike underline': {'font': (fontName, default_font_size, 'underline overstrike'), 'foreground': '#333'},
            'bold italic underline': {'font': (fontName, default_font_size, 'bold italic underline'), 'foreground': '#333'},
            'bold italic overstrike': {'font': (fontName, default_font_size, 'bold italic overstrike'), 'foreground': '#333'},
            'bold overstrike underline': {'font': (fontName, default_font_size, 'bold underline overstrike'), 'foreground': '#333'},
            'italic overstrike underline': {'font': (fontName, default_font_size, 'italic underline overstrike'), 'foreground': '#333'},
            'bold italic overstrike underline': {'font': (fontName, default_font_size, 'bold italic underline overstrike'), 'foreground': '#333'},
        }
        # Text 위젯에 태그 정의
        for tagType in self.tagTypes:
            self.text.tag_configure(tagType.lower(), self.tagTypes[tagType])

    # 동작 후 1초간 추가동작 없을 시 메모 저장, chatGpt
    def onInput(self, event=None):
        self.isChanged = True
        if hasattr(self, "timer_id"):
            self.master.after_cancel(self.timer_id)
        self.timer_id = self.master.after(1000, self.saveMemo)

    def loadMemo(self):
        pass

    def saveMemo(self):
        pass
        today = datetime.datetime.now()
        formatted_date = today.strftime('%y.%m.%d %H:%M')
        self.dateVar.set(formatted_date)

    def tagToggle(self, tagName):
        try:
            tags = ' '.join(self.text.tag_names("sel.first"))

            current_tags = set(tag for tag in tags.split(' ') if tag != "sel")
            # toggle the tag
            if tagName in current_tags:
                current_tags.remove(tagName)
                self.text.tag_remove(tagName, "sel.first", "sel.last")
            else:
                current_tags.add(tagName)

            combined_tag = ' '.join(sorted(current_tags))

            if combined_tag in self.tagTypes:
                self.remove_tags()
                self.text.tag_add(combined_tag, "sel.first", "sel.last")
            self.onInput()
        except:
            pass

    def remove_tags(self):
        # get current tags
        current_tags = self.text.tag_names("sel.first")
        # remove each tag from the selection
        for tag in current_tags:
            if tag != "sel":
                self.text.tag_remove(tag, "sel.first", "sel.last")

    def deleteNote(self):
        pass

    def on_close(self):
        if self.isChanged:
            self.saveMemo()
        self.parent.destroy()

    def biggerFont(self):
        global default_font_size
        if default_font_size >= 24:
            return
        default_font_size += 2
        self.initTagTypes()
        self.text.configure(font=(fontName, default_font_size))

    def smallerFont(self):
        global default_font_size
        if default_font_size <= 10:
            return
        default_font_size -= 2
        self.initTagTypes()
        self.text.configure(font=(fontName, default_font_size))


class StyleButton(ctk.CTkButton):
    def __init__(self, parent, iconname, **kwargs):
        super().__init__(parent, **kwargs)
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets/images/icons")
        button_image = ctk.CTkImage(Image.open(os.path.join(image_path, iconname + ".png")), size=(14, 14))
        self.configure(image=button_image, hover_color="gray80", fg_color="transparent", text="", width=30, height=30, corner_radius=5)
