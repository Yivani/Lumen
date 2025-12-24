# LUMEN // ICARUS SAVE EDITOR

![LUMEN EDITOR INTERFACE](grafik.png)

## // SYSTEM OVERVIEW

**LUMEN EDITOR** is an advanced external tool designed for the manipulation of *ICARUS* player profile data. It provides Prospectors with direct access to account currencies, character progression metrics, and resource allocation systems.

This software operates outside the standard UAC protocols, allowing for the modification of local `Profile.json` and `Characters.json` data streams.

---

## // OPERATIONAL CAPABILITIES

### [ 1 ] CURRENCY MANAGEMENT
Direct injection and modification of all orbital exchange currencies.
* **REN:** Standard currency modification.
* **EXOTICS:** Purple exotic matter allocation.
* **STABILIZED EXOTICS:** Red exotic matter allocation.
* **LEGENDARY BIOMASS:** Biological resource management.
* **LEGENDARY LICENSE:** Permit allocation.

### [ 2 ] PROGRESSION MATRIX
Advanced Level and Experience Point (XP) calculator with bi-directional synchronization.
* **LEVEL CALCULATOR:** Input desired Level -> System calculates required XP.
* **XP CALCULATOR:** Input raw XP -> System derives current Level.
* **VISUAL INDICATOR:** Live progress bar tracking current level threshold completion.

### [ 3 ] AUTOMATED POINT ALLOCATION
The system bypasses standard progression locks by automatically calculating available points based on the set Level.
* **TALENT POINTS:** Auto-filled based on Level.
* **SOLO TALENT POINTS:** Auto-filled based on Level.
* **BLUEPRINT (TECH) POINTS:** Auto-filled based on Level.

### [ 4 ] PROFILE INTERFACE
* **AUTO-SCAN:** Automatically detects SteamID and local save paths (`%localappdata%\Icarus\Saved\PlayerData`).
* **MANUAL OVERRIDE:** Directory browsing for non-standard installations.
* **MULTI-PROFILE:** Dropdown selector for multiple Steam accounts.

---

## // VISUAL INTELLIGENCE

### **INTERFACE: LUMEN ELITE UI**
Custom-engineered GUI matching the internal ICARUS "Dark Olive" aesthetic for seamless integration with existing UAC terminals.

![GAMEPLAY COMPARISON](Icarus-Win64-Shipping_hRmTKDTDiV.jpg)

---

## // DEPLOYMENT INSTRUCTIONS

### **OPTION A: EXECUTABLE (RECOMMENDED)**
1.  Download the latest `LumenEditor.exe` release.
2.  Ensure *ICARUS* is fully terminated (Process ID: 0).
3.  Run `LumenEditor.exe` as Administrator.
4.  Select Profile ID or Browse manually.
5.  Modify values.
6.  Click **[ SAVE & APPLY ]**.

### **OPTION B: PYTHON SOURCE**
1.  Ensure **Python 3.11+** is installed.
2.  Install dependencies:
    ```bash
    pip install customtkinter
    ```
3.  Launch the script:
    ```bash
    python IcarusGUI.py
    ```

---

## // TROUBLESHOOTING

| ERROR MESSAGE | CAUSE | SOLUTION |
| :--- | :--- | :--- |
| **"File is locked"** | The game client is currently running. | Terminate *ICARUS* and retry the save operation. |
| **"No Profile Detected"** | Non-standard installation path. | Use the **[ BROWSE ]** button to locate the numbered folder inside `Local\Icarus\Saved\PlayerData\`. |

---

## // DISCLAIMER

> **WARNING:** This tool modifies local data files. While safety protocols (backups) are implemented, usage is at the operator's own risk. Always backup your `PlayerData` folder before engaging experimental software.

* **DEVELOPER:** [YOUR NAME]
* **VERSION:** FINAL // ELITE
* **STATUS:** ACTIVE
