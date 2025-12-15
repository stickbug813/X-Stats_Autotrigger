# XSAT Auto-Trigger

Automatic live sports graphics triggering for Ross XPression using real-time XML stat feeds.

## Features
- Automatic player scoring graphics (2PT / 3PT / FT)
- Team scoring burst detection
- RossTalk TCP control
- Ross Dashboard HTTP control
- Safe XML debounce & dedupe
- Broadcast-tested in live environments

## Requirements
- Windows 10 / 11
- Ross XPression
- Python 3.11+ (if running from source)

## Quick Start (Operators)
1. Download the latest release
2. Extract ZIP
3. Edit `config.yaml`
4. Run `xsat_autotrigger.exe`

## Configuration
See `config.yaml` for:
- Stat types enabled
- Burst thresholds
- RossTalk host/port
- Timing behavior

## Dashboard Integration
Example Dashboard button:
```js
ogscript.asyncHTTP("http://127.0.0.1:5005/enable", "PUT");
