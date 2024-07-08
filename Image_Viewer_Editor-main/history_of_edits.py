from tkinter import Frame, Button, END, LEFT, BOTH, YES, BOTTOM, X, TOP, CENTER
from tkinter import ttk


class History(Frame):
    def __init__(self, master=None):

        Frame.__init__(self, master=master, bg="#6b6b6b")

        # Fetches the history array from the master and sets initial indices
        self.history_arr = self.master.master.history
        self.history_length = 0
        self.current_index = 0
        self.starting_index = 0

        # Creates a frame for the history display
        history_frame = Frame(self, bg="#6b6b6b")
        history_frame.pack(side=TOP, fill=BOTH, expand=YES)

        # Sets up a Treeview widget for displaying history items
        self.history_tree = ttk.Treeview(history_frame, columns=(
            "Title", "Time"), show="headings", height=20)
        self.history_tree.pack(side=TOP, fill=BOTH, expand=YES)

        # Configures columns and headings for the Treeview
        self.history_tree.column("Title", width=150, anchor=CENTER)
        self.history_tree.column("Time", width=100, anchor=CENTER)
        self.history_tree.heading("Title", text="Edit")
        self.history_tree.heading("Time", text="Time")

        # Inserts existing history items into the Treeview
        for item in self.history_arr:
            self.history_tree.insert("", END, values=(item.title, item.time))

        # Binds a click event to the Treeview
        self.history_tree.bind("<ButtonRelease>", self._item_clicked)

        # Creates a frame for buttons related to undo and redo actions
        button_frame = Frame(history_frame, bg="#6b6b6b")
        button_frame.pack(side=BOTTOM, fill=X)

        # Buttons for undo and redo actions
        self.undo_edit_button = Button(button_frame, text="Undo")
        self.redo_edit_button = Button(button_frame, text="Redo")
        self.undo_edit_button.bind("<ButtonRelease>", self.undo_action)
        self.redo_edit_button.bind("<ButtonRelease>", self.redo_action)
        self.undo_edit_button.pack(side=LEFT)
        self.redo_edit_button.pack(side=LEFT)

    def _set_indices(self):
        """
        Sets the history length, current index, and starting index.
        """
        self.history_length = len(self.history_arr)
        self.current_index = self.history_length - 1
        self.starting_index = 0

    def _set_image_properties(self, property_instance):
        """
        Sets the image properties to the values from the property instance.

        Parameters:
            property_instance (Property): The property instance to retrieve values from.

        Returns:
            None
        """
        self.master.master.image_properties.title = property_instance.title
        self.master.master.image_properties.time = property_instance.time
        self.master.master.image_properties.is_flipped_horz = property_instance.is_flipped_horz
        self.master.master.image_properties.is_flipped_vert = property_instance.is_flipped_vert
        self.master.master.image_properties.is_grayscaled = property_instance.is_grayscaled
        self.master.master.image_properties.is_sepia = property_instance.is_sepia
        self.master.master.image_properties.is_cropped = property_instance.is_cropped
        self.master.master.image_properties.is_rotated = property_instance.is_rotated
        self.master.master.image_properties.is_resized = property_instance.is_resized
        self.master.master.image_properties.original_image_height = property_instance.original_image_height
        self.master.master.image_properties.original_image_width = property_instance.original_image_width
        self.master.master.image_properties.altered_image_height = property_instance.altered_image_height
        self.master.master.image_properties.altered_image_width = property_instance.altered_image_width
        self.master.master.image_properties.resize_image_height = property_instance.resize_image_height
        self.master.master.image_properties.resize_image_width = property_instance.resize_image_width
        self.master.master.image_properties.zoom_scale_factor = property_instance.zoom_scale_factor
        self.master.master.image_properties.rotation = property_instance.rotation
        self.master.master.image_properties.brightness = property_instance.brightness
        self.master.master.image_properties.contrast = property_instance.contrast
        self.master.master.image_properties.saturation = property_instance.saturation
        self.master.master.image_properties.blur = property_instance.blur
        self.master.master.image_properties.hue = property_instance.hue
        self.master.master.image_properties.crop_start_x = property_instance.crop_start_x
        self.master.master.image_properties.crop_start_y = property_instance.crop_start_y
        self.master.master.image_properties.crop_end_x = property_instance.crop_end_x
        self.master.master.image_properties.crop_end_y = property_instance.crop_end_y
        self.master.master.image_properties.crop_ratio = property_instance.crop_ratio
        self.master.master.image_properties.crop_rectangle_width = property_instance.crop_rectangle_width
        self.master.master.image_properties.crop_rectangle_height = property_instance.crop_rectangle_height
        self.master.master.image_properties.at_time_canvas_width = property_instance.at_time_canvas_width
        self.master.master.image_properties.at_time_canvas_height = property_instance.at_time_canvas_height

    def undo_action(self, event=None):
        """
        Performs an undo action by decrementing the current index and retrieving the property instance.

        Parameters:
            event (tkinter.Event): The event that triggered the undo action.

        Returns:
            None
        """
        if self.current_index > self.starting_index:
            self.master.master.undo_performed = True
            self.current_index -= 1
        property_instance = self.history_arr[self.current_index]
        self._set_image_properties(property_instance)
        self.update_displayed_image()

    def redo_action(self, event=None):
        """
        Performs a redo action by incrementing the current index and retrieving the property instance.

        Parameters:
            event (tkinter.Event): The event that triggered the redo action.

        Returns:
            None
        """
        if self.current_index < self.history_length - 1:
            self.current_index += 1
            property_instance = self.history_arr[self.current_index]
            self._set_image_properties(property_instance)
            self.update_displayed_image()
        else:
            print("No undo action to redo")

    def _item_clicked(self, event=None):
        """
        Handles a click on a history item by retrieving the property instance and setting the current index.

        Parameters:
            event (tkinter.Event): The event that triggered the item click.

        Returns:
            None
        """
        item = self.history_tree.selection()[0]
        index = self.history_tree.index(item)
        self.current_index = index
        if self.current_index > self.starting_index:
            self.master.master.undo_performed = True
        property_instance = self.history_arr[index]
        self._set_image_properties(property_instance)
        self.update_displayed_image()

    def update_history_list(self):
        """
        Updates the history list by deleting all items and inserting new items from the updated history array.
        """
        # Deletes all items from the Treeview
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Inserts new items from the updated history list into the Treeview
        for item in self.history_arr:
            self.history_tree.insert("", END, values=(item.title, item.time))

    def _clear_after_edit(self):
        """
        Clears the history array after the current index.
        """
        self.history_arr = self.history_arr[:self.current_index + 1]
        self.master.master.history = self.history_arr
        self.master.master.undo_performed = False
        self._set_indices()
        self.update_history_list()

    def update_displayed_image(self):
        """
        Updates the displayed image by applying all edits to the original image.
        """
        self.master.master.image_viewer._apply_all_edits()

    def _clear_history(self):
        """
        Clears the history array.
        """
        self.history_arr.clear()
        self.master.master.history = self.history_arr
        self._set_indices()
        self.update_history_list()
