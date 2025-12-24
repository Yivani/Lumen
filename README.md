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
* **RESPEC POINTS:** Refund point allocation for talent unlearning.

### [ 2 ] PROGRESSION MATRIX
Advanced Level and Experience Point (XP) calculator with bi-directional synchronization.
* **LEVEL CALCULATOR:** Input desired Level -> System calculates required XP.
* **XP CALCULATOR:** Input raw XP -> System derives current Level.
* **VISUAL INDICATOR:** Live progress bar tracking current level threshold completion.

### [ 3 ] PROFILE INTERFACE
* **AUTO-SCAN:** Automatically detects SteamID and local save paths (`AppData\%localappdata%\Icarus\Saved\PlayerData`).
* **MANUAL OVERRIDE:** Directory browsing for non-standard installations.
* **MULTI-PROFILE:** Dropdown selector for multiple Steam accounts.

---

## // VISUAL INTELLIGENCE

### **INTERFACE: LUMEN ELITE UI**
Custom-engineered GUI matching the internal ICARUS "Dark Olive" aesthetic for seamless integration with existing UAC terminals.

![GAMEPLAY COMPARISON](Icarus-Win64-Shipping_hRmTKDTDiV.jpg)

---

## // DEPLOYMENT INSTRUCTIONS

### **EXECUTABLE LAUNCH**
1.  Download the latest **`LUMEN.exe`** release.
2.  **Game State:** It is **recommended** to close *ICARUS* completely. However, simply returning to the **Character Selection Menu** is sufficient for changes to take effect.
3.  Run **`LUMEN.exe`** as Administrator.
4.  Select your Profile ID from the dropdown (or Browse manually).
5.  Modify your desired values.
6.  Click **[ SAVE & APPLY ]**.

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
* **VERSION:** v1.0
* **STATUS:** ACTIVE
