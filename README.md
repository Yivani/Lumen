LUMEN // ICARUS SAVE EDITOR
// SYSTEM OVERVIEW

LUMEN EDITOR is an advanced external tool designed for the manipulation of ICARUS player profile data. It provides Prospectors with direct access to account currencies, character progression metrics, and resource allocation systems.

This software operates outside the standard UAC protocols, allowing for the modification of local Profile.json and Characters.json data streams.
// OPERATIONAL CAPABILITIES
[ 1 ] CURRENCY MANAGEMENT

Direct injection and modification of all orbital exchange currencies.

    REN: Standard currency modification.

    EXOTICS: Purple exotic matter allocation.

    STABILIZED EXOTICS: Red exotic matter allocation.

    LEGENDARY BIOMASS: Biological resource management.

    LEGENDARY LICENSE: Permit allocation.

[ 2 ] PROGRESSION MATRIX

Advanced Level and Experience Point (XP) calculator with bi-directional synchronization.

    LEVEL CALCULATOR: Input desired Level -> System calculates required XP.

    XP CALCULATOR: Input raw XP -> System derives current Level.

    VISUAL INDICATOR: Live progress bar tracking current level threshold completion.

[ 3 ] AUTOMATED POINT ALLOCATION

The system bypasses standard progression locks by automatically calculating available points based on the set Level.

    TALENT POINTS: Auto-filled based on Level.

    SOLO TALENT POINTS: Auto-filled based on Level.

    BLUEPRINT (TECH) POINTS: Auto-filled based on Level.

[ 4 ] PROFILE INTERFACE

    AUTO-SCAN: Automatically detects SteamID and local save paths (%localappdata%\Icarus\Saved\PlayerData).

    MANUAL OVERRIDE: Directory browsing for non-standard installations.

    MULTI-PROFILE: Dropdown selector for multiple Steam accounts.

// VISUAL INTELLIGENCE

INTERFACE: LUMEN ELITE UI Custom-engineered GUI matching the internal ICARUS "Dark Olive" aesthetic for seamless integration with existing UAC terminals.
// DEPLOYMENT INSTRUCTIONS
OPTION A: EXECUTABLE (RECOMMENDED)

    Download the latest LumenEditor.exe release.

    Ensure ICARUS is fully terminated (Process ID: 0).

    Run LumenEditor.exe as Administrator.

    Select Profile ID or Browse manually.

    Modify values.

    Click [ SAVE & APPLY ].

OPTION B: PYTHON SOURCE

    Ensure Python 3.11+ is installed.

    Install dependencies:
    Bash

    pip install customtkinter

    Launch the script:
    Bash

    python IcarusGUI.py

// TROUBLESHOOTING

ERROR: "File is locked"

    CAUSE: The game client is currently running and has locked the JSON files.

    SOLUTION: Terminate ICARUS and retry the save operation.

ERROR: "No Profile Detected"

    CAUSE: Non-standard installation path.

    SOLUTION: Use the [ BROWSE ] button to locate the numbered folder inside Local\Icarus\Saved\PlayerData\.

// DISCLAIMER

WARNING: This tool modifies local data files. While safety protocols (backups) are implemented, usage is at the operator's own risk. Always backup your PlayerData folder before engaging experimental software.

    DEVELOPER: [YOUR NAME]

    VERSION: FINAL // ELITE

    STATUS: ACTIVE
