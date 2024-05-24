import tkinter as tk


class GUIElement:
    def __init__(
        self,
        side: str = "top",
        expand: bool = True,
        fill: str = "none",
        relief: str = "flat",
        borderwidth=0,
        padx: int = 0,
        pady=0,
        width: int = -1,
        height: int = -1,
    ) -> None:

        self.side = side
        self.expand = expand
        self.fill = fill

        self.relief = relief
        self.borderwidth = borderwidth

        self.padx = padx
        self.pady = pady

        self.width = width
        self.height = height


class GUIFrame(GUIElement):
    def __init__(
        self,
        root,
        side: str = "top",
        expand: bool = True,
        fill: str = "none",
        relief: str = "raised",
        borderwidth: int = 2,
        padx: int = 0,
        pady: int = 0,
        width: int = -1,
        height: int = -1,
    ) -> None:

        super().__init__(
            side=side,
            expand=expand,
            fill=fill,
            relief=relief,
            borderwidth=borderwidth,
            padx=padx,
            pady=pady,
            width=width,
            height=height,
        )

        self.root = root

        if isinstance(root, tk.Frame):
            self.frame = tk.Frame(
                self.root,
                relief=self.relief,
                borderwidth=self.borderwidth,
                width=self.width,
                height=self.height,
            )
        elif isinstance(root, GUIFrame):
            self.frame = tk.Frame(
                self.root.frame,
                relief=self.relief,
                borderwidth=self.borderwidth,
                width=self.width,
                height=self.height,
            )
        else:
            raise TypeError(
                f"Root must be tk.Frame or GUIFrame, {type(root)} was given!"
            )

        self.elements = []

    def add(self, element) -> None:
        self.elements.append(element)

    def pack(self, root="") -> None:
        if root != "":
            self.root = root
        if isinstance(self.root, tk.Frame):
            self.frame = tk.Frame(
                self.root,
                relief=self.relief,
                borderwidth=self.borderwidth,
                width=self.width,
                height=self.height,
            )
        elif isinstance(self.root, GUIFrame):
            self.frame = tk.Frame(
                self.root.frame,
                relief=self.relief,
                borderwidth=self.borderwidth,
                width=self.width,
                height=self.height,
            )
        else:
            raise TypeError(
                f"Root must be tk.Frame or GUIFrame, {type(self.root)} was given!"
            )
        self.frame.pack(
            expand=self.expand,
            fill=self.fill,
            side=self.side,
            padx=self.padx,
            pady=self.pady,
        )
        for i in range(len(self.elements)):
            self.elements[i].pack(self.frame)


class GUIButton(GUIElement):
    def __init__(self, text: str, function, color: str = "#FFFFFF") -> None:

        super().__init__(
            side="left",
            expand=True,
            fill="none",
            relief="raised",
            borderwidth=2,
            padx=10,
            pady=10,
        )

        self.text: str = text
        self.function = function
        self.color = color

    def pack(self, root: tk.Frame) -> None:
        self.button: tk.Button = tk.Button(
            root,
            text=self.text,
            command=self.function,
            bg=self.color,
            relief=self.relief,
            borderwidth=self.borderwidth,
            width=self.width,
            height=self.height,
        )
        self.button.pack(
            side=self.side,
            expand=self.expand,
            fill=self.fill,
            padx=self.padx,
            pady=self.pady,
        )
