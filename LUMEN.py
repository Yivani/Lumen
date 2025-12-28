import customtkinter as ctk
import os
import json
import shutil
import math
import sys
from datetime import datetime
from tkinter import filedialog

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- CONFIG & COLORS ---
COL_TEXT_LIGHT = "#dceabd"    
COL_TEXT_DARK  = "#141614"    
COL_ACCENT_GOLD= "#d9b84f"    
COL_BG_ROOT    = "#141614"    
COL_BG_PANEL   = "#1F221E"    
COL_BG_INPUT   = "#232621"    
COL_BORDER     = "#45483c"    
C_REN = "#d9b84f"
C_EXO = "#ceb9de"
C_RED = "#f22e00"
C_BIO = "#00b57c"
C_LIC = "#01f5ff"
C_REF = "#FFFFFF"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# --- THEMED POPUP SYSTEM ---
class ThemePopup(ctk.CTkToplevel):
    def __init__(self, title, message, color=COL_ACCENT_GOLD):
        super().__init__()
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(fg_color=COL_BG_ROOT)
        # Calculate position before setting geometry for better performance
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws - 420) // 2
        y = (hs - 240) // 2
        self.geometry(f'420x240+{x}+{y}')
        main_frame = ctk.CTkFrame(self, fg_color=COL_BG_PANEL, border_width=2, border_color=color, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(main_frame, text=title.upper(), font=("Impact", 24), text_color=color).pack(pady=(25, 10))
        ctk.CTkLabel(main_frame, text=message, font=("Arial", 13), text_color=COL_TEXT_LIGHT, wraplength=380).pack(pady=10)
        ctk.CTkButton(main_frame, text="ACKNOWLEDGE", command=self.destroy, fg_color=color, text_color=COL_TEXT_DARK, hover_color="#b59840", font=("Arial", 12, "bold"), width=140, height=40, corner_radius=2).pack(side="bottom", pady=25)
        self.grab_set()

class LumenIcarusEditor(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LUMEN EDITOR [v2.0]")
        w, h = 850, 1125
        ws, hs = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{int((ws/2)-(w/2))}+{int((hs/2)-(h/2))}")
        self.minsize(700, 700)
        self.configure(fg_color=COL_BG_ROOT)
        
        # --- CONFIGURATION ---
        self.config_file = "lumen_config.json"
        self.config = self.load_config()

        # --- SET WINDOW ICON (BUNDLED) ---
        icon_path = resource_path("logo.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        self.profiles_map = self.scan_for_profiles() 
        self.current_folder_path = None
        self.profile_data = {}
        
        # --- CHARACTER DATA ---
        self.char_root_container = None    
        self.char_list_ref = None          
        self.parsed_chars = []             
        self.active_char_index = -1
        self.char_frame = None            
        
        self.entries = {}
        self.xp_entry_ref = None
        self.lvl_entry_ref = None
        self.progress_bar_ref = None
        self.progress_label_ref = None
        
        # --- TAB SYSTEM ---
        self.tab_view = None
        self.editor_tab = None
        self.settings_tab = None
        
        self.create_widgets()
        # Defer profile loading to after() to improve initial window display speed
        if self.profiles_map:
            first_id = next(iter(self.profiles_map.keys()))  # Faster than list conversion
            self.profile_dropdown.set(first_id)
            self.after(100, lambda: self.change_profile(first_id))  # Defer loading
        else:
            self.status_label.configure(text="NO PROFILE - SELECT MANUALLY", text_color="#FF5555")
            self.btn_save.configure(state="disabled")
            self.btn_save_launch.configure(state="disabled")
            self.after(200, lambda: self.show_message("NO PROFILE FOUND", "Could not auto-detect profiles.\nPlease click [ BROWSE ] and select your PlayerData folder manually.", "#FF5555"))

    def load_config(self):
        """Load configuration from JSON file or create default."""
        default_backup = os.path.join(os.path.expanduser('~'), 'Documents', 'LUMEN_BACKUP')
        default_config = {"backup_path": default_backup, "max_backups": 10, "close_on_launch": False}
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                # Ensure required keys exist in loaded config
                loaded_config.setdefault("max_backups", 10)
                loaded_config.setdefault("close_on_launch", False)
                return loaded_config
            except (json.JSONDecodeError, IOError, OSError):
                return default_config
        return default_config

    def save_config(self):
        """Save current configuration to JSON file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Failed to save config: {e}")

    def show_message(self, title, msg, color=COL_ACCENT_GOLD):
        ThemePopup(title, msg, color)

    def scan_for_profiles(self):
        appdata = os.getenv('LOCALAPPDATA')
        if not appdata: return {}
        base_path = os.path.join(appdata, 'Icarus', 'Saved', 'PlayerData')
        profiles = {}
        if os.path.exists(base_path):
            try:
                # Use listdir with error handling for better performance
                for folder in os.listdir(base_path):
                    if folder.isdigit():
                        full_path = os.path.join(base_path, folder)
                        if os.path.isdir(full_path):
                            profiles[folder] = full_path
            except (PermissionError, OSError):
                pass
        return profiles

    def browse_folder(self):
        folder_selected = filedialog.askdirectory(title="SELECT ICARUS PLAYER DATA FOLDER")
        if folder_selected:
            p_check = os.path.join(folder_selected, "Profile.json")
            if os.path.exists(p_check):
                folder_name = os.path.basename(folder_selected)
                self.profiles_map[folder_name] = folder_selected
                self.profile_dropdown.configure(values=list(self.profiles_map.keys()))
                self.profile_dropdown.set(folder_name)
                self.current_folder_path = folder_selected
                self.load_data()
                self.btn_save.configure(state="normal")
                self.btn_save_launch.configure(state="normal")
                self.show_message("SUCCESS", f"Profile loaded successfully:\n{folder_name}")
            else:
                self.show_message("INVALID FOLDER", "Folder must contain Profile.json!", "#FF5555")

    def create_widgets(self):
        self.header_frame = ctk.CTkFrame(self, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER, corner_radius=0, height=80)
        self.header_frame.pack(fill="x", side="top", padx=1, pady=1)
        ctk.CTkLabel(self.header_frame, text="LUMEN // EDITOR", font=("Impact", 28), text_color=COL_TEXT_LIGHT).pack(side="left", padx=30, pady=20)
        ctrl_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        ctrl_frame.pack(side="right", padx=30)
        self.btn_browse = ctk.CTkButton(ctrl_frame, text="[ BROWSE ]", width=100, command=self.browse_folder, fg_color=COL_BG_INPUT, hover_color=COL_BORDER, border_width=1, border_color=COL_BORDER, text_color=COL_TEXT_LIGHT)
        self.btn_browse.pack(side="right", padx=10)
        self.profile_dropdown = ctk.CTkOptionMenu(ctrl_frame, values=list(self.profiles_map.keys()) if self.profiles_map else ["NO PROFILE"], command=self.change_profile, width=200, fg_color=COL_BG_INPUT, button_color=COL_BORDER, button_hover_color=COL_ACCENT_GOLD, text_color=COL_TEXT_LIGHT, dropdown_fg_color=COL_BG_PANEL, dropdown_text_color=COL_TEXT_LIGHT, corner_radius=2)
        self.profile_dropdown.pack(side="right", padx=5)
        ctk.CTkLabel(ctrl_frame, text="ID:", font=("Arial", 10, "bold"), text_color=COL_BORDER).pack(side="right", padx=5)
        
        # --- TABVIEW CONTAINER ---
        self.tab_view = ctk.CTkTabview(
            self, width=800, height=600, corner_radius=2, 
            fg_color=COL_BG_ROOT, 
            segmented_button_fg_color=COL_BG_INPUT, 
            segmented_button_selected_color=COL_ACCENT_GOLD, 
            segmented_button_selected_hover_color="#b59840", 
            segmented_button_unselected_color=COL_BG_INPUT, 
            segmented_button_unselected_hover_color=COL_BORDER, 
            text_color=COL_TEXT_LIGHT
        )
        self.tab_view.pack(pady=10, padx=20, fill="both", expand=True)
        self.tab_view._segmented_button.configure(font=("Impact", 18), text_color_disabled=COL_BORDER)
        
        self.editor_tab = self.tab_view.add("EDITOR")
        self.settings_tab = self.tab_view.add("SETTINGS")
        
        # --- EDITOR TAB CONTENT ---
        self.frame = ctk.CTkScrollableFrame(self.editor_tab, corner_radius=0, fg_color="transparent")
        self.frame.pack(fill="both", expand=True)
        
        # --- SETTINGS TAB CONTENT ---
        self.create_settings_ui()

        self.footer_frame = ctk.CTkFrame(self, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER, corner_radius=0, height=90)
        self.footer_frame.pack(fill="x", side="bottom", padx=1, pady=1)
        self.status_label = ctk.CTkLabel(self.footer_frame, text="WAITING...", font=("Consolas", 12), text_color=COL_BORDER)
        self.status_label.pack(side="left", padx=30)
        self.btn_save_launch = ctk.CTkButton(self.footer_frame, text="[ SAVE & LAUNCH GAME ]", command=self.save_and_launch_game, width=200, height=45, font=("Arial", 13, "bold"), fg_color=C_BIO, hover_color="#008f62", text_color=COL_TEXT_DARK, corner_radius=2)
        self.btn_save_launch.pack(side="right", padx=10, pady=20)
        self.btn_save = ctk.CTkButton(self.footer_frame, text="[ SAVE & APPLY ]", command=self.save_data, width=220, height=45, font=("Arial", 13, "bold"), fg_color=COL_ACCENT_GOLD, hover_color="#b59840", text_color=COL_TEXT_DARK, corner_radius=2)
        self.btn_save.pack(side="right", padx=10, pady=20)
        self.btn_refresh = ctk.CTkButton(self.footer_frame, text="RELOAD", command=self.refresh_current_profile, width=100, height=45, font=("Arial", 12, "bold"), fg_color=COL_BG_INPUT, hover_color=COL_BORDER, text_color=COL_TEXT_LIGHT, border_width=1, border_color=COL_BORDER, corner_radius=2)
        self.btn_refresh.pack(side="right", padx=10)

    def create_settings_ui(self):
        """Create the UI elements for the Settings tab."""
        content = ctk.CTkScrollableFrame(self.settings_tab, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # --- BACKUP SECTION ---
        backup_header = ctk.CTkFrame(content, fg_color="transparent")
        backup_header.pack(fill="x", pady=(0, 5))
        ctk.CTkFrame(backup_header, width=3, height=18, fg_color=COL_ACCENT_GOLD, corner_radius=0).pack(side="left")
        ctk.CTkLabel(backup_header, text="BACKUP", font=("Arial", 16, "bold"), text_color=COL_TEXT_LIGHT).pack(side="left", padx=10)
        ctk.CTkFrame(content, height=1, fg_color=COL_BORDER, corner_radius=0).pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(content, text="BACKUP LOCATION", font=("Arial", 12, "bold"), text_color=COL_ACCENT_GOLD).pack(anchor="w", pady=(0, 5))
        
        self.path_frame = ctk.CTkFrame(content, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER)
        self.path_frame.pack(fill="x", pady=(0, 15))
        
        self.lbl_backup_path = ctk.CTkLabel(self.path_frame, text=self.config.get("backup_path", ""), font=("Consolas", 12), text_color=COL_TEXT_LIGHT, wraplength=500)
        self.lbl_backup_path.pack(side="left", padx=15, pady=10)
        
        ctk.CTkButton(self.path_frame, text="CHANGE", command=self.change_backup_folder, width=80, height=30, fg_color=COL_BG_INPUT, hover_color=COL_BORDER, text_color=COL_TEXT_LIGHT).pack(side="right", padx=10, pady=10)
        
        ctk.CTkLabel(content, text="BACKUP RETENTION", font=("Arial", 12, "bold"), text_color=COL_ACCENT_GOLD).pack(anchor="w", pady=(0, 5))
        
        retention_frame = ctk.CTkFrame(content, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER)
        retention_frame.pack(fill="x", pady=(0, 15))
        
        retention_content = ctk.CTkFrame(retention_frame, fg_color="transparent")
        retention_content.pack(fill="x", padx=20, pady=12)
        
        header_row = ctk.CTkFrame(retention_content, fg_color="transparent")
        header_row.pack(fill="x", pady=(0, 6))
        
        ctk.CTkLabel(header_row, text="Max Backups to Keep", font=("Arial", 12, "bold"), text_color=COL_TEXT_LIGHT).pack(side="left")
        
        value_display = ctk.CTkFrame(header_row, fg_color=COL_BG_INPUT, corner_radius=4)
        value_display.pack(side="right")
        self.max_backups_label = ctk.CTkLabel(
            value_display, text=str(int(self.config.get("max_backups", 10))),
            font=("Consolas", 14, "bold"), text_color=COL_ACCENT_GOLD, width=45
        )
        self.max_backups_label.pack(padx=10, pady=4)
        
        slider_row = ctk.CTkFrame(retention_content, fg_color="transparent")
        slider_row.pack(fill="x", pady=(0, 4))
        
        ctk.CTkLabel(slider_row, text="5", font=("Arial", 10), text_color=COL_BORDER).pack(side="left", padx=(0, 10))
        
        self.max_backups_slider = ctk.CTkSlider(
            slider_row, from_=5, to=50, number_of_steps=45,
            command=self.update_backup_limit_label, width=300,
            progress_color=COL_ACCENT_GOLD, button_color=COL_ACCENT_GOLD,
            button_hover_color="#b59840", fg_color=COL_BG_INPUT
        )
        self.max_backups_slider.set(self.config.get("max_backups", 10))
        self.max_backups_slider.pack(side="left", fill="x", expand=True, padx=5)
        
        ctk.CTkLabel(slider_row, text="50", font=("Arial", 10), text_color=COL_BORDER).pack(side="left", padx=(10, 0))
        
        ctk.CTkLabel(retention_content, text="Oldest backups are automatically deleted when limit is exceeded", font=("Arial", 10), text_color=COL_BORDER).pack(anchor="w", pady=(2, 0))
        
        tools_frame = ctk.CTkFrame(content, fg_color="transparent")
        tools_frame.pack(fill="x", pady=(0, 30))
        
        ctk.CTkButton(tools_frame, text="OPEN BACKUP FOLDER", command=self.open_backup_folder, fg_color=COL_BG_INPUT, hover_color=COL_BORDER, text_color=COL_TEXT_LIGHT).pack(side="left", padx=(0, 10))
        ctk.CTkButton(tools_frame, text="DELETE ALL BACKUPS", command=self.delete_all_backups, fg_color=C_RED, hover_color="#b52200", text_color=COL_TEXT_DARK).pack(side="left")
        
        # --- IMPORTANT SETTINGS SECTION ---
        settings_header = ctk.CTkFrame(content, fg_color="transparent")
        settings_header.pack(fill="x", pady=(0, 5))
        ctk.CTkFrame(settings_header, width=3, height=18, fg_color=COL_ACCENT_GOLD, corner_radius=0).pack(side="left")
        ctk.CTkLabel(settings_header, text="IMPORTANT SETTINGS", font=("Arial", 16, "bold"), text_color=COL_TEXT_LIGHT).pack(side="left", padx=10)
        ctk.CTkFrame(content, height=1, fg_color=COL_BORDER, corner_radius=0).pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(content, text="STEAM CLOUD GUARD", font=("Arial", 12, "bold"), text_color=COL_ACCENT_GOLD).pack(anchor="w", pady=(0, 5))
        
        steam_frame = ctk.CTkFrame(content, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER)
        steam_frame.pack(fill="x", pady=(0, 15))
        
        steam_content = ctk.CTkFrame(steam_frame, fg_color="transparent")
        steam_content.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(steam_content, text="⚠ WARNING: Disable Steam Cloud Sync before saving!", font=("Arial", 12, "bold"), text_color=C_RED).pack(anchor="w", pady=(0, 5))
        ctk.CTkLabel(steam_content, text="Steam Cloud may overwrite manual JSON edits. Disable it in:\nSteam → Library → Right-click Icarus → Properties → General → Steam Cloud", font=("Arial", 11), text_color=COL_BORDER, justify="left").pack(anchor="w")
        
        ctk.CTkLabel(content, text="CLOSE ON LAUNCH", font=("Arial", 12, "bold"), text_color=COL_ACCENT_GOLD).pack(anchor="w", pady=(0, 5))
        
        close_frame = ctk.CTkFrame(content, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER)
        close_frame.pack(fill="x", pady=(0, 15))
        
        close_content = ctk.CTkFrame(close_frame, fg_color="transparent")
        close_content.pack(fill="x", padx=20, pady=20)
        
        toggle_row = ctk.CTkFrame(close_content, fg_color="transparent")
        toggle_row.pack(fill="x", pady=(0, 10))
        
        label_frame = ctk.CTkFrame(toggle_row, fg_color="transparent")
        label_frame.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(label_frame, text="Close Editor when Game Starts", font=("Arial", 12, "bold"), text_color=COL_TEXT_LIGHT).pack(anchor="w")
        ctk.CTkLabel(label_frame, text="Automatically close the editor after launching Icarus", font=("Arial", 10), text_color=COL_BORDER).pack(anchor="w", pady=(2, 0))
        
        switch_frame = ctk.CTkFrame(toggle_row, fg_color="transparent")
        switch_frame.pack(side="right", padx=(20, 0))
        
        self.close_status_label = ctk.CTkLabel(
            switch_frame, text="OFF", font=("Arial", 10, "bold"),
            text_color=COL_BORDER, width=40
        )
        self.close_status_label.pack(side="right", padx=(0, 10))
        
        self.close_on_launch_switch = ctk.CTkSwitch(
            switch_frame, text="", command=self.toggle_close_on_launch,
            onvalue=True, offvalue=False, width=60, height=28,
            progress_color=C_BIO, button_color=COL_TEXT_LIGHT,
            button_hover_color=COL_ACCENT_GOLD, fg_color=COL_BG_INPUT
        )
        self.close_on_launch_switch.pack(side="right")
        
        if self.config.get("close_on_launch", False):
            self.close_on_launch_switch.select()
            self.close_status_label.configure(text="ON", text_color=C_BIO)
        else:
            self.close_on_launch_switch.deselect()
            self.close_status_label.configure(text="OFF", text_color=COL_BORDER)
        
        ctk.CTkLabel(content, text="JSON INTEGRITY CHECK", font=("Arial", 12, "bold"), text_color=COL_ACCENT_GOLD).pack(anchor="w", pady=(0, 5))
        
        validate_frame = ctk.CTkFrame(content, fg_color="transparent")
        validate_frame.pack(fill="x", pady=(0, 0))
        
        ctk.CTkButton(validate_frame, text="VALIDATE FILES", command=self.validate_json_files, fg_color=C_BIO, hover_color="#008f62", text_color=COL_TEXT_DARK, font=("Arial", 12, "bold")).pack(side="left")
        ctk.CTkLabel(validate_frame, text="Scan JSON files for syntax errors before saving", font=("Arial", 11), text_color=COL_BORDER).pack(side="left", padx=15)

    def validate_json_files(self):
        """Validate JSON integrity of Profile and Characters files."""
        if not self.current_folder_path:
            self.show_message("NO PROFILE", "Please load a profile first.", "#FF5555")
            return
        
        errors = []
        
        p_path = os.path.join(self.current_folder_path, 'Profile.json')
        if os.path.exists(p_path):
            try:
                with open(p_path, 'r', encoding='utf-8') as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                errors.append(f"Profile.json: {str(e)}")
        else:
            errors.append("Profile.json: File not found")
        
        c_path = os.path.join(self.current_folder_path, 'Characters.json')
        if os.path.exists(c_path):
            try:
                with open(c_path, 'r', encoding='utf-8') as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                errors.append(f"Characters.json: {str(e)}")
        else:
            errors.append("Characters.json: File not found")
        
        if errors:
            error_msg = "\n".join(errors)
            self.show_message("VALIDATION FAILED", f"JSON syntax errors detected:\n\n{error_msg}", "#FF5555")
        else:
            self.show_message("VALIDATION PASSED", "All JSON files are valid!\nNo syntax errors detected.", C_BIO)

    def update_backup_limit_label(self, value):
        """Update the label showing current max backups value."""
        self.max_backups_label.configure(text=str(int(value)))
        self.config["max_backups"] = int(value)
        self.save_config()

    def toggle_close_on_launch(self):
        """Toggle the close on launch setting."""
        is_enabled = self.close_on_launch_switch.get()
        self.config["close_on_launch"] = is_enabled
        self.save_config()
        
        if is_enabled:
            self.close_status_label.configure(text="ON", text_color=C_BIO)
        else:
            self.close_status_label.configure(text="OFF", text_color=COL_BORDER)

    def cleanup_old_backups(self):
        """Delete oldest backups if count exceeds max_backups limit."""
        backup_base = self.config.get("backup_path")
        if not backup_base or not os.path.exists(backup_base):
            return
        
        max_backups = self.config.get("max_backups", 10)
        
        try:
            backup_folders = []
            for item in os.listdir(backup_base):
                full_path = os.path.join(backup_base, item)
                if os.path.isdir(full_path) and item.startswith("Backup_"):
                    try:
                        timestamp_str = item.replace("Backup_", "")
                        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S")
                        backup_folders.append((timestamp, full_path, item))
                    except:
                        mtime = os.path.getmtime(full_path)
                        backup_folders.append((datetime.fromtimestamp(mtime), full_path, item))
            
            backup_folders.sort(key=lambda x: x[0])
            
            if len(backup_folders) >= max_backups:
                to_delete = len(backup_folders) - max_backups + 1  # +1 to make room for new backup
                deleted_count = 0
                for _, full_path, item in backup_folders[:to_delete]:
                    try:
                        shutil.rmtree(full_path)
                        deleted_count += 1
                    except Exception as e:
                        print(f"Failed to delete backup {item}: {e}")
                
                if deleted_count > 0:
                    self.status_label.configure(text=f"AUTO-CLEANED {deleted_count} OLD BACKUP(S)", text_color=COL_BORDER)
        except Exception as e:
            print(f"Error cleaning up backups: {e}")

    def change_backup_folder(self):
        folder = filedialog.askdirectory(title="SELECT BACKUP FOLDER")
        if folder:
            self.config["backup_path"] = folder
            self.save_config()
            self.lbl_backup_path.configure(text=folder)
            self.show_message("UPDATED", "Backup location updated successfully!")

    def open_backup_folder(self):
        path = self.config.get("backup_path")
        if path and os.path.exists(path):
            os.startfile(path)
        else:
            self.show_message("ERROR", "Backup folder does not exist!", "#FF5555")

    def delete_all_backups(self):
        path = self.config.get("backup_path")
        if not path or not os.path.exists(path): return
        
        try:
            count = 0
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path) and item.startswith("Backup_"):
                    shutil.rmtree(full_path)
                    count += 1
            self.show_message("SUCCESS", f"Deleted {count} backup folders.", C_BIO)
        except Exception as e:
            self.show_message("ERROR", f"Failed to delete backups:\n{e}", "#FF5555")

    def change_profile(self, selected_id):
        if selected_id in self.profiles_map:
            self.current_folder_path = self.profiles_map[selected_id]
            self.load_data()
        else:
            self.current_folder_path = None

    def refresh_current_profile(self):
        if self.current_folder_path:
            self.load_data()
            self.status_label.configure(text="DATA RELOADED", text_color=C_LIC)

    def clear_ui(self):
        for widget in self.frame.winfo_children(): widget.destroy()
        self.entries.clear()
        self.char_frame = None

    def add_section_header(self, text):
        """Create a styled section header with accent bar."""
        container = ctk.CTkFrame(self.frame, fg_color="transparent")
        container.pack(fill="x", pady=(25, 5), padx=30)
        ctk.CTkFrame(container, width=3, height=18, fg_color=COL_ACCENT_GOLD, corner_radius=0).pack(side="left")
        ctk.CTkLabel(container, text=text, font=("Arial", 16, "bold"), text_color=COL_TEXT_LIGHT).pack(side="left", padx=10)
        ctk.CTkFrame(self.frame, height=1, fg_color=COL_BORDER, corner_radius=0).pack(fill="x", padx=30, pady=0)

    def add_input_field(self, label_text, key_id, value, section, icon_color=None):
        """Create a labeled input field with optional colored accent bar."""
        row = ctk.CTkFrame(self.frame, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER, corner_radius=2)
        row.pack(fill="x", pady=4, padx=30)
        
        if icon_color: ctk.CTkFrame(row, width=4, height=45, corner_radius=0, fg_color=icon_color).pack(side="left")
        else: ctk.CTkFrame(row, width=4, height=45, corner_radius=0, fg_color="transparent").pack(side="left")

        ctk.CTkLabel(row, text=label_text.upper(), font=("Arial", 11, "bold"), text_color=COL_TEXT_LIGHT, anchor="w", width=220).pack(side="left", padx=15)
        
        entry = ctk.CTkEntry(
            row, font=("Consolas", 15), fg_color=COL_BG_INPUT, border_width=0, corner_radius=0,
            text_color=COL_TEXT_LIGHT, justify="right"
        )
        val_str = str(value) if value is not None else "0"
        entry.insert(0, val_str)
        entry.pack(side="right", padx=15, pady=10, fill="x", expand=True)
        
        self.entries[f"{section}|{key_id}"] = entry
        return entry

    def switch_character(self, selection):
        """Switch the active character and refresh the character UI section."""
        if not self.parsed_chars: return
        
        selected_idx = 0
        for i, char_data in enumerate(self.parsed_chars):
            name = char_data['obj'].get('CharacterName', 'UNKNOWN').upper()
            if name == selection:
                selected_idx = i
                break
        
        self.active_char_index = selected_idx
        self.render_character_ui()

    def render_character_ui(self):
        """Render the stats/level manager for the currently active character."""
        if self.active_char_index < 0 or self.active_char_index >= len(self.parsed_chars): return
        
        if self.char_frame is None:
            self.char_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
            self.char_frame.pack(fill="x", padx=0, pady=0)
        
        for widget in self.char_frame.winfo_children(): widget.destroy()
        
        keys_to_remove = [k for k in self.entries.keys() if k.startswith("CHAR|")]
        for k in keys_to_remove: del self.entries[k]

        char_data = self.parsed_chars[self.active_char_index]
        char_obj = char_data['obj']
        name = char_obj.get("CharacterName", "UNKNOWN").upper()
        
        container = ctk.CTkFrame(self.char_frame, fg_color="transparent")
        container.pack(fill="x", pady=(25, 5), padx=30)
        ctk.CTkFrame(container, width=3, height=18, fg_color=COL_ACCENT_GOLD, corner_radius=0).pack(side="left")
        ctk.CTkLabel(container, text=f"CHARACTER: {name}", font=("Arial", 16, "bold"), text_color=COL_TEXT_LIGHT).pack(side="left", padx=10)
        
        if len(self.parsed_chars) > 1:  # Only show dropdown if multiple characters
            char_names = [c['obj'].get('CharacterName', 'UNKNOWN').upper() for c in self.parsed_chars]
            sel_container = ctk.CTkFrame(container, fg_color="transparent")
            sel_container.pack(side="right")
            ctk.CTkLabel(sel_container, text="SELECT:", font=("Arial", 10, "bold"), text_color=COL_BORDER).pack(side="left", padx=(0, 5))
            char_dropdown = ctk.CTkOptionMenu(
                sel_container, values=char_names, command=self.switch_character,
                width=200, fg_color=COL_BG_INPUT, button_color=COL_BORDER,
                button_hover_color=COL_ACCENT_GOLD, text_color=COL_TEXT_LIGHT,
                dropdown_fg_color=COL_BG_PANEL, dropdown_text_color=COL_TEXT_LIGHT
            )
            char_dropdown.set(name)
            char_dropdown.pack(side="left")
        
        ctk.CTkFrame(self.char_frame, height=1, fg_color=COL_BORDER, corner_radius=0).pack(fill="x", padx=30, pady=0)

        is_dead = char_obj.get("IsDead", False)
        is_abandoned = char_obj.get("IsAbandoned", False)
        self.add_revive_manager(is_dead, is_abandoned, parent=self.char_frame)
        
        current_xp = char_obj.get("XP", 0)
        current_xp_debt = char_obj.get("XP_Debt", 0)
        self.add_level_manager(current_xp, current_xp_debt, "CHAR", parent=self.char_frame)

    def add_revive_manager(self, is_dead, is_abandoned, parent=None):
        """Add character revive/rescue UI with revive button."""
        target = parent if parent else self.frame
        container = ctk.CTkFrame(target, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER, corner_radius=2)
        container.pack(fill="x", pady=5, padx=30)
        
        head = ctk.CTkFrame(container, fg_color="transparent")
        head.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(head, text="REVIVE & RESCUE", font=("Arial", 11, "bold"), text_color=C_BIO).pack(side="left")
        
        content = ctk.CTkFrame(container, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=(0, 15))
        
        status_parts = []
        if is_dead:
            status_parts.append("DEAD")
        if is_abandoned:
            status_parts.append("ABANDONED")
        status_text = " | ".join(status_parts) if status_parts else "ALIVE"
        status_color = C_RED if (is_dead or is_abandoned) else C_BIO
        
        status_label = ctk.CTkLabel(content, text=f"Status: {status_text}", font=("Consolas", 14), text_color=status_color)
        status_label.pack(side="left", padx=(0, 20))
        
        def revive_character():
            if self.active_char_index < 0 or self.active_char_index >= len(self.parsed_chars):
                self.show_message("ERROR", "No character selected!", "#FF5555")
                return
            
            char_data = self.parsed_chars[self.active_char_index]
            char_obj = char_data['obj']
            
            was_dead = char_obj.get("IsDead", False)
            was_abandoned = char_obj.get("IsAbandoned", False)
            
            if not was_dead and not was_abandoned:
                self.show_message("ALREADY ALIVE", "Character is already alive and not abandoned.", COL_ACCENT_GOLD)
                return
            
            char_obj["IsDead"] = False
            char_obj["IsAbandoned"] = False
            
            c_path = os.path.join(self.current_folder_path, 'Characters.json')
            if not os.path.exists(c_path):
                self.show_message("ERROR", "Characters.json not found!", "#FF5555")
                return
            
            try:
                shutil.copy(c_path, c_path + ".backup")
                
                final_element = char_obj
                if char_data['is_encoded']:
                    final_element = json.dumps(char_obj)
                
                if char_data['is_nested']:
                    self.char_list_ref[self.active_char_index][0] = final_element
                else:
                    self.char_list_ref[self.active_char_index] = final_element
                
                with open(c_path, 'w', encoding='utf-8') as f:
                    json.dump(self.char_root_container, f, indent=4)
                
                status_label.configure(text="Status: ALIVE", text_color=C_BIO)
                self.status_label.configure(text="CHARACTER REVIVED & RESCUED", text_color=C_BIO)
                
                msg_parts = []
                if was_dead:
                    msg_parts.append("Revived from death")
                if was_abandoned:
                    msg_parts.append("Rescued from abandonment")
                msg = "\n".join(msg_parts) + "\n\nRestart game to see changes."
                
                self.show_message("SUCCESS", msg, C_BIO)
            except PermissionError:
                self.show_message("SAVE FAILED", "File is locked by Icarus.\nPlease close the game.", "#FF5555")
            except Exception as e:
                self.show_message("ERROR", f"Failed to revive character:\n{e}", "#FF5555")
        
        ctk.CTkButton(content, text="REVIVE & RESCUE", command=revive_character, width=160, height=35, corner_radius=2, fg_color=C_BIO, hover_color="#008f62", text_color=COL_TEXT_DARK, font=("Arial", 11, "bold")).pack(side="left")

    def add_level_manager(self, current_xp, current_xp_debt, section, parent=None):
        target = parent if parent else self.frame
        container = ctk.CTkFrame(target, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER, corner_radius=2)
        container.pack(fill="x", pady=5, padx=30)
        
        head = ctk.CTkFrame(container, fg_color="transparent")
        head.pack(fill="x", padx=15, pady=(5, 2))
        ctk.CTkLabel(head, text="LEVEL MANAGER", font=("Arial", 11, "bold"), text_color=COL_ACCENT_GOLD).pack(side="left")
        
        content_frame = ctk.CTkFrame(container, fg_color=COL_BG_PANEL, corner_radius=2)
        content_frame.pack(fill="both", padx=10, pady=(0, 10))
        
        controls = ctk.CTkFrame(content_frame, fg_color="transparent")
        controls.pack(fill="x", padx=10, pady=(10, 0))
        
        input_row = ctk.CTkFrame(controls, fg_color="transparent")
        input_row.pack(fill="x", pady=(0, 8))
        
        left_box = ctk.CTkFrame(input_row, fg_color="transparent")
        left_box.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(left_box, text="TARGET LEVEL", font=("Arial", 9, "bold"), text_color=COL_BORDER).pack(anchor="w", pady=(0, 2))
        self.lvl_entry_ref = ctk.CTkEntry(left_box, width=60, font=("Consolas", 14), fg_color=COL_BG_INPUT, border_width=0, justify="center", text_color=COL_TEXT_LIGHT)
        self.lvl_entry_ref.pack(side="left", pady=0)
        ctk.CTkButton(left_box, text="CALC XP ->", width=90, command=self.calc_xp_from_lvl, corner_radius=2, fg_color=COL_BORDER, hover_color=COL_BG_INPUT, text_color=COL_TEXT_LIGHT).pack(side="left", padx=5)
        
        right_box = ctk.CTkFrame(input_row, fg_color="transparent")
        right_box.pack(side="right", fill="x", expand=True)
        ctk.CTkLabel(right_box, text="CUSTOM XP", font=("Arial", 9, "bold"), text_color=COL_BORDER).pack(anchor="w", pady=(0, 2))
        self.xp_entry_ref = ctk.CTkEntry(right_box, font=("Consolas", 14), fg_color=COL_BG_INPUT, border_width=0, justify="right", text_color=COL_TEXT_LIGHT)
        self.xp_entry_ref.insert(0, str(current_xp))
        self.xp_entry_ref.pack(side="left", fill="x", expand=True, pady=0)
        ctk.CTkButton(right_box, text="<- GET LVL", width=90, command=self.calc_lvl_from_xp, corner_radius=2, fg_color=COL_BORDER, hover_color=COL_BG_INPUT, text_color=COL_TEXT_LIGHT).pack(side="left", padx=5)
        
        self.entries[f"{section}|XP"] = self.xp_entry_ref
        
        def reset_to_zero():
            self.xp_entry_ref.delete(0, "end")
            self.xp_entry_ref.insert(0, "0")
            self.lvl_entry_ref.delete(0, "end")
            self.lvl_entry_ref.insert(0, "1")
            self.update_progress_visuals(0)
            self.status_label.configure(text="PRESTIGE MODE: RESET TO LEVEL 1 (TALENTS PRESERVED)", text_color=C_BIO)
        
        def set_softcap():
            softcap_xp = 3890000
            self.xp_entry_ref.delete(0, "end")
            self.xp_entry_ref.insert(0, str(softcap_xp))
            self.lvl_entry_ref.delete(0, "end")
            self.lvl_entry_ref.insert(0, "50")
            self.update_progress_visuals(softcap_xp)
            self.status_label.configure(text="SET TO LEVEL 50 SOFT-CAP", text_color=COL_ACCENT_GOLD)
        
        preset_header = ctk.CTkFrame(controls, fg_color="transparent")
        preset_header.pack(fill="x", pady=(10, 2))
        ctk.CTkLabel(preset_header, text="PRESTIGE TOOLS", font=("Arial", 9, "bold"), text_color=COL_ACCENT_GOLD).pack(side="left")
        ctk.CTkLabel(preset_header, text="(Keeps talents & blueprints)", font=("Arial", 8), text_color=COL_BORDER).pack(side="left", padx=(8, 0))
        ctk.CTkLabel(preset_header, text="XP DEBT", font=("Arial", 9, "bold"), text_color=C_RED).pack(side="right")
        
        presets_row = ctk.CTkFrame(controls, fg_color="transparent")
        presets_row.pack(fill="x", pady=(0, 0))
        
        prestige_left = ctk.CTkFrame(presets_row, fg_color="transparent")
        prestige_left.pack(side="left")
        ctk.CTkButton(prestige_left, text="SOFT-RESET (LVL 1)", command=reset_to_zero, width=130, height=28, corner_radius=2, fg_color=C_RED, hover_color="#b52200", text_color=COL_TEXT_DARK, font=("Arial", 10, "bold")).pack(side="left", padx=(0, 6))
        ctk.CTkButton(prestige_left, text="SOFT-CAP (LVL 50)", command=set_softcap, width=130, height=28, corner_radius=2, fg_color=C_BIO, hover_color="#008f62", text_color=COL_TEXT_DARK, font=("Arial", 10, "bold")).pack(side="left")
        
        debt_content = ctk.CTkFrame(presets_row, fg_color="transparent")
        debt_content.pack(side="right")
        
        debt_label = ctk.CTkLabel(debt_content, text=f"Debt: {current_xp_debt}", font=("Consolas", 11), text_color=COL_TEXT_LIGHT)
        debt_label.pack(side="left", padx=(0, 8))
        
        xp_debt_entry = ctk.CTkEntry(debt_content, width=0, height=0, fg_color=COL_BG_INPUT, border_width=0)
        xp_debt_entry.insert(0, str(current_xp_debt))
        self.entries[f"{section}|XP_Debt"] = xp_debt_entry
        
        def clear_debt():
            xp_debt_entry.delete(0, "end")
            xp_debt_entry.insert(0, "0")
            debt_label.configure(text="Debt: 0")
            self.status_label.configure(text="XP DEBT CLEARED", text_color=C_BIO)
        
        ctk.CTkButton(debt_content, text="CLEAR", command=clear_debt, width=80, height=28, corner_radius=2, fg_color=C_RED, hover_color="#b52200", text_color=COL_TEXT_DARK, font=("Arial", 10, "bold")).pack(side="left")
        
        bar_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        bar_frame.pack(fill="x", padx=15, pady=(12, 15))
        self.progress_label_ref = ctk.CTkLabel(bar_frame, text="LEVEL PROGRESS", font=("Arial", 10, "bold"), text_color=COL_TEXT_LIGHT, anchor="w")
        self.progress_label_ref.pack(fill="x", pady=(0, 4))
        self.progress_bar_ref = ctk.CTkProgressBar(bar_frame, height=14, corner_radius=0, fg_color=COL_BORDER, progress_color=COL_TEXT_LIGHT)
        self.progress_bar_ref.set(0)
        self.progress_bar_ref.pack(fill="x")
        self.update_progress_visuals(current_xp)
        
        try:
            lvl_calc = self._get_level_for_xp(current_xp)
            self.lvl_entry_ref.delete(0, "end")
            self.lvl_entry_ref.insert(0, str(lvl_calc))
        except: pass

    def _get_xp_for_level(self, lvl):
        """
        Calculate total XP required to reach a specific level.
        Supports Level 50+ with correct curve:
        - Levels 1-50: Base curve (1570 * level^2)
        - Level 50 base: 3,925,000 XP
        - Levels 51+: Flat 144,000 XP per level above 50
        """
        if lvl <= 50:
            return int(1570 * (lvl ** 2))
        else:
            base_50 = 3925000
            extra_levels = lvl - 50
            return int(base_50 + (extra_levels * 144000))

    def _get_level_for_xp(self, xp):
        """
        Calculate level based on total XP.
        Supports Level 50+ with correct curve:
        - XP <= 3,925,000: Use base curve formula
        - XP > 3,925,000: Level 50 + (excess XP / 144,000)
        """
        if xp <= 3925000:
            val = int(math.sqrt(xp / 1570))
            return val if val > 0 else 1
        else:
            base_50 = 3925000
            diff = xp - base_50
            extra_levels = int(diff / 144000)
            return 50 + extra_levels

    def calc_xp_from_lvl(self):
        """
        Calculate XP from target level and update the XP entry field.
        Uses the standard XP curve formula (supports modded curves via manual entry).
        """
        try:
            lvl = int(self.lvl_entry_ref.get())
            if lvl < 1: lvl = 1
            if lvl > 150: lvl = 150
            
            new_xp = self._get_xp_for_level(lvl)
            
            self.xp_entry_ref.delete(0, "end")
            self.xp_entry_ref.insert(0, str(new_xp))
            self.update_progress_visuals(new_xp)
            self.status_label.configure(text=f"SET TO LEVEL {lvl}", text_color=COL_TEXT_LIGHT)
        except ValueError: pass

    def calc_lvl_from_xp(self):
        """
        Calculate level from custom XP and update the level entry field.
        Note: This is for display only. Manual XP entries are saved exactly as typed,
        allowing modded players to use custom XP values that don't match the standard curve.
        """
        try:
            raw_xp = int(self.xp_entry_ref.get())
            lvl = self._get_level_for_xp(raw_xp)
            
            self.lvl_entry_ref.delete(0, "end")
            self.lvl_entry_ref.insert(0, str(lvl))
            self.update_progress_visuals(raw_xp)
            self.status_label.configure(text=f"XP MATCHES LEVEL {lvl}", text_color=COL_TEXT_LIGHT)
        except ValueError: pass

    def update_progress_visuals(self, current_xp):
        try:
            current_xp = int(current_xp)
            current_lvl = self._get_level_for_xp(current_xp)
            
            xp_start_of_lvl = self._get_xp_for_level(current_lvl)
            xp_start_of_next = self._get_xp_for_level(current_lvl + 1)
            
            range_span = xp_start_of_next - xp_start_of_lvl
            if range_span <= 0: range_span = 1
            
            progress_val = (current_xp - xp_start_of_lvl) / range_span
            progress_val = max(0.0, min(1.0, progress_val))
            
            # Optimized: single update instead of multiple
            self.progress_bar_ref.set(progress_val)
            pct = int(progress_val * 100)
            self.progress_label_ref.configure(text=f"LEVEL {current_lvl}  >>  {pct}%  >>  LEVEL {current_lvl + 1}")
        except Exception as e:
            print(f"Progress visual error: {e}")
            pass

    def load_data(self):
        if not self.current_folder_path or not os.path.exists(self.current_folder_path): return
        self.clear_ui()
        p_path = os.path.join(self.current_folder_path, 'Profile.json')
        if os.path.exists(p_path):
            try:
                with open(p_path, 'r', encoding='utf-8') as f: self.profile_data = json.load(f)
                meta = self.profile_data.get("MetaResources", [])
                
                # POINT WALLET (Respec Points) - Optimized single pass
                self.add_section_header("POINT WALLET")
                point_config = {"Refund": {"label": "RESPEC POINTS", "color": C_REF}}
                # Build dict of existing items for faster lookup
                meta_dict = {item.get("MetaRow"): item.get("Count", 0) for item in meta}
                for key, conf in point_config.items():
                    value = meta_dict.get(key, 0)
                    section = "PROFILE" if key in meta_dict else "PROFILE_NEW"
                    self.add_input_field(conf["label"], key, value, section, icon_color=conf["color"])
                
                # ACCOUNT WALLET (Currencies) - Optimized single pass
                self.add_section_header("ACCOUNT WALLET")
                currency_config = {"Credits": {"label": "REN", "color": C_REN}, "Exotic1": {"label": "EXOTICS", "color": C_EXO}, "Exotic_Red": {"label": "STABILIZED", "color": C_RED}, "Biomass": {"label": "LEGENDARY BIOMASS", "color": C_BIO}, "licence": {"label": "LEGENDARY LICENSE", "color": C_LIC}}
                for key, conf in currency_config.items():
                    value = meta_dict.get(key, 0)
                    section = "PROFILE" if key in meta_dict else "PROFILE_NEW"
                    self.add_input_field(conf["label"], key, value, section, icon_color=conf["color"])
            except Exception as e: self.show_message("ERROR", f"Failed to load Profile:\n{e}", "#FF5555")
        
        c_path = os.path.join(self.current_folder_path, 'Characters.json')
        if os.path.exists(c_path):
            try:
                with open(c_path, 'r', encoding='utf-8') as f: container = json.load(f)
                self.char_root_container = container
                
                # Identify the list of characters
                target_list = None
                if isinstance(container, list): 
                    target_list = container
                elif isinstance(container, dict):
                    if "Characters.json" in container and isinstance(container["Characters.json"], list):
                        target_list = container["Characters.json"]
                    else:
                        for v in container.values():
                            if isinstance(v, list): target_list = v; break
                
                self.char_list_ref = target_list
                self.parsed_chars = []
                
                if target_list:
                    # Optimized character parsing - single pass with early exits
                    for item in target_list:
                        real_item = item
                        is_nested = isinstance(item, list) and len(item) > 0
                        if is_nested:
                            real_item = item[0]
                        
                        char_obj = None
                        is_encoded = False
                        
                        if isinstance(real_item, str):
                            try:
                                char_obj = json.loads(real_item)
                                is_encoded = True
                            except (json.JSONDecodeError, TypeError):
                                continue
                        elif isinstance(real_item, dict):
                            char_obj = real_item
                        else:
                            continue
                        
                        if char_obj:
                            self.parsed_chars.append({
                                'obj': char_obj,
                                'is_encoded': is_encoded,
                                'is_nested': is_nested
                            })
                
                if self.parsed_chars:
                    # Init first character
                    self.active_char_index = 0
                    self.render_character_ui()
                else:
                    self.active_char_index = -1

            except Exception as e: self.show_message("ERROR", f"Failed to load Characters:\n{e}", "#FF5555")
        
        # Single UI update after all widgets are created for better performance
        self.update_idletasks()
        
        self.status_label.configure(text=f"CONNECTED: {os.path.basename(self.current_folder_path)}", text_color=C_BIO)

    def save_data(self):
        if not self.current_folder_path: return
        try:
            # --- SAFETY SYSTEM: AUTO-BACKUP ---
            backup_base = self.config.get("backup_path")
            if not backup_base:
                backup_base = os.path.join(os.path.expanduser('~'), 'Documents', 'LUMEN_BACKUP')
                
            if not os.path.exists(backup_base): os.makedirs(backup_base)
            
            self.cleanup_old_backups()
            
            ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_dir = os.path.join(backup_base, f"Backup_{ts}")
            os.makedirs(backup_dir)

            p_src = os.path.join(self.current_folder_path, 'Profile.json')
            if os.path.exists(p_src): shutil.copy(p_src, os.path.join(backup_dir, 'Profile.json'))
            
            c_src = os.path.join(self.current_folder_path, 'Characters.json')
            if os.path.exists(c_src): shutil.copy(c_src, os.path.join(backup_dir, 'Characters.json'))
            # ----------------------------------

            p_path = os.path.join(self.current_folder_path, 'Profile.json')
            if os.path.exists(p_path):
                shutil.copy(p_path, p_path + ".backup") 
                meta = self.profile_data.get("MetaResources", [])
                # Optimized: Build dict for O(1) lookup instead of O(n) loop
                meta_dict = {item["MetaRow"]: item for item in meta}
                new_items = []
                
                for key_full, entry in list(self.entries.items()):
                    section, r_key = key_full.split("|", 1)
                    try: 
                        val = int(entry.get())
                    except (ValueError, AttributeError): 
                        continue
                    
                    if section == "PROFILE" and r_key in meta_dict:
                        meta_dict[r_key]["Count"] = val
                    elif section == "PROFILE_NEW" and val > 0:
                        new_items.append({"MetaRow": r_key, "Count": val})
                
                # Rebuild meta list with updated values and new items
                self.profile_data["MetaResources"] = list(meta_dict.values()) + new_items
                with open(p_path, 'w', encoding='utf-8') as f: 
                    json.dump(self.profile_data, f, indent=4)
            c_path = os.path.join(self.current_folder_path, 'Characters.json')
            if self.char_root_container is not None and os.path.exists(c_path) and self.active_char_index >= 0:
                shutil.copy(c_path, c_path + ".backup")
                
                char_data = self.parsed_chars[self.active_char_index]
                char_obj = char_data['obj']
                
                for key_full, entry in list(self.entries.items()):
                    section, r_key = key_full.split("|", 1)
                    if section == "CHAR":
                        try: char_obj[r_key] = int(entry.get())
                        except (ValueError, AttributeError): pass
                
                final_element = char_obj
                if char_data['is_encoded']: final_element = json.dumps(char_obj)
                
                if char_data['is_nested']:
                    self.char_list_ref[self.active_char_index][0] = final_element
                else:
                    self.char_list_ref[self.active_char_index] = final_element
                    
                with open(c_path, 'w', encoding='utf-8') as f: json.dump(self.char_root_container, f, indent=4)
            self.status_label.configure(text="SUCCESSFUL WRITE", text_color=C_BIO)
            self.show_message("SUCCESS", "Data saved successfully!\n\n(Restart game to see changes.)", C_BIO)
        except PermissionError: self.show_message("SAVE FAILED", "File is locked by Icarus.\nPlease close the game.", "#FF5555")
        except Exception as e: self.show_message("ERROR", f"Error saving data:\n{e}", "#FF5555")

    def save_and_launch_game(self):
        """Save data and launch Icarus via Steam."""
        if not self.current_folder_path:
            self.show_message("NO PROFILE", "Please load a profile first.", "#FF5555")
            return
        
        try:
            # --- SAFETY SYSTEM: AUTO-BACKUP ---
            backup_base = self.config.get("backup_path")
            if not backup_base:
                backup_base = os.path.join(os.path.expanduser('~'), 'Documents', 'LUMEN_BACKUP')
                
            if not os.path.exists(backup_base): os.makedirs(backup_base)
            
            # Cleanup old backups BEFORE creating new one (to maintain exact limit)
            self.cleanup_old_backups()
            
            ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_dir = os.path.join(backup_base, f"Backup_{ts}")
            os.makedirs(backup_dir)

            p_src = os.path.join(self.current_folder_path, 'Profile.json')
            if os.path.exists(p_src): shutil.copy(p_src, os.path.join(backup_dir, 'Profile.json'))
            
            c_src = os.path.join(self.current_folder_path, 'Characters.json')
            if os.path.exists(c_src): shutil.copy(c_src, os.path.join(backup_dir, 'Characters.json'))
            # ----------------------------------

            p_path = os.path.join(self.current_folder_path, 'Profile.json')
            if os.path.exists(p_path):
                shutil.copy(p_path, p_path + ".backup") 
                meta = self.profile_data.get("MetaResources", [])
                # Optimized: Build dict for O(1) lookup instead of O(n) loop
                meta_dict = {item["MetaRow"]: item for item in meta}
                new_items = []
                
                for key_full, entry in list(self.entries.items()):
                    section, r_key = key_full.split("|", 1)
                    try: 
                        val = int(entry.get())
                    except (ValueError, AttributeError): 
                        continue
                    
                    if section == "PROFILE" and r_key in meta_dict:
                        meta_dict[r_key]["Count"] = val
                    elif section == "PROFILE_NEW" and val > 0:
                        new_items.append({"MetaRow": r_key, "Count": val})
                
                # Rebuild meta list with updated values and new items
                self.profile_data["MetaResources"] = list(meta_dict.values()) + new_items
                with open(p_path, 'w', encoding='utf-8') as f: 
                    json.dump(self.profile_data, f, indent=4)
            
            c_path = os.path.join(self.current_folder_path, 'Characters.json')
            if self.char_root_container is not None and os.path.exists(c_path) and self.active_char_index >= 0:
                shutil.copy(c_path, c_path + ".backup")
                
                char_data = self.parsed_chars[self.active_char_index]
                char_obj = char_data['obj']
                
                for key_full, entry in list(self.entries.items()):
                    section, r_key = key_full.split("|", 1)
                    if section == "CHAR":
                        try: char_obj[r_key] = int(entry.get())
                        except (ValueError, AttributeError): pass
                
                final_element = char_obj
                if char_data['is_encoded']: final_element = json.dumps(char_obj)
                
                if char_data['is_nested']:
                    self.char_list_ref[self.active_char_index][0] = final_element
                else:
                    self.char_list_ref[self.active_char_index] = final_element
                    
                with open(c_path, 'w', encoding='utf-8') as f: json.dump(self.char_root_container, f, indent=4)
            
            self.status_label.configure(text="SAVED & LAUNCHING...", text_color=C_BIO)
            os.startfile("steam://rungameid/1149460")
            
            if self.config.get("close_on_launch", False):
                self.after(1000, self.destroy)
            else:
                self.show_message("LAUNCHING", "Data saved successfully!\n\nLaunching Icarus via Steam...", C_BIO)
            
        except PermissionError:
            self.show_message("SAVE FAILED", "File is locked by Icarus.\nPlease close the game before launching.", "#FF5555")
        except Exception as e:
            self.show_message("ERROR", f"Error saving data:\n{e}\n\nGame launch cancelled.", "#FF5555")

if __name__ == "__main__":
    app = LumenIcarusEditor()
    app.mainloop()