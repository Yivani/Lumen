# LUMEN // ICARUS SAVE EDITOR

![LUMEN EDITOR INTERFACE](https://i.imgur.com/qTPgFzd.png)

## // SYSTEM OVERVIEW

**LUMEN EDITOR** is an advanced external tool designed for the manipulation of *ICARUS* player profile data. It provides Prospectors with direct access to account currencies, character progression metrics, and resource allocation systems.

This software operates outside the standard UAC protocols, allowing for the modification of local `Profile.json` and `Characters.json` data streams.

---

## // SECURITY & ANTIVIRUS NOTE

> **FALSE POSITIVE WARNING:** Some antivirus software (including VirusTotal scans) may flag `LUMEN.exe` as generic malware.

**This is a known false positive caused by PyInstaller.**
Because this tool is a standalone executable built from Python scripts without a digital signature, heuristics engines often misidentify it.

* **VERIFICATION:** The full source code is available in this repository (`LUMEN.py`) for inspection.
* **ACTION:** If your antivirus blocks the file, please add an **Exclusion/Exception** for `LUMEN.exe`.
* **SAFETY:** This tool operates entirely locally and makes no network connections other than scanning your local file system for save data.

---

## // OPERATIONAL CAPABILITIES

### [ 1 ] CURRENCY MANAGEMENT
Direct injection and modification of all orbital exchange currencies.
* **REN:** Standard currency modification.
* **EXOTICS:** Purple exotic matter allocation.
* **STABILIZED EXOTICS:** Red exotic matter allocation.
* **LEGENDARY BIOMASS:** Biological resource management.
* **LEGENDARY LICENSE:** Permit allocation.
* **RESPEC POINTS:** Refund point allocation for talent unlearning.

### [ 2 ] PROGRESSION MATRIX
Advanced Level and Experience Point (XP) calculator with bi-directional synchronization.
* **LEVEL CALCULATOR:** Input desired Level -> System calculates required XP.
* **XP CALCULATOR:** Input raw XP -> System derives current Level.
* **VISUAL INDICATOR:** Live progress bar tracking current level threshold completion.
* **XP DEBT MANAGEMENT:** Clear XP debt with a single click.
* **PRESTIGE TOOLS:** Soft-reset to Level 1 or set to Level 50 soft-cap while preserving talents and blueprints.

### [ 3 ] CHARACTER MANAGEMENT
* **REVIVE & RESCUE:** Revive dead characters and rescue abandoned characters with one-click functionality.
* **CHARACTER SELECTOR:** Easy dropdown selection for multiple characters.
* **MULTI-CHARACTER SUPPORT:** Edit any character in your save file.

### [ 4 ] PROFILE INTERFACE
* **AUTO-SCAN:** Automatically detects SteamID and local save paths (`AppData\%localappdata%\Icarus\Saved\PlayerData`).
* **MANUAL OVERRIDE:** Directory browsing for non-standard installations.
* **MULTI-PROFILE:** Dropdown selector for multiple Steam accounts.

### [ 5 ] STEAM INTEGRATION
* **SAVE & LAUNCH:** One-click button to save your changes and launch Icarus via Steam.
* **CLOSE ON LAUNCH:** Optional toggle to automatically close the editor when launching the game.

### [ 6 ] BACKUP SYSTEM
* **AUTO-BACKUP:** Automatic backup creation before every save operation.
* **BACKUP RETENTION:** Configurable limit (5-50 backups) with automatic cleanup of oldest backups.
* **BACKUP MANAGEMENT:** Open backup folder or delete all backups with dedicated tools.

### [ 7 ] DATA VALIDATION
* **JSON INTEGRITY CHECK:** Validate Profile.json and Characters.json for syntax errors before saving.
* **ERROR DETECTION:** Identifies and reports JSON parsing errors to prevent corrupted saves.

---

## // VISUAL INTELLIGENCE

### **INTERFACE: LUMEN ELITE UI**
Custom-engineered GUI matching the internal ICARUS "Dark Olive" aesthetic for seamless integration with existing UAC terminals.

---

## // DEPLOYMENT INSTRUCTIONS

### **EXECUTABLE LAUNCH**
1.  Download the latest **`LUMEN.exe`** release.
2.  **Game State:** It is **recommended** to close *ICARUS* completely. However, simply returning to the **Character Selection Menu** is sufficient for changes to take effect.
3.  Run **`LUMEN.exe`** as Administrator.
4.  Select your Profile ID from the dropdown (or Browse manually).
5.  Modify your desired values.
6.  Click **[ SAVE & APPLY ]** or **[ SAVE & LAUNCH GAME ]** to save and optionally launch Icarus.

### **SETTINGS TAB**
Access advanced settings via the **SETTINGS** tab:
* **Backup Location:** Configure where backups are stored.
* **Backup Retention:** Set maximum number of backups to keep (5-50).
* **Close on Launch:** Toggle automatic editor closure when launching the game.
* **JSON Validation:** Validate save files for syntax errors before saving.

---

## // TROUBLESHOOTING

| ERROR MESSAGE | CAUSE | SOLUTION |
| :--- | :--- | :--- |
| **"File is locked"** | The game client is currently writing to the file. | Return to the **Character Select Menu** or fully terminate *ICARUS* and retry. |
| **"No Profile Detected"** | Non-standard installation path. | Use the **[ BROWSE ]** button to locate the numbered folder inside `AppData\Local\Icarus\Saved\PlayerData\`. |

---

## // DISCLAIMER

> **WARNING:** This tool modifies local data files. While safety protocols (backups) are implemented, usage is at the operator's own risk. Always backup your `PlayerData` folder before engaging experimental software.

* **DEVELOPER:** Yivani
* **VERSION:** v2.0
* **STATUS:** ACTIVE
