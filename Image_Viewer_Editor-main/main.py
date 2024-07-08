import tkinter as tk
from tkinter import ttk, Toplevel, Frame, Button, messagebox
from app_options import AppOptions  # tried to make a button
from image_manager import ImageManager
from editor_options import EditorOptions
from history_of_edits import History


class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.file_location = ""
        self.original_image = None
        self.processed_image = None
        self.image_properties = None

        self.advanced_tools = None
        self.in_crop_mode = False

        self.undo_performed = False
        self.history = []
        self.item_clicked = False

        self.is_saved = False

        self.configure(bg="#6b6b6b")

        self.title("Image Editor")
        self.geometry("1440x810")
        self.resizable(True, True)

        # Creates a frame for the main window
        main_frame = tk.Frame(self, bg="#6b6b6b")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.app_options = AppOptions(master=main_frame)
        self.app_options.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        separator1 = ttk.Separator(master=main_frame, orient=tk.HORIZONTAL)
        separator1.pack(fill=tk.X, padx=10, pady=5)

        self.editor_options = EditorOptions(master=main_frame)
        self.editor_options.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=10)

        separator4 = ttk.Separator(master=main_frame, orient=tk.VERTICAL)
        separator4.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.image_viewer = ImageManager(master=main_frame)
        self.image_viewer.pack(side=tk.LEFT, fill=tk.BOTH,
                               padx=20, pady=10, expand=True)

        separator5 = ttk.Separator(master=main_frame, orient=tk.VERTICAL)
        separator5.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.history_of_edits = History(master=main_frame)
        self.history_of_edits.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Bindings
        self.bind("<Control-z>", self.history_of_edits.undo_action)
        self.bind('<Control-y>', self.history_of_edits.redo_action)

        self.bind("<MouseWheel>", self.image_viewer._zoom)
        self.bind("<Control-equal>", self.image_viewer._zoom_in)
        self.bind("<Control-minus>", self.image_viewer._zoom_out)

        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _switch_crop_to_off(self):
        """
        Switches the crop mode to off.
        """
        self.in_crop_mode = False

    def _on_closing(self, event=None):
        """
        Prompts the user to save the image before closing the window.
        """
        if not self.is_saved:
            save_prompt = tk.Toplevel(self)
            save_prompt.title("Save Image")
            save_prompt.geometry("300x100")
            save_prompt.resizable(False, False)
            save_prompt.configure(bg="#6b6b6b")

            save_question = tk.Label(
                save_prompt, text="Would you like to save your image?", bg="#6b6b6b", fg="white")
            save_question.pack(anchor="center")

            save_button = tk.Button(
                save_prompt, text="Save", width=4, height=2, command=self._combine_save)
            save_button.pack(anchor="center", padx=25, pady=10, side=tk.LEFT)

            no_button = tk.Button(save_prompt, text="No",
                                  width=4, height=2, command=self.destroy)
            no_button.pack(anchor="center", padx=25, pady=10, side=tk.RIGHT)

            # Intercept window closing event
            self.protocol("WM_DELETE_WINDOW",
                          lambda: self._close_window(save_prompt))

        else:
            self.destroy()

    def _close_window(self, window):
        """
        Closes the window and destroys the window object.

        Parameters:
            window (tk.Toplevel): The window to be closed.
        """
        window.destroy()
        self.destroy()

    def _combine_save(self):
        """
        Combines the save and destroy methods.
        """
        self.app_options.save_button_click()
        self.destroy()
