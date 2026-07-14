# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

KFishMonger is a Linux (Debian/Ubuntu) tool for automating anonymity environments: VPN, Tor, DNSCrypt, proxychains, kill switches, etc. It is controlled by the `kfm` CLI and monitored by a PySide6 desktop GUI. Code comments and user-facing strings are in Portuguese; match that when editing.

## Repository layout

Three independent parts:

- `command/` — the `kfm` CLI entrypoint and installer/updater shell scripts.
- `projects/` — the core. Each subdirectory is a self-contained *project* (a feature: `vpn`, `tor`, `dns`, `json`, `fake`, `panicroom`, `network`, `db`, `conky`, `i2p`, `proxychains`, ...). `projects/api/` is the shared library imported by all projects.
- `ui/` — PySide6 desktop app (a "PyDracula"-style themed window) that monitors and controls the environment.

## Install / runtime paths (important)

This is not run from the repo checkout. Installation copies the tree to **`/opt/kfishmonger`** and symlinks `/opt/kfishmonger/command/kfm.sh` to `/bin/kfm`. Runtime state lives under **`/var/kfm/`**:

- `/var/kfm/<project>/config.json` — per-project runtime config (see ConfigProject below).
- `/var/kfm/log/<project>.log` — per-project logs (viewable via `kfm -p <project> -c log`).
- `/var/kfm/data/` — global config (e.g. install URL).

Paths like `/opt/kfishmonger/...` are hardcoded throughout (`api/CONST.py`, `.service` files, `kfm.sh`). Code that reads its own location uses `inspect.getfile(inspect.currentframe())` to compute `ROOT` and does `sys.path.append(ROOT)` so that `from api.X import Y` resolves — preserve this pattern in new project scripts.

## Commands

Install (as root — copies to `/opt`, apt-installs deps, pip-installs `netifaces psutil pycryptodome Pysocks socks`, runs every project's `install.py`):

```sh
sudo /tmp/install.sh          # or: sudo command/install.sh  (add -y for non-interactive)
```

Everyday CLI usage (`kfm.sh` requires root; add `-b` to run in background):

```sh
kfm -c install                     # install all projects (those with config.json "default": true)
kfm -p vpn -c install              # install a single project
kfm -p vpn -c start                # run projects/vpn/start.py
kfm -p vpn -c stop | restart       # run the matching <command>.py in the project dir
kfm -p vpn -c log                  # cat /var/kfm/vpn.log
kfm -c update                      # re-download and reinstall from SourceForge
```

The dispatch rule (`command/kfm.py`): `kfm -p <project> -c <command>` executes `projects/<project>/<command>.py` with `python3`. `install`, `update`, and `log` are special-cased; everything else maps directly to a `.py` file. So "adding a command" to a project = adding `projects/<project>/<command>.py`.

Run the GUI (from the `ui/` directory — it loads fonts by relative path and sets `ROOT` from `__file__`):

```sh
cd ui && python3 main.py
```

There is **no test suite, linter, or build step**. Several modules have a `main()` under `if __name__ == "__main__"` used for ad-hoc manual testing.

## Project (module) structure

Each `projects/<name>/` follows a convention (see `projects/network/readme.md`):

- `config.json` — module metadata. `{"default": true}` means the module is **auto-executed via systemd**: the bulk installer (`kfm -c install` / `projects/install.py`) runs its `install.py`, which enables and starts the module's `kfm_<name>.service`. Set `false` to keep a module from auto-starting. (An unread `execute` key appears in some configs but nothing in the code consumes it.)
- `install.py` — **required**. Installs apt/pip deps, copies systemd `.service` files from `resources/` to `/etc/systemd/system/` (substituting `{LOGNAME}` etc.), seeds `/var/kfm/<name>/config.json`, and enables/starts the service. Run directly with `python3`.
- `execstart.py` — the long-running process the systemd service actually executes (`ExecStart=python3 .../execstart.py`).
- `start.py` / `stop.py` / `restart.py` — thin wrappers, usually `Systemctl(SERVICE).start()` etc.
- `resources/` — templates: `.service` unit files and the default `config.json`.
- `sub/` — sub-projects installed via `kfm -p <project> -s <sub> -c install`.

Systemd services are named `kfm_<name>.service` (constants in `api/CONST.py`, e.g. `VPN_SERVICE`). Older unversioned names (`vpn.service`) are cleaned up on install.

## Shared API (`projects/api/`)

Reusable wrappers around shell/system operations — always used instead of calling subprocess ad-hoc:

- `process.py` — `Process(command)`: `.run()` (blocking, returns stdout), `wait=False` for fire-and-forget, `.asThread(callback)` for line-streaming a long process.
- `systemctl.py` — `Systemctl(service)`: start/stop/restart/enable/status/running.
- `config.py` — `Config(path)`: edit line-oriented Unix config files (add/comment/uncomment/replace attributes) with support for `chattr +i` immutability (`.block()`/`.unblock()`) used for locking `/etc/resolv.conf`.
- `config_project.py` — `ConfigProject(name)`: merges `resources/config.json` (defaults) into `/var/kfm/<name>/config.json` without overwriting existing keys; `.load()` sets each key as an attribute on the instance.
- `apt.py`, `pip.py`, `distro.py`, `log.py`, `network.py`, `resolv.py`, `torrc.py`, `tor.py`, `vpn.py`, `database.py`, `downloadinstall.py`, `rsahelp.py` — package installs, distro/user detection, logging to `/var/kfm/log/`, and feature-specific helpers.
- `CONST.py` — all service names and ports. **Ports: JSON monitor 20000, DB 20001, panicroom 20002, Tor SOCKS 9050 / trans 9040 / DNS 53.**

## The `json` project — state bus for monitoring

`projects/json/execstart.py` runs a TCP daemon on `127.0.0.1:20000`. Projects report their state to it; it merges everything into `/tmp/fishmonger.json` (written every 5s) which `conky`/the GUI read. Wire protocol: a **20-byte ASCII version header** (`"00000000000000000000"`) followed by a JSON body; merge is a recursive dict join. Clients use `projects/json/api/jsonclient.py` (`JsonClient().send(dict)`). `projects/json/sub/` and `monitor.py` are the per-feature reporters.

## GUI (`ui/`)

PySide6 app. `main.py` is the window; `files_rc.py` is the compiled Qt resource bundle (icons/fonts — do not hand-edit). `ui_main.py`/`ui_functions.py`/`ui_styles.py`/`app_functions.py`/`app_modules.py` are the generated + custom UI layer; `widget/` holds the per-feature pages (`page_vpn.py`, `page_dns.py`, `widget_tor.py`, ...). The GUI drives the environment through the same project scripts / json bus rather than reimplementing logic.
