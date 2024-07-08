from tkinter import Frame, Button, END, LEFT, Menu, Toplevel, Text, ttk
from file_manager import FileManager
from image_properties import ImageProperties
import cv2
import time
import os
from PIL import Image
import numpy as np

class AppOptions(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=master, bg="#6b6b6b")

        self.file_options_button = Button(
            self, text="File", command=self._show_file_menu)
        self.file_options_button.pack(side=LEFT)

        self.file_menu = Menu(self, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_button_click)
        self.file_menu.add_command(
            label="Save", command=self.save_button_click)
        self.file_menu.add_command(
            label="Save As", command=self.save_as_button_click)

        self.edit_options_button = Button(
            self, text="Edit", command=self._show_edit_menu)
        self.edit_options_button.pack(side=LEFT)

        self.edit_menu = Menu(self, tearoff=0)
        self.edit_menu.add_command(
            label="Batch Processing", command=self.batch_processing_button_click)

        self.help_menu_items = [
            "General", # h2
            "Import Image",
            "Export Image",
            "Undo Edit",
            "Redo Edit",
            "Batch Processing",
            "Zoom",
            "Pan",
            "Save File",
            "History Selection",
            "Access Meta Data",
            "Clear All",
            "Advanced Edits", # h2
            "Brightness",
            "Contrast",
            "Blur",
            "Hue",
            "Saturation",
            "Basic Edits", # h2
            "Horizontal Flip",
            "Vertical Flip",
            "Rotate",
            "Resize",
            "Grayscale",
            "Sepia",
            "Crop"
        ]

        self.dictionary_of_help_menu_items_and_help_information = {
            "Import Image":
                "To import an image, navigate to the homepage and click on \"File\" -> \"New.\" Select your desired image file. Supported formats include .png, .jpeg (.jpg), .gif, .bmp, and .tiff.",

            "Export Image":
                "To export an image, go to the homepage, click on \"File\" -> \"Save As,\" enter the filename, choose the destination, and select the file type. Supported formats include .png, .jpeg (.jpg), .gif, .bmp, and .tiff.",

            "Undo Edit":
                "Undo edits by clicking the undo button on the homepage or using the keyboard shortcut Ctrl+Z.",

            "Redo Edit":
                "Redo edits by clicking the redo button on the homepage or using the keyboard shortcut Shift+Ctrl+Z.",

            "Batch Processing":
                "Initiate batch processing by selecting \"Edit\" -> \"Batch Processing\" and choosing the files you want to apply the edits to.",

            "Zoom":
                "Effortlessly zoom in and out using your trackpad or by holding down the 'Ctrl' key and pressing '+' or '-'.",

            "Pan":
                "Navigate across your image seamlessly by clicking and dragging your mouse. To move around the image, click, hold, and drag to explore different areas. Release the mouse button when you've reached the desired view.",

            "Crop":
                "To crop an image, select the \"Crop\" option, click, and\drag across the desired area. Release the mouse button to confirm the crop.",

            "Brightness":
                "Adjust brightness by selecting \"Advanced\" on the homepage and using the brightness slider (range: [0, 100]). Click apply when finished.",

            "Contrast":
                "Adjust contrast by selecting \"Advanced\" on the homepage and using the contrast slider (range: [0, 100]). Click apply when finished.",

            "Blur":
                "Adjust blur by selecting \"Advanced\" on the homepage and using the blur slider (range: [0, 100]). Click apply when finished.",

            "Hue":
                "Adjust hue by selecting \"Advanced\" on the homepage and using the hue slider (range: [-100, 100]). Click apply when finished.",

            "Saturation":
                "Adjust saturation by selecting \"Advanced\" on the homepage and using the saturation slider (range: [-100, 100]). Click apply when finished.",

            "Horizontal Flip":
                "Apply a horizontal flip by selecting \"Horz Flip\" on the homepage, resulting in a mirrored version along the vertical axis.",

            "Vertical Flip":
                "Apply a vertical flip by selecting \"Vert Flip\" on the homepage, resulting in a mirrored version along the horizontal axis.",

            "Rotate":
                "Rotate the image 90° counterclockwise by selecting \"Rotate\" on the homepage.",

            "Resize":
                "Resize an image by selecting \"Resize\" on the homepage and entering width and height values within the valid range [1, 7680].",

            "Grayscale":
                "Apply grayscale by selecting \"Grayscale\" on the homepage, converting the image to shades of gray.",

            "Sepia":
                "Apply sepia by selecting \"Sepia\" on the homepage, imparting a warm, brownish tone for a vintage look.",

            "Clear All":
                "Clear all applied edits by selecting \"Clear All\" on the homepage. The history log remains for future reference.",

            "Save File":
                "Save the image by clicking \"File\" -> \"Save\" on the\homepage, saving it to your operating system's file manager.",

            "History Selection":
                "Access the history log on the homepage's right panel.Click on a history item to return to a specific point in your image's editing history. Items are labeled with the edit and time.",

            "Access Meta Data":
                """Meta data is displayed for the loaded image on the bottom left of the homepage. The following information can be found: size (in Bytes), file name, extension, Bytes per pixel, and zoomed-in resolution."""
        }

        self.help_button = Button(
            self, text="Help", command=self._show_help_menu)
        self.help_button.pack(side="left")

    def convert_index_to_end(self, index):
        """
        Converts an index to the end of the line
        """
        line, column = index.split('.')
        return f"{line}.end"

    def _add_help_menu_items(self):
        """
        Adds the help menu items to the help text
        """
        current_position = self.help_text.index("insert")
        end_index = self.convert_index_to_end(current_position)
        self.help_text.insert(END, "User Guide\n\n")
        self.help_text.tag_add("header", current_position, end_index)
        self.help_text.tag_configure("header", font=("Arial", 30, "bold"))

        for element in self.help_menu_items:
            help_info = self.dictionary_of_help_menu_items_and_help_information.get(
                element, "")
            if element not in self.dictionary_of_help_menu_items_and_help_information: # h2 is being added
                self.help_text.insert(END, "\n")
                current_position = self.help_text.index("insert")
                end_index = self.convert_index_to_end(current_position)
                self.help_text.insert(END, f"{element}\n")
                self.help_text.tag_add("header1", current_position, end_index)
                self.help_text.tag_configure(
                    "header1", font=("Arial", 20, "bold", "underline"))
                self.help_text.insert(END, "\n")
            else:
                current_position = self.help_text.index("insert")
                end_index = self.convert_index_to_end(current_position)
                self.help_text.insert(END, f"{element}:\n")
                self.help_text.tag_add("header2", current_position, end_index)
                self.help_text.tag_configure(
                    "header2", font=("Arial", 12, "bold"))
                current_position = self.help_text.index("insert")
                end_index = self.convert_index_to_end(current_position)
                self.help_text.insert(END, f"{help_info}\n\n")

    def _show_help_menu(self, event=None):
        """
        Shows the help menu
        """
        default_font = ("Arial", 12)
        screen_width = int(self.winfo_screenwidth() * 0.04)
        print(self.winfo_screenwidth())
        print(screen_width)
        screen_height = int(self.winfo_screenheight())

        self.help_popup = Toplevel(width=screen_width, height=screen_height)
        style = ttk.Style(self.help_popup)
        system_button_face_color = style.lookup("TButton", "background")
        default_font = ("Arial", 12)
        self.help_text = Text(self.help_popup, font=default_font, wrap="word", width=screen_width - 10,
                              height=screen_height - 10, borderwidth=0, highlightthickness=0, bg=system_button_face_color)
        self.help_text.pack(padx=20, pady=20)
        self._add_help_menu_items()
        close_button = Button(self.help_popup, text="Close",
                              command=self.help_popup.destroy)
        close_button.pack(pady=10)
        self.help_text.config(state="disabled")

    def _show_file_menu(self, event=None):
        """
        Shows the file dropdown menu: New, Save, Save As
        """
        self.file_menu.post(self.file_options_button.winfo_rootx(
        ), self.file_options_button.winfo_rooty() + self.file_options_button.winfo_height())

    def _show_edit_menu(self, event=None):
        """
        Shows the edit dropdown menu: Batch Processing
        """
        self.edit_menu.post(self.edit_options_button.winfo_rootx(
        ), self.edit_options_button.winfo_rooty() + self.edit_options_button.winfo_height())

    def _update_app_title(self):
        """
        Updates the app title to the current file name
        """
        if self.master.file_location is not None:
            self.master.master.title(
                f"Image Editor - {os.path.basename(self.master.file_location)}")
        else:
            self.master.master.title("Image Editor")

    def new_button_click(self, event=None):
        """
        Opens a file dialog to select a new image
        """
        fm = FileManager()
        fm.get_file()
        if fm.file is not None:
            self.my_file = fm.file
            self.master.file_location = fm.file
            image = cv2.imread(fm.file)
            self.master.master.original_image = image.copy()
            self.master.master.processed_image = image.copy()
            self.master.master.image_properties = ImageProperties()
            self._set_dimensions_of_image(image)
            self.master.master.history_of_edits._clear_history()
            self._insert_into_history(image)
            self.master.master.image_viewer._reset()
            self.master.master.image_viewer.display_image(image)
            self._update_metadata()
            self._update_app_title()

    def bytes_per_pixel(self, image):
        """
        Calculates the bytes per pixel of an image (color depth)
        """
        try:
            if isinstance(image, np.ndarray):
                channels = image.shape[-1] if len(image.shape) > 2 else 1
                bit_depth = image.dtype.itemsize * 8

                bytes_per_pixel = (bit_depth * channels + 7) // 8
            else:
                channels = len(image.getbands())
                bit_depth = getattr(image, 'bits', 8)
                bytes_per_pixel = (bit_depth * channels + 7) // 8

            return bytes_per_pixel
        except Exception as e:
            print(f"Error calculating bytes per pixel: {e}")
            return None

    def _update_metadata(self):
        """
        Updates the metadata labels when an image is imported
        """
        fm = FileManager()
        path = self.master.file_location
        fm.find_file(path)
        if fm.file is not None:
            try:
                with Image.open(fm.file) as img:
                    resolution = img.size
                    file_size = os.path.getsize(fm.file)
                    file_name = os.path.basename(fm.file)
                    file_extension = os.path.splitext(file_name)[1]
                    bytes_per_pixel = self.bytes_per_pixel(img)
                    zoom_resolution = (
                        int(resolution[0] * self.master.master.image_viewer.scale_factor),
                        int(resolution[1] * self.master.master.image_viewer.scale_factor))
            except Exception as e:
                print(f"Error reading image metadata: {e}")
        if self.master.master.processed_image is not None:
            resolution = (self.master.master.processed_image.shape[1], self.master.master.processed_image.shape[0])
            file_size = os.path.getsize(fm.file)
            file_name = os.path.basename(fm.file)
            file_extension = os.path.splitext(file_name)[1]
            bytes_per_pixel = self.bytes_per_pixel(self.master.master.processed_image)
            zoom_resolution = (
                int(resolution[0] * self.master.master.image_viewer.scale_factor),
                int(resolution[1] * self.master.master.image_viewer.scale_factor))
        self.master.master.editor_options.update_metadata_labels(file_size, resolution, file_name, file_extension, bytes_per_pixel, zoom_resolution)

    def _set_dimensions_of_image(self, img=None):
        """
        Sets the dimensions of the image when imported
        """
        image = img
        height, width = image.shape[:2]
        self.master.master.image_properties.original_image_height = height
        self.master.master.image_properties.original_image_width = width
        self.master.master.image_properties.altered_image_height = height
        self.master.master.image_properties.altered_image_width = width
        self.master.master.image_properties.resize_image_height = height
        self.master.master.image_properties.resize_image_width = width
        self.master.master.image_properties.zoom_image_height = height
        self.master.master.image_properties.zoom_image_width = width

    def save_button_click(self, event=None):
        """
        Saves the image to the current file location
        """
        fm = FileManager()
        path = self.master.file_location
        fm.find_file(path)

        if fm.file is not None:
            fm.save_file(self.master.master.processed_image)
            self.master.master.is_saved = True

    def save_as_button_click(self, event=None):
        """
        Opens a file dialog to save the image as a new file
        """
        fm = FileManager()
        path = self.master.file_location
        fm.find_file(path)

        if fm.file is not None:
            fm.save_as_file(self.master.master.processed_image)
            self.master.master.is_saved = True

    def batch_processing_button_click(self, event=None):
        """
        Opens a file dialog to select multiple images or a folder containing multiple images for batch processing
        """
        fm = FileManager()
        fm.get_files()

        if fm.batch_files is not None:
            for i in fm.batch_files:
                self.master.file_location = i
                image = cv2.imread(i)
                if image is None: # image failed to be read
                    print(f"Corrupt image at {i}\n")
                    continue

                self.master.master.original_image = image.copy()
                self.master.master.processed_image = image.copy()
                self._set_dimensions_of_image(image)

                self.master.master.image_viewer._apply_all_edits()

                fm = FileManager()
                path = self.master.file_location
                fm.find_file(path)

                if fm.file is not None:
                    fm.save_file(self.master.master.processed_image)
                    self.master.master.is_saved = True

    def _insert_into_history(self, img=None):
        """
        Inserts the current image into the history array
        """
        image = img
        height, width = image.shape[:2]
        title = "File Imported"
        import_instance = ImageProperties(
            title=title,
            time=str(time.strftime('%H:%M:%S')),
            is_flipped_horz=self.master.master.image_properties.is_flipped_horz,
            is_flipped_vert=self.master.master.image_properties.is_flipped_vert,
            is_grayscaled=self.master.master.image_properties.is_grayscaled,
            is_sepia=self.master.master.image_properties.is_sepia,
            is_cropped=self.master.master.image_properties.is_cropped,
            original_image_height=height,
            original_image_width=width,
            altered_image_height=height,
            altered_image_width=width,
            resize_image_height=height,
            resize_image_width=width,
            rotation=self.master.master.image_properties.rotation,
            brightness=self.master.master.image_properties.brightness,
            contrast=self.master.master.image_properties.contrast,
            saturation=self.master.master.image_properties.saturation,
            blur=self.master.master.image_properties.blur,
            hue=self.master.master.image_properties.hue,
            crop_start_x=self.master.master.image_properties.crop_start_x,
            crop_start_y=self.master.master.image_properties.crop_start_y,
            crop_end_x=self.master.master.image_properties.crop_end_x,
            crop_end_y=self.master.master.image_properties.crop_end_y,
            crop_ratio=self.master.master.image_properties.crop_ratio
        )
        self.master.master.history.append(import_instance)
        self.master.master.history_of_edits._set_indices()
        self.master.master.history_of_edits.update_history_list()

    def _reset_all_edits(self):
        """
        Resets all edits to the original image
        """
        self.master.master.processed_image = self.master.master.original_image
        self.master.master.image_viewer.display_image(
            self.master.master.processed_image)
        self.master.master.editor_options.reset_all_edits()
        self.master.master.editor_options.display_image(
            self.master.master.processed_image)
        self.master.master.image_properties = self.master.master.image_properties()
