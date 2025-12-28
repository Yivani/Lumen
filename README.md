# LUMEN // ICARUS SAVE EDITOR

![LUMEN EDITOR INTERFACE](https://i.imgur.com/y6DeHto.png)

## // SYSTEM OVERVIEW

**LUMEN EDITOR** is an advanced external tool for manipulating *ICARUS* player profile data. Provides direct access to account currencies, character progression, and resource allocation systems.

---

## // SECURITY NOTE

> **FALSE POSITIVE WARNING:** Some antivirus software may flag `LUMEN.exe` as malware. This is a known false positive caused by PyInstaller. The full source code is available for inspection. Add an exclusion if blocked.

---

## // FEATURES

**CURRENCY MANAGEMENT:** Edit REN, Exotics, Stabilized Exotics, Legendary Biomass, Legendary License, and Respec Points.

**PROGRESSION MATRIX:** Level/XP calculator with bi-directional sync, progress bar, XP debt clearing, and prestige tools (soft-reset to Level 1 or Level 50 soft-cap).

**CHARACTER MANAGEMENT:** Revive dead/abandoned characters, multi-character support with dropdown selector.

**PROFILE INTERFACE:** Auto-detects SteamID and save paths, manual browse option, multi-profile support.

**STEAM INTEGRATION:** Save & launch Icarus with one click, optional auto-close on launch.

**BACKUP SYSTEM:** Automatic backups before saves, configurable retention (5-50), backup management tools.

**DATA VALIDATION:** JSON integrity check before saving.

---

## // QUICK START

1. Download **`LUMEN.exe`** (close ICARUS or return to Character Selection Menu)
2. Run as Administrator
3. Select Profile ID from dropdown (or Browse manually)
4. Modify values
5. Click **[ SAVE & APPLY ]** or **[ SAVE & LAUNCH GAME ]**

**Settings Tab:** Configure backup location, retention limit, close-on-launch toggle, and JSON validation.

---

## // TROUBLESHOOTING

| ERROR | SOLUTION |
| :--- | :--- |
| **"File is locked"** | Return to Character Select Menu or close ICARUS completely |
| **"No Profile Detected"** | Use **[ BROWSE ]** to locate folder in `AppData\Local\Icarus\Saved\PlayerData\` |

---

> **WARNING:** This tool modifies local data files. Always backup your `PlayerData` folder before use.

* **DEVELOPER:** Yivani | **VERSION:** v2.0 | **STATUS:** ACTIVE
