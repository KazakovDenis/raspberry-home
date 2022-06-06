# Control unit
Manipulates Raspberry Pi remotely, e.g. reboot, shutdown.

Consists of:
- agent running on Raspberry Pi directly
- telegram bot running outside

## Command agent
Executes a limited set of commands received via HTTP.  
See docstring in `agent.py` for installation instructions.

## Telegram bot
Is used to send commands to the Command agent via HTTP.  
