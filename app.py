#!/usr/bin/env python3

import hmac
import hashlib
import requests
import string
import random
import json
import codecs
import time
from datetime import datetime
import os
import sys
import base64
import signal
import threading
import psutil
import re
import subprocess
import importlib
import logging
import warnings
import urllib3
import shutil
import inspect
import platform
import getpass
import asyncio
from flask import Flask
import threading

# Flask app للـ health check
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host='0.0.0.0', port=port)
# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore")

# ============================================
# 🔍 DEBUG MODE
# ============================================
DEBUG_MODE = True

def debug_log(msg, level="INFO"):
    if DEBUG_MODE:
        colors = {
            "INFO": "\033[36m", "SUCCESS": "\033[32m", "ERROR": "\033[31m",
            "WARNING": "\033[33m", "REQUEST": "\033[35m", "RESPONSE": "\033[34m"
        }
        color = colors.get(level, "\033[0m")
        print(f"{color}[{level}] {datetime.now():%H:%M:%S} - {msg}\033[0m")

# ============================================
# 🎭 FINGERPRINT SPOOFING
# ============================================
class FingerprintSpoofer:
    UAS = [
        'Dalvik/2.1.0 (Linux; U; Android 13; SM-S908B Build/TP1A)',
        'Dalvik/2.1.0 (Linux; U; Android 14; Pixel 8 Pro Build/UD1A)',
        'Dalvik/2.1.0 (Linux; U; Android 12; Redmi Note 11 Build/SKQ1)',
        'Mozilla/5.0 (Linux; Android 13; SM-A546B) AppleWebKit/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15',
    ]
    LANGS = ['en-US,en;q=0.9','en-GB,en;q=0.8','en-US,en;q=0.9,ar;q=0.8','en-US,en;q=0.9,id;q=0.8']
    DEVICES = [
        {'m':'SM-S908B','b':'samsung','o':'Android 13'},
        {'m':'Pixel 8 Pro','b':'google','o':'Android 14'},
        {'m':'Redmi Note 11','b':'Xiaomi','o':'Android 12'},
        {'m':'iPhone 15 Pro','b':'Apple','o':'iOS 17'},
    ]
    @classmethod
    def random_ua(cls): return random.choice(cls.UAS)
    @classmethod
    def random_lang(cls): return random.choice(cls.LANGS)
    @classmethod
    def random_device(cls): return random.choice(cls.DEVICES)
    @classmethod
    def apply(cls, session):
        d = cls.random_device()
        session.headers.update({
            'User-Agent': cls.random_ua(),
            'Accept-Language': cls.random_lang(),
            'X-Device-Model': d['m'],
            'X-Device-Brand': d['b'],
            'X-OS': d['o'],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Cache-Control': 'no-cache',
        })

# ============================================
# ⏱️ REQUEST DELAYER
# ============================================
class RequestDelayer:
    def __init__(self):
        self._times = []
        self._lock = threading.Lock()
    def wait(self, max_per_sec=3):
        with self._lock:
            now = time.time()
            self._times = [t for t in self._times if now - t < 1.0]
            if len(self._times) >= max_per_sec:
                time.sleep(1.0 - (now - self._times[0]) + random.uniform(0.1, 0.3))
            self._times.append(time.time())
    def human_delay(self): time.sleep(random.uniform(0.3, 1.5))
    def backoff(self, attempt, base=1.0, max_d=60.0):
        time.sleep(min(base * (2 ** attempt), max_d) + random.uniform(0, 0.5))

# ============================================
# 🧵 SESSION MANAGER
# ============================================
class SessionManager:
    def __init__(self, size=10):
        self._pool = []
        self._lock = threading.Lock()
        for _ in range(size):
            s = requests.Session()
            FingerprintSpoofer.apply(s)
            self._pool.append(s)
    def get(self):
        with self._lock:
            if not self._pool:
                s = requests.Session()
                FingerprintSpoofer.apply(s)
                return s
            s = self._pool.pop()
            FingerprintSpoofer.apply(s)
            return s
    def put(self, s):
        with self._lock:
            if len(self._pool) < 20:
                self._pool.append(s)

# ============================================
# 🛡️ BULK PROTECTION
# ============================================
class BulkProtection:
    def __init__(self):
        self.generation_count = 0
        self.last_ip_change = time.time()
        self.ip_change_interval = random.randint(50, 100)
        self.current_ip_index = 0
        self.fake_ips = self._generate_fake_ips()
        self._lock = threading.Lock()
    def _generate_fake_ips(self):
        ips = []
        for _ in range(50):
            ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            ips.append(ip)
        return ips
    def get_next_ip(self):
        with self._lock:
            self.generation_count += 1
            if self.generation_count % self.ip_change_interval == 0:
                self.current_ip_index = (self.current_ip_index + 1) % len(self.fake_ips)
                self.last_ip_change = time.time()
            return self.fake_ips[self.current_ip_index]
    def should_rest(self):
        with self._lock:
            if self.generation_count % 200 == 0:
                return random.uniform(5, 15)
            if self.generation_count % 1000 == 0:
                return random.uniform(30, 60)
        return 0

# تهيئة الأنظمة
session_pool = SessionManager(size=15)
request_delayer = RequestDelayer()
bulk_protection = BulkProtection()

print(f"\033[38;5;82m🛡️ PROTECTION ACTIVE: Anti-Detect + Spoof + Throttle + Bulk\033[0m")

# =============================================================================
# 🛡️ ULTIMATE ANTI-CREDIT & FILENAME PROTECTION SYSTEM
# =============================================================================

class SecurityShield:
    """Security checks removed"""
    @classmethod
    def verify_filename(cls): return True
    @classmethod
    def verify_credits(cls): return True, "OK"
    @classmethod
    def show_breach(cls, reason): pass

# =============================================================================
# 🎨 ULTIMATE VISUAL MASTER - DARK GOLD THEME
# =============================================================================

class VisualMaster:
    """Professional visual design system - Dark Gold Cinema UI"""

    COLORS = {
        'primary':   '\033[38;5;51m',
        'secondary': '\033[38;5;45m',
        'success':   '\033[38;5;82m',
        'error':     '\033[38;5;196m',
        'warning':   '\033[38;5;220m',
        'info':      '\033[38;5;87m',
        'accent':    '\033[38;2;255;215;0m',
        'reset':     '\033[0m',
        'bold':      '\033[1m',
        'dim':       '\033[38;5;240m',
        'border':    '\033[38;2;184;134;11m',
        'c1':        '\033[38;2;218;165;32m',
        'c2':        '\033[38;2;238;173;14m',
        'c3':        '\033[38;2;255;215;0m',
        'c4':        '\033[38;2;255;223;0m',
        'c5':        '\033[38;2;238;173;14m',
        'c6':        '\033[38;2;218;165;32m',
    }

    BOX = {
        'top': "╭═━───────────────────༺𓆩✧𓆪༻───────────────────━═╮",
        'bottom': "╰═━───────────────────༺𓆩✧𓆪༻───────────────────━═╯",
        'mid': "├═━─────────────────────────────────────────────━═┤",
        'v': "║"
    }

    @classmethod
    def show_header(cls, user_level="USER"):
        if not hasattr(cls, '_header_shown'):
            cls._header_shown = False
        if not cls._header_shown:
            cls.clear()
            cls.animate_header(user_level)
            cls._header_shown = True

    @classmethod
    def clear(cls):
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

    @classmethod
    def create_panel(cls, title, content, width=50):
        C = cls.COLORS
        B = cls.BOX
        lines_content = content.split('\n')
        result = []
        result.append(f"{C['border']}{B['top']}{C['reset']}")
        result.append(f"{C['border']}{B['v']}{C['reset']}              {C['accent']}{C['bold']}{title.center(33)}{C['reset']} {C['border']}{B['v']}{C['reset']}")
        result.append(f"{C['border']}{B['mid']}{C['reset']}")
        for line in lines_content:
            visible_line = re.sub(r'\033\[[0-9;]*m', '', line)
            pad = max(0, 45 - len(visible_line))
            result.append(f"{C['border']}{B['v']}{C['reset']} {line}{' ' * pad} {C['border']}{B['v']}{C['reset']}")
        result.append(f"{C['border']}{B['bottom']}{C['reset']}")
        return '\n'.join(result)

    @classmethod
    def animate_header(cls, user_level="USER"):
        import sys, time
        W = 55
        C = cls.COLORS
        B = C['bold']
        R = C['reset']
        SH = [C['c1'], C['c2'], C['c3'], C['c4'], C['c5'], C['c6']]
        
        for frame in range(12):
            line = "═" * W
            shade = SH[frame % len(SH)]
            sys.stdout.write(f"\r{shade}{B}{line}{R}")
            sys.stdout.flush()
            time.sleep(0.05)
        print()

        for i in range(0, W-2, 6):
            bar = "═" * min(i, W-2)
            sys.stdout.write(f"\r{C['c1']}{B}╔{bar}>{R}")
            sys.stdout.flush()
            time.sleep(0.018)
        sys.stdout.write(f"\r{C['c1']}{B}╔{'═'*(W-2)}╗{R}\n")
        sys.stdout.flush()

        MASTER = [
            "███╗░░░███╗░█████╗░███████╗████████╗███████╗██████╗░",
            "████╗░████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗",
            "██╔████╔██║███████║███████╗░░░██║░░░█████╗░░██████╔╝",
            "██║╚██╔╝██║██╔══██║╚════██║░░░██║░░░██╔══╝░░██╔══██╗",
            "██║░╚═╝░██║██║░░██║███████║░░░██║░░░███████╗██║░░██║",
            "╚═╝░░░░░╚═╝╚═╝░░╚═╝╚══════╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝"
        ]
        for i, line in enumerate(MASTER):
            shade = SH[i % len(SH)]
            for end in range(1, len(line)+1, 4):
                sys.stdout.write(f"\r{shade}{B}{line[:end].center(W)}{R}")
                sys.stdout.flush()
                time.sleep(0.006)
            sys.stdout.write(f"\r{shade}{B}{line.center(W)}{R}\n")
            sys.stdout.flush()

        waves = ["≋"*(W-4), "〰"*((W-4)//2), "━"*(W-4), "═"*(W-4)]
        for w in waves:
            sys.stdout.write(f"\r{C['c2']}{B}  {w}  {R}")
            sys.stdout.flush()
            time.sleep(0.05)
        print()

        SYSTEM = [
            "  ██████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗  ",
            " ██╔════╝██║   ██║██╔════╝╚══██╔══╝██╔════╝████╗ ████║  ",
            " ╚█████╗ ██║   ██║███████╗   ██║   █████╗  ██╔████╔██║  ",
            "  ╚═══██╗╚██╗ ██╔╝╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║  ",
            " ██████╔╝ ╚████╔╝ ███████║   ██║   ███████╗██║ ╚═╝ ██║  ",
            " ╚═════╝   ╚═══╝  ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝  ",
        ]
        for i, line in enumerate(SYSTEM):
            shade = SH[(i+3) % len(SH)]
            for end in range(1, len(line)+1, 4):
                sys.stdout.write(f"\r{shade}{B}{line[:end].center(W)}{R}")
                sys.stdout.flush()
                time.sleep(0.006)
            sys.stdout.write(f"\r{shade}{B}{line.center(W)}{R}\n")
            sys.stdout.flush()

        spin = ["◐","◓","◑","◒","◐","◓","◑","◒","●","○","●"]
        for s in spin:
            sys.stdout.write(f"\r{C['c1']}{B}  {s}  MASTER SYSTEM READY  {s}  {R}")
            sys.stdout.flush()
            time.sleep(0.07)
        print()

        if user_level == "OWNER":
            lv = f"👑 OWNER MODE"; lc = C['c1']
        elif user_level == "ADMIN":
            lv = f"⚡ ADMIN MODE"; lc = C['c2']
        else:
            lv = f"👤 USER MODE"; lc = C['c3']

        info = f"◈  MASTER V12 READY  ·  {lv}  ·  PRO  ◈"
        print(f"{lc}{B}{info.center(W)}{R}")
        feat = "⚡ GENERATOR   💎 RARE FINDER   💑 COUPLES   🔥 ACTIVATOR"
        print(f"{C['c4']}{feat.center(W)}{R}")
        cred = "📱 @MASTER |  @MASTER |  🐙 github.com/MASTER"
        print(f"{C['c5']}{cred.center(W)}{R}")

        sys.stdout.write(f"\r{C['c1']}{B}╚{'═'*(W-2)}╝{R}\n\n")
        sys.stdout.flush()

        bar_w = min(50, W-20)
        for i in range(bar_w+1):
            filled = "█" * i
            empty  = "░" * (bar_w - i)
            pct    = int(i / bar_w * 100)
            shade  = SH[i % len(SH)]
            sys.stdout.write(f"\r  {C['c2']}LAUNCHING {shade}{B}[{filled}{C['dim']}{empty}{shade}] {pct:3d}%{R}  ")
            sys.stdout.flush()
            time.sleep(0.022)
        print(f"\n  {C['c1']}{B}✔  MASTER SYSTEM READY!{R}\n")

# =============================================================================
# ⚡ FAST REQUIREMENTS INSTALLER
# =============================================================================

VISUAL = VisualMaster()

def install_requirements():
    required = ['requests', 'pycryptodome', 'colorama', 'psutil', 'protobuf']
    print(f"{VISUAL.COLORS['info']}🔧 Checking requirements...{VISUAL.COLORS['reset']}")
    for pkg in required:
        try:
            if pkg == 'pycryptodome':
                import Crypto
            elif pkg == 'requests':
                import requests
            elif pkg == 'colorama':
                from colorama import Fore, Style, init
            elif pkg == 'psutil':
                import psutil
            elif pkg == 'protobuf':
                import google.protobuf
            print(f"{VISUAL.COLORS['success']}✅ {pkg} already installed{VISUAL.COLORS['reset']}")
        except ImportError:
            print(f"{VISUAL.COLORS['info']}📦 Installing {pkg}...{VISUAL.COLORS['reset']}")
            try:
                process = subprocess.Popen(
                    [sys.executable, '-m', 'pip', 'install', '--no-cache-dir', pkg, '-q'],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                try:
                    stdout, stderr = process.communicate(timeout=30)
                    if process.returncode == 0:
                        print(f"{VISUAL.COLORS['success']}✅ {pkg} installed{VISUAL.COLORS['reset']}")
                except subprocess.TimeoutExpired:
                    process.kill()
                    print(f"{VISUAL.COLORS['warning']}⚠️ {pkg} timeout, continuing...{VISUAL.COLORS['reset']}")
            except:
                print(f"{VISUAL.COLORS['warning']}⚠️ {pkg} install failed, continuing...{VISUAL.COLORS['reset']}")
            time.sleep(1)
    try:
        from colorama import Fore, Style, init
        init(autoreset=True)
    except:
        pass
    time.sleep(1)

install_requirements()

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
    AES_AVAILABLE = True
except:
    AES_AVAILABLE = False
    def aes_encrypt(data): return data.encode() if isinstance(data, str) else data

try:
    import MajoRLoGinrEq_pb2
    import MajoRLoGinrEs_pb2
    import PorTs_pb2
    NEW_PROTO_AVAILABLE = True
except ImportError:
    NEW_PROTO_AVAILABLE = False

# =============================================================================
# ⚙️ CONFIGURATION
# =============================================================================

class Config:
    VERSION = "12.0 ULTIMATE ADMIN CONTROL"
    MAX_THREADS = min(psutil.cpu_count() * 2, 16)
    USER_LEVEL = "OWNER" 

    SUCCESS = 0; RARE = 0; COUPLES = 0; ACTIVATED = 0; FAILED = 0; BIO = 0; ATTEMPTS = 0
    LOCK = threading.Lock()
    FILE_LOCKS = {}

    EXIT = False
    AUTO_ACT = False
    AUTO_BIO = False
    MAX_RETRIES = 5 if USER_LEVEL == "USER" else 10

    CUSTOM_PASS_PREFIX = "MASTER"
    CUSTOM_NAME_PREFIX = "MASTER"
    CUSTOM_RARITY_THRESHOLD = 3
    CUSTOM_TARGET = 999999999
    CURRENT_JSON_BASE = "accounts"
    CURRENT_ACTIVATED_BASE = "accounts-activated"

    if USER_LEVEL in ["ADMIN", "OWNER"]:
        DEBUG_MODE = True
        VERBOSE_LOGGING = True
        MAX_THREADS = min(psutil.cpu_count() * 4, 32)
        CAN_EDIT_CREDITS = True
    else:
        DEBUG_MODE = False
        VERBOSE_LOGGING = False
        CAN_EDIT_CREDITS = False

    if USER_LEVEL == "OWNER":
        BYPASS_RATE_LIMIT = True
        FORCE_GENERATION = True
        CUSTOM_API_PRIORITY = True
    else:
        BYPASS_RATE_LIMIT = False
        FORCE_GENERATION = False
        CUSTOM_API_PRIORITY = False

    RARITY_THRESHOLD = 3

    BIO_TEXT = "[FF0000]🌈[FF7700]M[FFFF00]A[00FF00]S[00BFFF]T[8B00FF]E[FF0000]R[FF0000]🌈"

    REGION_LANG = {
        "ME": "ar", "IND": "hi", "ID": "id", "VN": "vi", "TH": "th",
        "BD": "bn", "PK": "ur", "TW": "zh", "CIS": "ru", "SAC": "es", "BR": "pt"
    }

    ACTIVATION_REGIONS = {
        'IND': {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
                'major_login_url': 'https://loginbp.common.ggbluefox.com/MajorLogin',
                'get_login_data_url': 'https://client.ind.freefiremobile.com/GetLoginData',
                'client_host': 'client.ind.freefiremobile.com'},
        'BD':  {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
                'major_login_url': 'https://loginbp.ggpolarbear.com/MajorLogin',
                'get_login_data_url': 'https://clientbp.ggpolarbear.com/GetLoginData',
                'client_host': 'clientbp.ggpolarbear.com'},
        'PK':  {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
                'major_login_url': 'https://loginbp.ggpolarbear.com/MajorLogin',
                'get_login_data_url': 'https://clientbp.ggpolarbear.com/GetLoginData',
                'client_host': 'clientbp.ggpolarbear.com'},
        'ID':  {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
                'major_login_url': 'https://loginbp.ggpolarbear.com/MajorLogin',
                'get_login_data_url': 'https://clientbp.ggpolarbear.com/GetLoginData',
                'client_host': 'clientbp.ggpolarbear.com'},
        'TH':  {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
                'major_login_url': 'https://loginbp.ggpolarbear.com/MajorLogin',
                'get_login_data_url': 'https://clientbp.common.ggbluefox.com/GetLoginData',
                'client_host': 'clientbp.common.ggbluefox.com'},
        'VN':  {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
                'major_login_url': 'https://loginbp.ggpolarbear.com/MajorLogin',
                'get_login_data_url': 'https://clientbp.ggpolarbear.com/GetLoginData',
                'client_host': 'clientbp.ggpolarbear.com'},
        'ME':  {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
                'major_login_url': 'https://loginbp.common.ggbluefox.com/MajorLogin',
                'get_login_data_url': 'https://clientbp.ggpolarbear.com/GetLoginData',
                'client_host': 'clientbp.ggpolarbear.com'},
        'BR':  {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
                'major_login_url': 'https://loginbp.ggpolarbear.com/MajorLogin',
                'get_login_data_url': 'https://clientbp.ggpolarbear.com/GetLoginData',
                'client_host': 'clientbp.ggpolarbear.com'},
        'NA':  {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
                'major_login_url': 'https://loginbp.ggpolarbear.com/MajorLogin',
                'get_login_data_url': 'https://clientbp.ggpolarbear.com/GetLoginData',
                'client_host': 'clientbp.ggpolarbear.com'},
        'LK':  {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
                'major_login_url': 'https://loginbp.ggpolarbear.com/MajorLogin',
                'get_login_data_url': 'https://clientbp.ggpolarbear.com/GetLoginData',
                'client_host': 'clientbp.ggpolarbear.com'},
    }

    HEX_KEY = "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"
    API_KEY  = bytes.fromhex(HEX_KEY)

    REGISTER_URL      = "https://100067.connect.garena.com/api/v2/oauth/guest:register"
    TOKEN_URL         = "https://100067.connect.garena.com/api/v2/oauth/guest/token:grant"
    MAJOR_REGISTER_URL = "https://loginbp.ggpolarbear.com/MajorRegister"
    MAJOR_LOGIN_URL    = "https://loginbp.ggpolarbear.com/MajorLogin"

    CURRENT_DIR            = os.path.dirname(os.path.abspath(__file__))
    BASE_FOLDER            = os.path.join(CURRENT_DIR, "GUEST-GEN")
    TOKENS_FOLDER          = os.path.join(BASE_FOLDER, "TOKENS")
    ACCOUNTS_FOLDER        = os.path.join(BASE_FOLDER, "ACCOUNTS")
    RARE_ACCOUNTS_FOLDER   = os.path.join(BASE_FOLDER, "RARE_ACCOUNTS")
    COUPLES_ACCOUNTS_FOLDER= os.path.join(BASE_FOLDER, "COUPLES_ACCOUNTS")
    GHOST_FOLDER           = os.path.join(BASE_FOLDER, "GHOST")
    GHOST_ACCOUNTS_FOLDER  = os.path.join(GHOST_FOLDER, "ACCOUNTS")
    GHOST_RARE_FOLDER      = os.path.join(GHOST_FOLDER, "RARE_ACCOUNTS")
    GHOST_COUPLES_FOLDER   = os.path.join(GHOST_FOLDER, "COUPLES_ACCOUNTS")
    ACTIVATED_FOLDER       = os.path.join(BASE_FOLDER, "ACTIVATED")
    FAILED_ACTIVATION_FOLDER = os.path.join(BASE_FOLDER, "FAILED_ACTIVATION")
    CONFIG_FOLDER          = os.path.join(BASE_FOLDER, "CONFIG")
    BACKUP_FOLDER          = os.path.join(BASE_FOLDER, "BACKUP")

    @classmethod
    def create_folders(cls):
        folders = [
            cls.BASE_FOLDER, cls.TOKENS_FOLDER, cls.ACCOUNTS_FOLDER,
            cls.RARE_ACCOUNTS_FOLDER, cls.COUPLES_ACCOUNTS_FOLDER,
            cls.GHOST_FOLDER, cls.GHOST_ACCOUNTS_FOLDER, cls.GHOST_RARE_FOLDER,
            cls.GHOST_COUPLES_FOLDER, cls.ACTIVATED_FOLDER,
            cls.FAILED_ACTIVATION_FOLDER, cls.CONFIG_FOLDER, cls.BACKUP_FOLDER
        ]
        print(f"{VISUAL.COLORS['info']}📁 Creating folders...{VISUAL.COLORS['reset']}")
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
        print(f"{VISUAL.COLORS['success']}✅ Folders ready!{VISUAL.COLORS['reset']}")
        time.sleep(1)
        # =============================================================================
# 🔑 ACCOUNT GENERATION HELPERS
# =============================================================================

def generate_exponent_number():
    exponent_digits = {'0': '⁰','1': '¹','2': '²','3': '³','4': '⁴',
                       '5': '⁵','6': '⁶','7': '⁷','8': '⁸','9': '⁹'}
    number = random.randint(1, 99999)
    return ''.join(exponent_digits[d] for d in f"{number:05d}")

def generate_random_name():
    base = Config.CUSTOM_NAME_PREFIX if Config.CUSTOM_NAME_PREFIX else "MASTER"
    designs = [
        '▲','ℳ','☆','°','ℛ','『','ツ',
        '◇','༺','◆','웃','꧁','彡','★','ン',
        '•','乂','⍤','유','ヅ','Ø','♪','Ƹ','⌂','シ','⊹',
        '·','∞','♡','✦','✧','◈','▸','꧂','༻','࿐',
        'ʜ','ɪ','ᴋ','ᴍ','ɴ','ꪆ','ꪀ','』','「','」',
        '〖','〗','【','】','《','》','ッ','ジ','ヅ','亗',
        'ℳ','ℛ','Ɽ','Ƈ','Ƨ','Ƴ','Ʀ','Ƶ','⋆','⋈',
    ]
    designs = list(dict.fromkeys(designs))
    count = random.randint(3, 4)
    suffix = ''.join(random.choices(designs, k=count))
    return f"{base}{suffix}"

def generate_custom_password():
    prefix = Config.CUSTOM_PASS_PREFIX if Config.CUSTOM_PASS_PREFIX else "MASTER"
    clean_prefix = ''.join(c for c in prefix if c.isalnum() or c == '_')
    if not clean_prefix:
        clean_prefix = "MASTER"
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    password = f"{clean_prefix}_MASTER_{random_part}"
    if len(password) > 64:
        password = password[:64]
    return password

def smart_delay():
    time.sleep(random.uniform(0.01, 0.05))

def encode_string(original):
    keystream = [0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,
                 0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30]
    encoded = ""
    for i in range(len(original)):
        encoded += chr(ord(original[i]) ^ keystream[i % len(keystream)])
    return {"open_id": original, "field_14": encoded}

def to_unicode_escaped(s):
    return ''.join(c if 32 <= ord(c) <= 126 else '\\u{:04x}'.format(ord(c)) for c in s)

def decode_jwt_token(jwt_token):
    try:
        parts = jwt_token.split('.')
        if len(parts) >= 2:
            payload_part = parts[1]
            padding = 4 - len(payload_part) % 4
            if padding != 4:
                payload_part += '=' * padding
            decoded = base64.urlsafe_b64decode(payload_part)
            data = json.loads(decoded)
            account_id = data.get('account_id') or data.get('external_id')
            if account_id:
                return str(account_id)
    except:
        pass
    return "N/A"
    # =============================================================================
# 🔐 ASYNC PROTOBUF HELPERS (from OB54new.zip)
# =============================================================================

async def EnC_Vr(N):
    if N < 0: return b''
    H = []
    while True:
        BesTo = N & 0x7F
        N >>= 7
        if N: BesTo |= 0x80
        H.append(BesTo)
        if not N: break
    return bytes(H)

async def CrEaTe_VarianT(field_number, value):
    return await EnC_Vr((field_number << 3) | 0) + await EnC_Vr(value)

async def CrEaTe_LenGTh(field_number, value):
    h = await EnC_Vr((field_number << 3) | 2)
    e = value.encode() if isinstance(value, str) else value
    return h + await EnC_Vr(len(e)) + e

async def CrEaTe_ProTo(fields):
    p = bytearray()
    for f, v in fields.items():
        if isinstance(v, dict):
            p.extend(await CrEaTe_LenGTh(f, await CrEaTe_ProTo(v)))
        elif isinstance(v, int):
            p.extend(await CrEaTe_VarianT(f, v))
        elif isinstance(v, (str, bytes)):
            p.extend(await CrEaTe_LenGTh(f, v))
    return p

def run_async(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

def E_AEs(Pc):
    if not AES_AVAILABLE:
        return bytes.fromhex(Pc)
    Z = bytes.fromhex(Pc)
    key = bytes([89,103,38,116,99,37,68,69,117,104,54,37,90,99,94,56])
    iv  = bytes([54,111,121,90,68,114,50,50,69,51,121,99,104,106,77,37])
    K = AES.new(key, AES.MODE_CBC, iv)
    return K.encrypt(pad(Z, AES.block_size))

def encrypt_api(plain_text):
    if not AES_AVAILABLE:
        return plain_text
    Z = bytes.fromhex(plain_text)
    key = bytes([89,103,38,116,99,37,68,69,117,104,54,37,90,99,94,56])
    iv  = bytes([54,111,121,90,68,114,50,50,69,51,121,99,104,106,77,37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(Z, AES.block_size)).hex()

# =============================================================================
# 🔌 API MASTER  (OB54 — new /api/v2/ JSON endpoints)
# =============================================================================

class APIMaster:
    HEX_KEY  = Config.HEX_KEY
    API_KEY  = Config.API_KEY
    API_POOL = [{"id": "100067", "key": Config.API_KEY, "label": f"API {i:02d} ⚡"} for i in range(1, 8)]

    @classmethod
    def init(cls):
        more_ids = ["100068","100069","100070","100071","100072"]
        for i, api_id in enumerate(more_ids, start=len(cls.API_POOL)+1):
            cls.API_POOL.append({"id": api_id, "key": cls.API_KEY, "label": f"API {i:02d} ⚡"})
        return len(cls.API_POOL)

API_COUNT = APIMaster.init()

# =============================================================================
# 📝 CREDIT EDITOR (ADMIN ONLY)
# =============================================================================

class CreditEditor:
    CREDIT_FILE = os.path.join(Config.CONFIG_FOLDER, "credit_config.json")

    @classmethod
    def load_credits(cls):
        default_credits = {
            "primary_credit": "MASTER",
            "github": "https://github.com/OOO",
            "telegram1": "@MASTER",
            "telegram2": "@MASTER",
            "display_name": "MASTER",
            "banner_text": "⚡ POWERED BY MASTER⚡",
            "footer_text": "👤 CREDIT: MASTER| TELEGRAM: @MASTER,@MASTER| GITHUB: MASTER",
            "bio_text": "[FF0000]🌈[FF7700]M[FFFF00]A[00FF00]S[00BFFF]T[8B00FF]E[FF0000]R[FF0000]🌈",
            "last_modified": datetime.now().isoformat(),
            "modified_by": Config.USER_LEVEL
        }
        try:
            if os.path.exists(cls.CREDIT_FILE):
                with open(cls.CREDIT_FILE, 'r') as f:
                    return json.load(f)
            else:
                cls.save_credits(default_credits)
                return default_credits
        except:
            return default_credits

    @classmethod
    def save_credits(cls, credits):
        try:
            credits["last_modified"] = datetime.now().isoformat()
            credits["modified_by"] = Config.USER_LEVEL
            os.makedirs(os.path.dirname(cls.CREDIT_FILE), exist_ok=True)
            with open(cls.CREDIT_FILE, 'w') as f:
                json.dump(credits, f, indent=4)
            return True
        except:
            return False

    @classmethod
    def backup_current_file(cls):
        try:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
            backup_path = os.path.join(Config.BACKUP_FOLDER, backup_name)
            shutil.copy2(__file__, backup_path)
            return backup_path
        except:
            return None

# =============================================================================
# 🔐 FILE LOCK / JSON
# =============================================================================

def get_file_lock(filename):
    if filename not in Config.FILE_LOCKS:
        Config.FILE_LOCKS[filename] = threading.Lock()
    return Config.FILE_LOCKS[filename]

def safe_json_save(filepath, data):
    try:
        parent = os.path.dirname(filepath)
        if parent and not os.path.isdir(parent):
            os.makedirs(parent, exist_ok=True)
        temp = filepath + '.tmp'
        with open(temp, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        os.replace(temp, filepath) if os.path.exists(filepath) else os.rename(temp, filepath)
        return True
    except:
        return False

def safe_json_load(filepath, default=None):
    try:
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return default if default is not None else []

# =============================================================================
# 🔄 COUPLES DETECTION
# =============================================================================

POTENTIAL_COUPLES = {}
COUPLES_LOCK = threading.Lock()

# =============================================================================
# 🚦 SIGNAL HANDLING
# =============================================================================

EXIT_FLAG = False

def safe_exit(signum=None, frame=None):
    global EXIT_FLAG
    EXIT_FLAG = True
    print(f"\n{VISUAL.COLORS['warning']}🚨 Shutting down...{VISUAL.COLORS['reset']}")
    sys.exit(0)

signal.signal(signal.SIGINT, safe_exit)
signal.signal(signal.SIGTERM, safe_exit)

# =============================================================================
# 🖨️ PRINT FUNCTIONS
# =============================================================================

C = VISUAL.COLORS

GENERATION_SILENT = False

def print_success(msg):
    if not GENERATION_SILENT: print(f"{C['success']}{C['bold']}✅ {msg}{C['reset']}")
def print_error(msg):
    if not GENERATION_SILENT: print(f"{C['error']}{C['bold']}❌ {msg}{C['reset']}")
def print_warning(msg):
    if not GENERATION_SILENT: print(f"{C['warning']}{C['bold']}⚠️  {msg}{C['reset']}")
def print_info(msg):
    if not GENERATION_SILENT: print(f"{C['info']}ℹ️  {msg}{C['reset']}")
def print_rare(msg):
    if not GENERATION_SILENT: print(f"{C['rare']}{C['bold']}💎 {msg}{C['reset']}")
def print_couple(msg):
    if not GENERATION_SILENT: print(f"{C['couple']}{C['bold']}💑 {msg}{C['reset']}")
def print_activation(msg):
    if not GENERATION_SILENT: print(f"{C['primary']}{C['bold']}🔥 {msg}{C['reset']}")

def debug_print(msg):
    if not GENERATION_SILENT and Config.USER_LEVEL in ["ADMIN","OWNER"] and Config.DEBUG_MODE:
        print(f"{C['dim']}🔍 DEBUG: {msg}{C['reset']}")

# =============================================================================
# 🔐 BIO FUNCTION  (Direct — no external API needed)
# =============================================================================

BIO_SET_COUNTER = 0

try:
    from google.protobuf import descriptor_pool as _bio_dp
    from google.protobuf import symbol_database as _bio_sym_db
    from google.protobuf.internal import builder as _bio_builder
    _BIO_PROTO = (
        b'\n\ndata.proto\"\xbb\x01\n\x04\x44\x61ta'
        b'\x12\x0f\n\x07\x66ield_2\x18\x02 \x01(\x05'
        b'\x12\x1e\n\x07\x66ield_5\x18\x05 \x01(\x0b\x32\r.EmptyMessage'
        b'\x12\x1e\n\x07\x66ield_6\x18\x06 \x01(\x0b\x32\r.EmptyMessage'
        b'\x12\x0f\n\x07\x66ield_8\x18\x08 \x01(\t'
        b'\x12\x0f\n\x07\x66ield_9\x18\t \x01(\x05'
        b'\x12\x1f\n\x08\x66ield_11\x18\x0b \x01(\x0b\x32\r.EmptyMessage'
        b'\x12\x1f\n\x08\x66ield_12\x18\x0c \x01(\x0b\x32\r.EmptyMessage'
        b'\"\x0e\n\x0c\x45mptyMessageb\x06proto3'
    )
    _bio_builder.BuildMessageAndEnumDescriptors(
        _bio_dp.Default().AddSerializedFile(_BIO_PROTO), globals()
    )
    _bio_builder.BuildTopDescriptorsAndMessages(
        _bio_dp.Default().AddSerializedFile(_BIO_PROTO), 'bio_inline_pb2', globals()
    )
    _BioData      = _bio_sym_db.Default().GetSymbol('Data')
    _EmptyMessage = _bio_sym_db.Default().GetSymbol('EmptyMessage')
    BIO_PROTO_AVAILABLE = True
except Exception:
    BIO_PROTO_AVAILABLE = False

_BIO_SERVERS = {
    "IND": "https://client.ind.freefiremobile.com/UpdateSocialBasicInfo",
    "BD":  "https://clientbp.ggblueshark.com/UpdateSocialBasicInfo",
    "SG":  "https://clientbp.ggblueshark.com/UpdateSocialBasicInfo",
    "PK":  "https://clientbp.ggblueshark.com/UpdateSocialBasicInfo",
    "ID":  "https://clientbp.ggblueshark.com/UpdateSocialBasicInfo",
    "VN":  "https://clientbp.ggblueshark.com/UpdateSocialBasicInfo",
    "TH":  "https://clientbp.common.ggbluefox.com/UpdateSocialBasicInfo",
    "ME":  "https://clientbp.common.ggbluefox.com/UpdateSocialBasicInfo",
    "BR":  "https://client.us.freefiremobile.com/UpdateSocialBasicInfo",
    "US":  "https://client.us.freefiremobile.com/UpdateSocialBasicInfo",
    "EU":  "https://clientbp.ggpolarbear.com/UpdateSocialBasicInfo",
}

_BIO_HEADERS = {
    "Expect":          "100-continue",
    "X-Unity-Version": "2018.4.11f1",
    "X-GA":            "v1 1",
    "ReleaseVersion":  "OB54",
    "Content-Type":    "application/x-www-form-urlencoded",
    "User-Agent":      "Dalvik/2.1.0 (Linux; U; Android 11; SM-A305F Build/RP1A.200720.012)",
    "Connection":      "Keep-Alive",
    "Accept-Encoding": "gzip",
}

_BIO_AES_KEY = bytes([89,103,38,116,99,37,68,69,117,104,54,37,90,99,94,56])
_BIO_AES_IV  = bytes([54,111,121,90,68,114,50,50,69,51,121,99,104,106,77,37])

def _bio_encrypt(data_bytes):
    if not AES_AVAILABLE:
        return data_bytes
    from Crypto.Cipher import AES as _AES
    from Crypto.Util.Padding import pad as _pad
    cipher = _AES.new(_BIO_AES_KEY, _AES.MODE_CBC, _BIO_AES_IV)
    return cipher.encrypt(_pad(data_bytes, _AES.block_size))

def _bio_guest_login(uid, password):
    try:
        payload = {
            'uid':           str(uid),
            'password':      str(password),
            'response_type': 'token',
            'client_type':   '2',
            'client_secret': Config.HEX_KEY,
            'client_id':     '100067',
        }
        headers = {'User-Agent': 'GarenaMSDK/4.0.19P9(SM-M526B ;Android 13;pt;BR;)',
                   'Connection': 'Keep-Alive'}
        resp = requests.post(
            'https://100067.connect.garena.com/oauth/guest/token/grant',
            data=payload, headers=headers, timeout=10, verify=False
        )
        data = resp.json()
        return data.get('access_token'), data.get('open_id')
    except:
        return None, None

def _bio_major_login(access_token, open_id):
    try:
        import my_pb2 as _my_pb2
        import output_pb2 as _out_pb2
    except ImportError:
        return None

    _login_headers = {
        "User-Agent":      "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
        "Connection":      "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Content-Type":    "application/octet-stream",
        "Expect":          "100-continue",
        "X-Unity-Version": "2018.4.11f1",
        "X-GA":            "v1 1",
        "ReleaseVersion":  "OB54",
    }
    for p_type in [8, 3, 4, 6]:
        try:
            gd = _my_pb2.GameData()
            gd.timestamp     = "2024-12-05 18:15:32"
            gd.game_name     = "free fire"
            gd.game_version  = 1
            gd.version_code  = "1.120.2"
            gd.os_info       = "Android OS 9 / API-28"
            gd.device_type   = "Handheld"
            gd.network_provider = "Verizon Wireless"
            gd.connection_type  = "WIFI"
            gd.screen_width  = 1280
            gd.screen_height = 960
            gd.dpi           = "240"
            gd.cpu_info      = "ARMv7 VFPv3 NEON VMH | 2400 | 4"
            gd.total_ram     = 5951
            gd.gpu_name      = "Adreno (TM) 640"
            gd.gpu_version   = "OpenGL ES 3.0"
            gd.user_id       = "Google|74b585a9-0268-4ad3-8f36-ef41d2e53610"
            gd.ip_address    = "172.190.111.97"
            gd.language      = "en"
            gd.open_id       = open_id
            gd.access_token  = access_token
            gd.platform_type = p_type
            gd.field_99      = str(p_type)
            gd.field_100     = str(p_type)

            encrypted = _bio_encrypt(gd.SerializeToString())
            resp = requests.post(
                "https://loginbp.ggblueshark.com/MajorLogin",
                data=encrypted, headers=_login_headers,
                verify=False, timeout=10
            )
            if resp.status_code == 200:
                msg = _out_pb2.Garena_420()
                msg.ParseFromString(resp.content)
                token = getattr(msg, 'token', None)
                if token:
                    return token
        except:
            continue
    return None

def _bio_update(jwt_token, bio_text, region):
    if not BIO_PROTO_AVAILABLE:
        return False
    try:
        url = _BIO_SERVERS.get(region.upper(), _BIO_SERVERS["BD"])
        data = _BioData()
        data.field_2 = 17
        data.field_5.CopyFrom(_EmptyMessage())
        data.field_6.CopyFrom(_EmptyMessage())
        data.field_8 = bio_text
        data.field_9 = 1
        data.field_11.CopyFrom(_EmptyMessage())
        data.field_12.CopyFrom(_EmptyMessage())

        encrypted = _bio_encrypt(data.SerializeToString())
        headers = _BIO_HEADERS.copy()
        headers['Authorization'] = f'Bearer {jwt_token}'
        r = requests.post(url, headers=headers, data=encrypted, verify=False, timeout=10)
        return r.status_code == 200
    except:
        return False

def set_account_bio(uid, password, bio_text, region="BD", existing_jwt=None):
    global BIO_SET_COUNTER
    if not Config.AUTO_BIO:
        return False
    try:
        bio_to_use = Config.BIO_TEXT
        jwt_token  = existing_jwt

        if not jwt_token:
            debug_print(f"Bio: guest login for uid={uid}")
            access_token, open_id = _bio_guest_login(uid, password)
            if not access_token or not open_id:
                debug_print("Bio: guest login failed")
                return False

            sess = requests.Session()
            login_result = _perform_major_login_sync(
                uid, password, access_token, open_id, region, sess
            )
            jwt_token = login_result.get("jwt_token", "")

        if not jwt_token:
            debug_print("Bio: could not obtain JWT")
            return False

        debug_print(f"Bio: updating bio for uid={uid}")
        success = _bio_update(jwt_token, bio_to_use, region)
        if success:
            with Config.LOCK:
                BIO_SET_COUNTER += 1
            return True
        else:
            debug_print(f"Bio: update request failed for uid={uid}")
    except Exception as e:
        debug_print(f"Bio error: {e}")
    return False

# =============================================================================
# 💎 RARITY DETECTION
# =============================================================================

ACCOUNT_RARITY_PATTERNS = {
    "REPEATED_DIGITS_4":       [r"(\d)\1{3,}", 3],
    "REPEATED_DIGITS_3":       [r"(\d)\1\1(\d)\2\2", 2],
    "SEQUENTIAL_5":            [r"(12345|23456|34567|45678|56789)", 4],
    "SEQUENTIAL_4":            [r"(0123|1234|2345|3456|4567|45678|5678|6789|9876|8765|7654|6543|5432|4321|3210)", 3],
    "PALINDROME_6":            [r"^(\d)(\d)(\d)\3\2\1$", 5],
    "PALINDROME_4":            [r"^(\d)(\d)\2\1$", 3],
    "SPECIAL_COMBINATIONS_HIGH":[r"(69|420|1337|007)", 4],
    "SPECIAL_COMBINATIONS_MED": [r"(100|200|300|400|500|666|777|888|999)", 2],
    "QUADRUPLE_DIGITS":        [r"(1111|2222|3333|4444|5555|6666|7777|8888|9999|0000)", 4],
    "MIRROR_PATTERN_HIGH":     [r"^(\d{2,3})\1$", 3],
    "MIRROR_PATTERN_MED":      [r"(\d{2})0\1", 2],
    "GOLDEN_RATIO":            [r"1618|0618", 3],
}

def check_account_rarity(account_data):
    account_id = account_data.get("account_id", "")
    if account_id == "N/A" or not account_id:
        return False, None, None, 0
    rarity_score = 0
    detected_patterns = []
    for rarity_type, pattern_data in ACCOUNT_RARITY_PATTERNS.items():
        if re.search(pattern_data[0], account_id):
            rarity_score += pattern_data[1]
            detected_patterns.append(rarity_type)
    digits = [int(d) for d in account_id if d.isdigit()]
    if len(set(digits)) == 1 and len(digits) >= 4:
        rarity_score += 5; detected_patterns.append("UNIFORM_DIGITS")
    if len(digits) >= 4:
        diffs = [digits[i+1] - digits[i] for i in range(len(digits)-1)]
        if len(set(diffs)) == 1:
            rarity_score += 4; detected_patterns.append("ARITHMETIC_SEQUENCE")
    if len(account_id) <= 8 and account_id.isdigit() and int(account_id) < 1000000:
        rarity_score += 3; detected_patterns.append("LOW_ACCOUNT_ID")
    threshold = Config.CUSTOM_RARITY_THRESHOLD if Config.USER_LEVEL in ["ADMIN","OWNER"] else Config.RARITY_THRESHOLD
    if rarity_score >= threshold:
        reason = f"ID {account_id} — Score: {rarity_score} — Patterns: {', '.join(detected_patterns)}"
        return True, "RARE_ACCOUNT", reason, rarity_score
    return False, None, None, rarity_score

def check_account_couples(account_data, thread_id):
    account_id = account_data.get("account_id", "")
    if account_id == "N/A" or not account_id:
        return False, None, None
    with COUPLES_LOCK:
        for stored_id, stored_data in list(POTENTIAL_COUPLES.items()):
            couple_found, reason = check_account_couple_patterns(account_id, stored_data.get('account_id', ''))
            if couple_found:
                partner_data = stored_data
                del POTENTIAL_COUPLES[stored_id]
                return True, reason, partner_data
        POTENTIAL_COUPLES[account_id] = {
            'uid': account_data.get('uid',''), 'account_id': account_id,
            'name': account_data.get('name',''), 'password': account_data.get('password',''),
            'region': account_data.get('region',''), 'thread_id': thread_id,
            'timestamp': datetime.now().isoformat()
        }
    return False, None, None

def check_account_couple_patterns(a1, a2):
    if a1 and a2 and abs(int(a1) - int(a2)) == 1:
        return True, f"Sequential IDs: {a1} & {a2}"
    if a1 == a2[::-1]:
        return True, f"Mirror IDs: {a1} & {a2}"
    if a1 and a2:
        s = int(a1) + int(a2)
        if s % 1000 == 0 or s % 10000 == 0:
            return True, f"Complementary sum: {a1}+{a2}={s}"
    for ln in ['520','521','1314','3344']:
        if ln in a1 and ln in a2:
            return True, f"Both contain love number: {ln}"
    return False, None

def print_rarity_found(account_data, rarity_type, reason, rarity_score):
    import sys, time
    RED  = '\033[38;5;196m'
    RED2 = '\033[38;5;160m'
    B = VISUAL.COLORS['bold']; R = VISUAL.COLORS['reset']
    W = 54
    for _ in range(4):
        for ch in ['░','▒','▓','█','▓','▒']:
            sys.stdout.write(f"\r{RED}{B}╔" + ch*W + f"╗{R}")
            sys.stdout.flush(); time.sleep(0.010)
    print()
    print(f"{RED}{B}╔{'═'*W}╗{R}")
    print(f"{RED}{B}║{'💎  RARE ACCOUNT FOUND!  💎'.center(W)}║{R}")
    print(f"{RED}{B}╠{'═'*W}╣{R}")
    def row(k, v):
        line = f"  {k}: {v}"
        pad  = max(0, W - len(line) - 1)
        print(f"{RED}{B}║{R}  {RED2}{k}{R}: {RED}{B}{v}{R}{' '*pad}{RED}{B}║{R}")
    row("🎯 Type   ", str(rarity_type))
    row("⭐ Score  ", str(rarity_score))
    row("👤 Name   ", account_data['name'])
    row("🆔 UID    ", str(account_data['uid']))
    row("🎮 Acct ID", account_data.get('account_id', 'N/A'))
    row("📝 Reason ", str(reason)[:45])
    print(f"{RED}{B}╠{'═'*W}╣{R}")
    print(f"{RED}{B}║{'🔴  SAVED TO RARE ACCOUNTS  🔴'.center(W)}║{R}")
    print(f"{RED}{B}╚{'═'*W}╝{R}\n")

def print_couples_found(account1, account2, reason):
    import sys, time
    GRN  = '\033[38;5;46m'
    GRN2 = '\033[38;5;40m'
    GRN3 = '\033[38;5;34m'
    B = VISUAL.COLORS['bold']; R = VISUAL.COLORS['reset']
    W = 58
    for ch in ['·','◇','◈','═']:
        sys.stdout.write(f"\r{GRN}{B}╔" + ch*W + f"╗{R}")
        sys.stdout.flush(); time.sleep(0.022)
    print()
    print(f"{GRN}{B}╔{'═'*W}╗{R}")
    print(f"{GRN}{B}║{'💑  COUPLES ACCOUNT FOUND!  💑'.center(W)}║{R}")
    print(f"{GRN}{B}╠{'═'*W}╣{R}")
    def row(k, v):
        line = f"  {k}: {v}"
        pad  = max(0, W - len(line) - 1)
        print(f"{GRN}{B}║{R}  {GRN3}{k}{R}: {GRN}{B}{v}{R}{' '*pad}{GRN}{B}║{R}")
    row("📝 Reason  ", str(reason))
    print(f"{GRN}{B}╠{'─'*W}╣{R}")
    print(f"{GRN}{B}║{'  ACCOUNT  1  '.center(W)}║{R}")
    row("👤 Name    ", account1['name'])
    row("🆔 UID     ", str(account1.get('uid','N/A')))
    row("🎮 Acct ID ", account1.get('account_id','N/A'))
    print(f"{GRN}{B}╠{'─'*W}╣{R}")
    print(f"{GRN}{B}║{'  ACCOUNT  2  '.center(W)}║{R}")
    row("👤 Name    ", account2['name'])
    row("🆔 UID     ", str(account2.get('uid','N/A')))
    row("🎮 Acct ID ", account2.get('account_id','N/A'))
    print(f"{GRN}{B}╠{'═'*W}╣{R}")
    print(f"{GRN}{B}║{'💚  SAVED TO COUPLES FILE  💚'.center(W)}║{R}")
    print(f"{GRN}{B}╚{'═'*W}╝{R}\n")
    # =============================================================================
# ⚡ AUTO ACTIVATOR (disabled – kept for reference but never called)
# =============================================================================

class AutoActivator:
    def __init__(self, max_workers=8, turbo_mode=True):
        self.key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        self.iv  = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
        self.max_workers    = max_workers
        self.turbo_mode     = turbo_mode
        self.stop_execution = False
        self.stats_lock     = threading.Lock()
        self.unauthorized_count = 0
        self.max_unauthorized_before_stop = 15

        self.session  = requests.Session()
        self.adapters = self._create_optimized_adapters()
        self._rotate_adapter()

    def _create_optimized_adapters(self):
        configs = [
            {'pool_connections': 100, 'pool_maxsize': 100, 'max_retries': 1},
            {'pool_connections': 50,  'pool_maxsize': 50,  'max_retries': 0},
            {'pool_connections': 75,  'pool_maxsize': 75,  'max_retries': 2},
        ]
        return [requests.adapters.HTTPAdapter(**c) for c in configs]

    def _rotate_adapter(self):
        adapter = random.choice(self.adapters)
        self.session.mount('http://',  adapter)
        self.session.mount('https://', adapter)

    def generate_fingerprint(self):
        user_agents = [
            'Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)',
            'Dalvik/2.1.0 (Linux; U; Android 10; SM-G973F Build/QP1A.190711.020)',
            'Dalvik/2.1.0 (Linux; U; Android 11; Pixel 5 Build/RQ3A.210805.001)',
            'Dalvik/2.1.0 (Linux; U; Android 12; SM-A525F Build/SP1A.210812.016)',
            'Dalvik/2.1.0 (Linux; U; Android 13; Redmi Note 12 Build/TKQ1.220829.002)',
            'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 Chrome/91 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 Chrome/92 Mobile Safari/537.36',
        ]
        self.session.headers.update({
            'User-Agent': random.choice(user_agents),
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
        })
        self._rotate_adapter()

    def smart_rate_limit_bypass(self):
        delay = random.uniform(0.03, 0.12) if self.turbo_mode else random.uniform(0.1, 0.25)
        time.sleep(delay)
        self.generate_fingerprint()

    def advanced_retry_strategy(self, attempt, max_attempts=3):
        base  = 1.5 ** attempt if self.turbo_mode else 2 ** attempt
        delay = base * random.uniform(0.8, 1.5)
        time.sleep(min(delay, 8.0))

    def encrypt_api(self, plain_text):
        if not AES_AVAILABLE:
            return plain_text
        try:
            plain_text = bytes.fromhex(plain_text)
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            return cipher.encrypt(pad(plain_text, AES.block_size)).hex()
        except:
            return None

    def parse_my_message(self, serialized_data):
        try:
            import MajorLoginRes_pb2 as _mlr
            msg = _mlr.MajorLoginRes()
            msg.ParseFromString(serialized_data)
            jwt   = msg.token
            key_h = msg.ak.hex()  if msg.ak  else None
            iv_h  = msg.aiv.hex() if msg.aiv else None
            if jwt:
                return jwt, key_h, iv_h
        except Exception:
            pass

        if NEW_PROTO_AVAILABLE:
            try:
                res = MajoRLoGinrEs_pb2.MajorLoginRes()
                res.ParseFromString(serialized_data)
                if res.token:
                    key_b = bytes(res.ak)  if res.ak  else None
                    iv_b  = bytes(res.aiv) if res.aiv else None
                    return res.token, (key_b.hex() if key_b else None), (iv_b.hex() if iv_b else None)
            except Exception:
                pass

        try:
            text = serialized_data.decode('utf-8', errors='ignore')
            jwt_start = text.find("eyJ")
            if jwt_start != -1:
                jwt_token = text[jwt_start:]
                second_dot = jwt_token.find(".", jwt_token.find(".") + 1)
                if second_dot != -1:
                    return jwt_token[:second_dot + 44], None, None
        except Exception:
            pass

        return None, None, None

    def guest_token(self, uid, password, region='IND'):
        if self.stop_execution:
            return None, None
        region_config = Config.ACTIVATION_REGIONS.get(region, Config.ACTIVATION_REGIONS['IND'])
        url = region_config['guest_url']
        data = {
            "uid": f"{uid}", "password": f"{password}",
            "response_type": "token", "client_type": "2",
            "client_secret": Config.HEX_KEY, "client_id": "100067",
        }
        max_attempts = 4 if self.turbo_mode else 3
        for attempt in range(max_attempts):
            try:
                if self.stop_execution:
                    return None, None
                self.smart_rate_limit_bypass()
                timeout = 8 if self.turbo_mode else 15
                response = self.session.post(url, data=data, timeout=timeout, verify=False)
                if response.status_code == 200:
                    d = response.json()
                    return d.get('access_token'), d.get('open_id')
                elif response.status_code == 429:
                    self.advanced_retry_strategy(attempt, max_attempts)
                    continue
                elif response.status_code in [400, 401, 403]:
                    if response.status_code == 401:
                        with self.stats_lock:
                            self.unauthorized_count += 1
                            if self.unauthorized_count >= self.max_unauthorized_before_stop:
                                self.stop_execution = True
                    return None, None
            except requests.exceptions.Timeout:
                pass
            except Exception:
                pass
            if attempt < max_attempts - 1:
                self.advanced_retry_strategy(attempt, max_attempts)
        return None, None

    def major_login(self, access_token, open_id, region='IND'):
        if self.stop_execution:
            return None
        region_config = Config.ACTIVATION_REGIONS.get(region, Config.ACTIVATION_REGIONS['IND'])
        url = region_config['major_login_url']

        headers = {
            'X-Unity-Version': '2018.4.11f1',
            'ReleaseVersion':  'OB54',
            'Content-Type':    'application/x-www-form-urlencoded',
            'X-GA':            'v1 1',
            'User-Agent':      'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
            'Host':            'loginbp.ggpolarbear.com',
            'Connection':      'Keep-Alive',
        }

        payload_template = bytes.fromhex(
            '1a13323032352d30372d33302031313a30323a3531220966726565206669726528013a07312e3131342e32422c416e64726f6964204f5320372e312e32202f204150492d323320284e32473438482f373030323530323234294a0848616e6468656c645207416e64726f69645a045749464960c00c68840772033332307a1f41524d7637205646507633204e454f4e20564d48207c2032343635207c203480019a1b8a010f416472656e6f2028544d292036343092010d4f70656e474c20455320332e319a012b476f6f676c657c31663361643662372d636562342d343934622d383730622d623164616364373230393131a2010c3139372e312e31322e313335aa0102656eb201203939366136323964626364623339363462653662363937386635643831346462ba010134c2010848616e6468656c64ca011073616d73756e6720534d2d473935354eea014066663930633037656239383135616633306134336234613966363031393531366530653463373033623434303932353136643064656661346365663531663261f00101ca0207416e64726f6964d2020457494649ca03203734323862323533646566633136343031386336303461316562626665626466e003daa907e803899b07f003bf0ff803ae088004999b078804daa9079004999b079804daa907c80403d204262f646174612f6170702f636f6d2e6474732e667265656669726574682d312f6c69622f61726de00401ea044832303837663631633139663537663261663465376665666630623234643964397c2f646174612f6170702f636f6d2e6474732e667265656669726574682d312f626173652e61706bf00403f804018a050233329a050a32303139313138363933a80503b205094f70656e474c455332b805ff7fc00504e005dac901ea0507616e64726f6964f2055c4b71734854394748625876574c6668437950416c52526873626d43676542557562555551317375746d525536634e30524f3751453141486e496474385963784d614c575437636d4851322b7374745279377830663935542b6456593d8806019006019a060134a2060134b2061e40001147550d0c074f530b4d5c584d57416657545a065f2a091d6a0d5033'
        )
        OLD_OPEN_ID      = b"996a629dbcdb3964be6b6978f5d814db"
        OLD_ACCESS_TOKEN = b"ff90c07eb9815af30a43b4a9f6019516e0e4c703b44092516d0defa4cef51f2a"
        payload = payload_template.replace(OLD_OPEN_ID, open_id.encode())
        payload = payload.replace(OLD_ACCESS_TOKEN, access_token.encode())
        encrypted_payload = self.encrypt_api(payload.hex())
        if not encrypted_payload:
            return None
        final_payload = bytes.fromhex(encrypted_payload)

        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                if self.stop_execution:
                    return None
                self.smart_rate_limit_bypass()
                timeout = 12 if self.turbo_mode else 18
                response = self.session.post(
                    url, headers=headers, data=final_payload,
                    verify=False, timeout=timeout
                )
                if response.status_code == 200 and len(response.content) > 0:
                    return response.content
                elif response.status_code == 429:
                    self.advanced_retry_strategy(attempt, max_attempts)
                    continue
            except Exception:
                pass
            if attempt < max_attempts - 1:
                self.advanced_retry_strategy(attempt, max_attempts)
        return None

    def GET_PAYLOAD_BY_DATA(self, JWT_TOKEN, NEW_ACCESS_TOKEN, region='IND'):
        try:
            token_payload_base64 = JWT_TOKEN.split('.')[1]
            token_payload_base64 += '=' * ((4 - len(token_payload_base64) % 4) % 4)
            decoded_payload = json.loads(base64.urlsafe_b64decode(token_payload_base64).decode('utf-8'))
            NEW_EXTERNAL_ID = decoded_payload['external_id']
            SIGNATURE_MD5   = decoded_payload['signature_md5']
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            payload = bytes.fromhex(
                "1a13323032352d30372d33302031313a30323a3531220966726565206669726528013a07312e3131342e32422c416e64726f6964204f5320372e312e32202f204150492d323320284e32473438482f373030323530323234294a0848616e6468656c645207416e64726f69645a045749464960c00c68840772033332307a1f41524d7637205646507633204e454f4e20564d48207c2032343635207c203480019a1b8a010f416472656e6f2028544d292036343092010d4f70656e474c20455320332e319a012b476f6f676c657c31663361643662372d636562342d343934622d383730622d623164616364373230393131a2010c3139372e312e31322e313335aa0102656eb201203939366136323964626364623339363462653662363937386635643831346462ba010134c2010848616e6468656c64ca011073616d73756e6720534d2d473935354eea014066663930633037656239383135616633306134336234613966363031393531366530653463373033623434303932353136643064656661346365663531663261f00101ca0207416e64726f6964d2020457494649ca03203734323862323533646566633136343031386336303461316562626665626466e003daa907e803899b07f003bf0ff803ae088004999b078804daa9079004999b079804daa907c80403d204262f646174612f6170702f636f6d2e6474732e667265656669726574682d312f6c69622f61726de00401ea044832303837663631633139663537663261663465376665666630623234643964397c2f646174612f6170702f636f6d2e6474732e667265656669726574682d312f626173652e61706bf00403f804018a050233329a050a32303139313138363933a80503b205094f70656e474c455332b805ff7fc00504e005dac901ea0507616e64726f6964f2055c4b71734854394748625876574c6668437950416c52526873626d43676542557562555551317375746d525536634e30524f3751453141486e496474385963784d614c575437636d4851322b7374745279377830663935542b6456593d8806019006019a060134a2060134b2061e40001147550d0c074f530b4d5c584d57416657545a065f2a091d6a0d5033"
            )
            payload = payload.replace(b"2025-07-30 11:02:51", now.encode())
            payload = payload.replace(
                b"ff90c07eb9815af30a43b4a9f6019516e0e4c703b44092516d0defa4cef51f2a",
                NEW_ACCESS_TOKEN.encode("UTF-8")
            )
            payload = payload.replace(b"996a629dbcdb3964be6b6978f5d814db", NEW_EXTERNAL_ID.encode("UTF-8"))
            payload = payload.replace(b"7428b253defc164018c604a1ebbfebdf", SIGNATURE_MD5.encode("UTF-8"))
            PAYLOAD = self.encrypt_api(payload.hex())
            if PAYLOAD:
                return bytes.fromhex(PAYLOAD)
            return None
        except Exception as e:
            debug_print(f"GET_PAYLOAD_BY_DATA error: {e}")
            return None

    def GET_LOGIN_DATA(self, JWT_TOKEN, PAYLOAD, region='IND'):
        if self.stop_execution:
            return False
        region_config = Config.ACTIVATION_REGIONS.get(region, Config.ACTIVATION_REGIONS['IND'])
        url         = region_config['get_login_data_url']
        client_host = region_config['client_host']
        headers = {
            'Expect':        '100-continue',
            'Authorization': f'Bearer {JWT_TOKEN}',
            'X-Unity-Version': '2018.4.11f1',
            'X-GA':          'v1 1',
            'ReleaseVersion': 'OB54',
            'Content-Type':  'application/x-www-form-urlencoded',
            'User-Agent':    'Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)',
            'Host':          client_host,
            'Connection':    'close',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        max_attempts = 2
        for attempt in range(max_attempts):
            try:
                if self.stop_execution:
                    return False
                self.smart_rate_limit_bypass()
                timeout = 8 if self.turbo_mode else 12
                response = self.session.post(
                    url, headers=headers, data=PAYLOAD,
                    verify=False, timeout=timeout
                )
                if response.status_code == 200:
                    return True
                elif response.status_code == 401:
                    with self.stats_lock:
                        self.unauthorized_count += 1
                        if self.unauthorized_count >= self.max_unauthorized_before_stop:
                            self.stop_execution = True
                    return False
                elif response.status_code == 404:
                    return False
            except Exception:
                pass
            if attempt < max_attempts - 1:
                self.advanced_retry_strategy(attempt, max_attempts)
        return False

    def activate_account(self, account_data):
        uid      = account_data['uid']
        password = account_data['password']
        region   = account_data.get('region', 'IND')
        if region not in Config.ACTIVATION_REGIONS:
            region = 'IND'

        access_token, open_id = self.guest_token(uid, password, region)
        if not access_token or not open_id:
            return False

        major_login_response = self.major_login(access_token, open_id, region)
        if not major_login_response:
            return False

        jwt_token, key, iv = self.parse_my_message(major_login_response)
        if not jwt_token:
            return False

        payload = self.GET_PAYLOAD_BY_DATA(jwt_token, access_token, region)
        if not payload:
            return False

        return self.GET_LOGIN_DATA(jwt_token, payload, region)

auto_activator = AutoActivator(max_workers=8, turbo_mode=True)

# =============================================================================
# 👤 ACCOUNT CREATION  (OB54 FIXED — new endpoints + JSON body)
# =============================================================================

def create_acc(region, session, is_ghost=False):
    if EXIT_FLAG:
        return None

    max_attempts = Config.MAX_RETRIES
    debug_log(f"create_acc START | Region: {region} | Max attempts: {max_attempts}", "INFO")

    for attempt in range(max_attempts):
        try:
            debug_log(f"Attempt {attempt+1} START", "INFO")
            
            password = generate_custom_password()
            debug_log(f"Password generated: {password[:15]}...", "INFO")

            # STEP 1: Register
            payload_register = json.dumps(
                {"app_id": 100067, "client_type": 2, "password": password, "source": 2},
                separators=(',', ':')
            )
            
            signature = hmac.new(Config.API_KEY, payload_register.encode(), hashlib.sha256).hexdigest()
            
            headers_reg = {
                "User-Agent": FingerprintSpoofer.random_ua(),
                "Authorization": f"Signature {signature}",
                "Content-Type": "application/json; charset=utf-8",
                "Accept": "application/json",
                "Connection": "Keep-Alive",
                "Host": "100067.connect.garena.com",
            }
            
            debug_log(f"SENDING REGISTER REQUEST...", "REQUEST")
            
            try:
                resp_reg = session.post(
                    Config.REGISTER_URL,
                    headers=headers_reg,
                    data=payload_register,
                    timeout=30,
                    verify=False
                )
                debug_log(f"REGISTER RESPONSE: status={resp_reg.status_code}", "RESPONSE")
            except Exception as req_err:
                debug_log(f"REGISTER EXCEPTION: {str(req_err)}", "ERROR")
                continue
            
            if resp_reg.status_code == 200:
                try:
                    reg_json = resp_reg.json()
                    if reg_json.get("code") == 0:
                        uid = str(reg_json['data']['uid'])
                        debug_log(f"✅ UID: {uid}", "SUCCESS")
                        
                        with Config.LOCK:
                            Config.ATTEMPTS += 1
                            global SUCCESS_COUNTER
                            SUCCESS_COUNTER += 1
                        
                        # حفظ حساب ناجح
                        account = {
                            "uid": uid,
                            "password": password,
                            "name": generate_random_name(),
                            "region": "GHOST" if is_ghost else region,
                            "status": "success",
                            "account_id": uid,
                            "jwt_token": "",
                            "api_label": "OB54",
                            "tcp_activated": False,
                            "thread_id": 0
                        }
                        save_normal_account(account, region, is_ghost)
                        
                        current_count = SUCCESS_COUNTER
                        print(f"\n✅ ACCOUNT #{current_count}: UID={uid} | Pass={password[:20]}...")
                        return account
                    else:
                        debug_log(f"API Error: {reg_json}", "ERROR")
                except Exception as parse_err:
                    debug_log(f"Parse error: {str(parse_err)}", "ERROR")
            else:
                debug_log(f"HTTP {resp_reg.status_code}", "ERROR")
                
        except Exception as e:
            debug_log(f"EXCEPTION: {str(e)}", "ERROR")
            traceback.print_exc()
        
        time.sleep(2)

    return None
    
def _major_register_and_login_sync(uid, password, access_token, open_id, name,
                                    region, api_config, session, is_ghost):
    try:
        keystream = [0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,
                     0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30]
        encoded_open_id = ""
        for i, ch in enumerate(open_id):
            encoded_open_id += chr(ord(ch) ^ keystream[i % len(keystream)])
        field14 = encoded_open_id.encode('latin1')

        lang_code = "pt" if is_ghost else Config.REGION_LANG.get(region.upper(), "en")
        payload_fields = {
            1: name, 2: access_token, 3: open_id,
            5: 102000007, 6: 4, 7: 1, 13: 1,
            14: field14, 15: lang_code, 16: 1, 17: 1
        }
        proto_bytes = run_async(CrEaTe_ProTo(payload_fields))
        encrypted_payload = E_AEs(bytes(proto_bytes).hex())

        host = "loginbp.ggpolarbear.com"
        register_url = Config.MAJOR_REGISTER_URL
        login_url    = Config.MAJOR_LOGIN_URL

        headers_reg = {
            "Accept-Encoding": "gzip", "Authorization": "Bearer",
            "Connection": "Keep-Alive", "Content-Type": "application/x-www-form-urlencoded",
            "Expect": "100-continue", "Host": host,
            "ReleaseVersion": "OB54",
            "User-Agent": FingerprintSpoofer.random_ua(),
            "X-GA": "v1 1", "X-Unity-Version": "1.126.1",
        }

        resp_reg = session.post(register_url, headers=headers_reg,
                                data=encrypted_payload, verify=False, timeout=15)
        if resp_reg.status_code != 200:
            return None

        login_result = _perform_major_login_sync(uid, password, access_token, open_id,
                                                  region, session, is_ghost)
        account_id = login_result.get("account_id", "N/A")
        jwt_token  = login_result.get("jwt_token", "")
        ml_key     = login_result.get("ml_key")
        ml_iv      = login_result.get("ml_iv")
        ml_ts      = login_result.get("ml_timestamp")
        ml_url     = login_result.get("ml_url")

        tcp_ok = False

        return {
            "uid": uid, "password": password, "name": name,
            "region": "GHOST" if is_ghost else region,
            "status": "success", "account_id": account_id,
            "jwt_token": jwt_token, "api_label": api_config["label"],
            "tcp_activated": tcp_ok,
        }
    except Exception as e:
        debug_print(f"MajorRegister error: {str(e)[:50]}")
        return None

def _encrypt_major_login_proto(open_id, access_token):
    if not NEW_PROTO_AVAILABLE or not AES_AVAILABLE:
        return None
    try:
        ml = MajoRLoGinrEq_pb2.MajorLogin()
        ml.event_time            = str(datetime.now())[:-7]
        ml.game_name             = "free fire"
        ml.platform_id           = 1
        ml.client_version        = "1.126.2"
        ml.system_software       = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
        ml.system_hardware       = "Handheld"
        ml.telecom_operator      = "Verizon"
        ml.network_type          = "WIFI"
        ml.screen_width          = 1920
        ml.screen_height         = 1080
        ml.screen_dpi            = "280"
        ml.processor_details     = "ARM64 FP ASIMD AES VMH | 2865 | 4"
        ml.memory                = 3003
        ml.gpu_renderer          = "Adreno (TM) 640"
        ml.gpu_version           = "OpenGL ES 3.1 v1.46"
        ml.unique_device_id      = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
        ml.client_ip             = "223.191.51.89"
        ml.language              = "en"
        ml.open_id               = open_id
        ml.open_id_type          = "4"
        ml.device_type           = "Handheld"
        ml.memory_available.version      = 55
        ml.memory_available.hidden_value = 81
        ml.access_token          = access_token
        ml.platform_sdk_id       = 1
        ml.network_operator_a    = "Verizon"
        ml.network_type_a        = "WIFI"
        ml.client_using_version  = "7428b253defc164018c604a1ebbfebdf"
        ml.external_storage_total        = 36235
        ml.external_storage_available    = 31335
        ml.internal_storage_total        = 2519
        ml.internal_storage_available    = 703
        ml.game_disk_storage_available   = 25010
        ml.game_disk_storage_total       = 26628
        ml.external_sdcard_avail_storage = 32992
        ml.external_sdcard_total_storage = 36235
        ml.login_by              = 3
        ml.library_path          = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
        ml.reg_avatar            = 1
        ml.library_token         = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
        ml.channel_type          = 3
        ml.cpu_type              = 2
        ml.cpu_architecture      = "64"
        ml.client_version_code   = "2019118695"
        ml.graphics_api          = "OpenGLES2"
        ml.supported_astc_bitset = 16383
        ml.login_open_id_type    = 4
        ml.analytics_detail      = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
        ml.loading_time          = 13564
        ml.release_channel       = "android"
        ml.extra_info            = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
        ml.android_engine_init_flag = 110009
        ml.if_push               = 1
        ml.is_vpn                = 1
        ml.origin_platform_type  = "4"
        ml.primary_platform_type = "4"
        serialized = ml.SerializeToString()
        key_b = bytes([89,103,38,116,99,37,68,69,117,104,54,37,90,99,94,56])
        iv_b  = bytes([54,111,121,90,68,114,50,50,69,51,121,99,104,106,77,37])
        cipher = AES.new(key_b, AES.MODE_CBC, iv_b)
        return cipher.encrypt(pad(serialized, AES.block_size))
    except Exception as e:
        debug_print(f"Proto MajorLogin build error: {e}")
        return None

def _perform_major_login_sync(uid, password, access_token, open_id, region, session, is_ghost=False):
    url = Config.MAJOR_LOGIN_URL
    headers = {
        "Accept-Encoding": "gzip", "Authorization": "Bearer",
        "Connection": "Keep-Alive", "Content-Type": "application/x-www-form-urlencoded",
        "Expect": "100-continue", "Host": "loginbp.ggpolarbear.com",
        "ReleaseVersion": "OB54",
        "User-Agent": FingerprintSpoofer.random_ua(),
        "X-GA": "v1 1", "X-Unity-Version": "2018.4.11f1",
    }

    final_payload = None
    if NEW_PROTO_AVAILABLE and AES_AVAILABLE:
        try:
            final_payload = _encrypt_major_login_proto(open_id, access_token)
            debug_print(f"MajorLogin (proto/new) for {uid}")
        except Exception as e:
            debug_print(f"Proto build failed, falling back: {e}")
            final_payload = None

    if final_payload is None:
        try:
            lang = "pt" if is_ghost else Config.REGION_LANG.get(region.upper(), "en")
            payload_parts = [
                b'\x1a\x132025-08-30 05:19:21\"\tfree fire(\x01:\x081.114.13B2Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)J\x08HandheldR\nATM MobilsZ\x04WIFI`\xb6\nh\xee\x05r\x03300z\x1fARMv7 VFPv3 NEON VMH | 2400 | 2\x80\x01\xc9\x0f\x8a\x01\x0fAdreno (TM) 640\x92\x01\rOpenGL ES 3.2\x9a\x01+Google|dfa4ab4b-9dc4-454e-8065-e70c733fa53f\xa2\x01\x0e105.235.139.91\xaa\x01\x02',
                lang.encode("ascii"),
                b'\xb2\x01 1d8ec0240ede109973f3321b9354b44d\xba\x01\x014\xc2\x01\x08Handheld\xca\x01\x10Asus ASUS_I005DA\xea\x01@afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390\xf0\x01\x01\xca\x02\nATM Mobils\xd2\x02\x04WIFI\xca\x03 7428b253defc164018c604a1ebbfebdf\xe0\x03\xa8\x81\x02\xe8\x03\xf6\xe5\x01\xf0\x03\xaf\x13\xf8\x03\x84\x07\x80\x04\xe7\xf0\x01\x88\x04\xa8\x81\x02\x90\x04\xe7\xf0\x01\x98\x04\xa8\x81\x02\xc8\x04\x01\xd2\x04=/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/lib/arm\xe0\x04\x01\xea\x04_2087f61c19f57f2af4e7feff0b24d9d9|/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/base.apk\xf0\x04\x03\xf8\x04\x01\x8a\x05\x0232\x9a\x05\n2019118693\xb2\x05\tOpenGLES2\xb8\x05\xff\x7f\xc0\x05\x04\xe0\x05\xf3F\xea\x05\x07android\xf2\x05pKqsHT5ZLWrYljNb5Vqh//yFRlaPHSO9NWSQsVvOmdhEEn7W+VHNUK+Q+fduA3ptNrGB0Ll0LRz3WW0jOwesLj6aiU7sZ40p8BfUE/FI/jzSTwRe2\xf8\x05\xfb\xe4\x06\x88\x06\x01\x90\x06\x01\x9a\x06\x014\xa2\x06\x014\xb2\x06"GQ@O\x00\x0e^\x00D\x06UA\x0ePM\r\x13hZ\x07T\x06\x0cm\\V\x0ejYV;\x0bU5'
            ]
            payload_bytes = b''.join(payload_parts)
            payload_bytes = payload_bytes.replace(
                b'afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390',
                access_token.encode()
            )
            payload_bytes = payload_bytes.replace(b'1d8ec0240ede109973f3321b9354b44d', open_id.encode())
            d = encrypt_api(payload_bytes.hex())
            if d:
                final_payload = bytes.fromhex(d)
            debug_print(f"MajorLogin (legacy) for {uid}")
        except Exception as e:
            debug_print(f"Legacy payload error: {e}")
            return {"account_id": "N/A", "jwt_token": ""}

    if final_payload is None:
        return {"account_id": "N/A", "jwt_token": ""}

    try:
        response = session.post(url, headers=headers, data=final_payload, verify=False, timeout=15)
        if response.status_code == 200 and len(response.content) > 10:
            if NEW_PROTO_AVAILABLE:
                try:
                    res = MajoRLoGinrEs_pb2.MajorLoginRes()
                    res.ParseFromString(response.content)
                    if res.token:
                        account_id = str(res.account_uid) if res.account_uid else decode_jwt_token(res.token)
                        key_bytes = bytes(res.key) if res.key else None
                        iv_bytes  = bytes(res.iv)  if res.iv  else None
                        return {
                            "account_id": account_id,
                            "jwt_token":  res.token,
                            "ml_key":     key_bytes,
                            "ml_iv":      iv_bytes,
                            "ml_timestamp": str(res.timestamp) if res.timestamp else None,
                            "ml_url":     res.url if res.url else None,
                        }
                except:
                    pass
            text = response.text
            jwt_start = text.find("eyJ")
            if jwt_start != -1:
                jwt_token = text[jwt_start:]
                second_dot = jwt_token.find(".", jwt_token.find(".") + 1)
                if second_dot != -1:
                    jwt_token = jwt_token[:second_dot + 44]
                    account_id = decode_jwt_token(jwt_token)
                    return {"account_id": account_id, "jwt_token": jwt_token,
                            "ml_key": None, "ml_iv": None,
                            "ml_timestamp": None, "ml_url": None}
    except Exception as e:
        debug_print(f"MajorLogin request error: {e}")

    return {"account_id": "N/A", "jwt_token": "",
            "ml_key": None, "ml_iv": None, "ml_timestamp": None, "ml_url": None}
            # =============================================================================
# 🔌 TCP ACCOUNT ACTIVATION (disabled – kept for reference but never called)
# =============================================================================

def _build_auth_token_hex(account_id, jwt_token, timestamp, key_bytes, iv_bytes):
    try:
        uid = int(account_id)
        uid_hex = hex(uid)[2:]
        uid_length = len(uid_hex)
        ts = int(timestamp)
        ts_hex = hex(ts)[2:]
        if len(ts_hex) == 1:
            ts_hex = "0" + ts_hex

        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
        encrypted_token = cipher.encrypt(pad(jwt_token.encode(), AES.block_size))
        encrypted_hex   = encrypted_token.hex()
        enc_len_hex     = hex(len(encrypted_hex) // 2)[2:]

        if uid_length == 9:
            headers_str = '0000000'
        elif uid_length == 8:
            headers_str = '00000000'
        elif uid_length == 10:
            headers_str = '000000'
        elif uid_length == 7:
            headers_str = '000000000'
        else:
            headers_str = '0000000'

        return f"0115{headers_str}{uid_hex}{ts_hex}00000{enc_len_hex}{encrypted_hex}"
    except Exception as e:
        debug_print(f"Auth token build error: {e}")
        return None

def _get_login_data_sync(base_url, open_id, access_token, jwt_token, session):
    try:
        if not NEW_PROTO_AVAILABLE:
            return None, None
        payload = _encrypt_major_login_proto(open_id, access_token)
        if payload is None:
            return None, None
        url = f"{base_url}/GetLoginData"
        host = base_url.replace("https://", "").replace("http://", "")
        headers = {
            "Accept-Encoding": "gzip",
            "Authorization": f"Bearer {jwt_token}",
            "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Expect": "100-continue",
            "Host": host,
            "ReleaseVersion": "OB54",
            "User-Agent": FingerprintSpoofer.random_ua(),
            "X-GA": "v1 1",
            "X-Unity-Version": "2018.4.11f1",
        }
        resp = session.post(url, headers=headers, data=payload, verify=False, timeout=15)
        if resp.status_code == 200 and resp.content:
            data = PorTs_pb2.GetLoginData()
            data.ParseFromString(resp.content)
            online_ip_port = data.Online_IP_Port if data.Online_IP_Port else None
            chat_ip_port   = data.AccountIP_Port if data.AccountIP_Port else None
            return online_ip_port, chat_ip_port
    except Exception as e:
        debug_print(f"GetLoginData error: {e}")
    return None, None

async def _tcp_connect_and_activate(ip, port, auth_hex, server_name, duration=0.8):
    try:
        reader, writer = await asyncio.open_connection(ip, int(port), ssl=False)
        debug_print(f"TCP connected to {server_name} {ip}:{port}")
        writer.write(bytes.fromhex(auth_hex))
        await writer.drain()
        debug_print(f"TCP auth sent to {server_name}")
        await asyncio.sleep(duration)
        writer.close()
        await writer.wait_closed()
        debug_print(f"TCP disconnected from {server_name}")
        return True
    except Exception as e:
        debug_print(f"TCP error {server_name} {ip}:{port} — {e}")
        return False

def _activate_via_tcp(account_id, jwt_token, timestamp, key_bytes, iv_bytes,
                      open_id, access_token, ml_url, session):
    debug_print("TCP activation disabled")
    return False

def _force_region_binding(region, jwt_token, session):
    debug_print("Region binding disabled")
    return False

def _select_veteran(region, jwt_token, session):
    debug_print("Veteran selection disabled")
    return False

# =============================================================================
# 🔥 AUTO ACTIVATION INTEGRATION (disabled)
# =============================================================================

ACTIVATED_COUNTER      = 0
FAILED_ACTIVATION_COUNTER = 0

def auto_activate_account(account_data):
    debug_print("Auto-activation disabled")
    return False

# =============================================================================
# 💾 SAVE FUNCTIONS
# =============================================================================

def save_activated_account(account_data):
    try:
        activated_name = getattr(Config, 'CURRENT_ACTIVATED_BASE', 'activated')
        filename = os.path.join(Config.ACTIVATED_FOLDER, f"{activated_name}.json")
        entry = {
            'uid': account_data['uid'], 'password': account_data['password'],
            'account_id': account_data.get('account_id','N/A'),
            'name': account_data['name'], 'region': account_data.get('region','UNKNOWN'),
            'activated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        with get_file_lock(filename):
            lst = safe_json_load(filename, [])
            lst.append(entry)
            safe_json_save(filename, lst)
    except: pass

def save_failed_activation(account_data):
    try:
        region = account_data.get('region', 'UNKNOWN')
        filename = os.path.join(Config.FAILED_ACTIVATION_FOLDER, f"failed-{region}.json")
        entry = {
            'uid': account_data['uid'], 'password': account_data['password'],
            'account_id': account_data.get('account_id','N/A'),
            'name': account_data['name'], 'region': region,
            'failed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        with get_file_lock(filename):
            lst = safe_json_load(filename, [])
            lst.append(entry)
            safe_json_save(filename, lst)
    except: pass

def save_jwt_token(account_data, jwt_token, region, is_ghost=False):
    try:
        filename = (os.path.join(Config.GHOST_FOLDER, "tokens-ghost.json") if is_ghost
                    else os.path.join(Config.TOKENS_FOLDER, f"tokens-{region}.json"))
        entry = {
            'uid': account_data["uid"], 'account_id': account_data.get("account_id","N/A"),
            'jwt_token': jwt_token, 'name': account_data["name"],
            'password': account_data["password"],
            'date_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'region': "YASIN" if is_ghost else region,
            'thread_id': account_data.get('thread_id','N/A')
        }
        with get_file_lock(filename):
            lst = safe_json_load(filename, [])
            existing = [t.get('account_id') for t in lst]
            if account_data.get("account_id","N/A") not in existing:
                lst.append(entry)
                safe_json_save(filename, lst)
                return True
        return False
    except: return False

def save_normal_account(account_data, region, is_ghost=False):
    try:
        if is_ghost:
            filename = os.path.join(Config.GHOST_ACCOUNTS_FOLDER, "ghost.json")
        else:
            json_base = getattr(Config, 'CURRENT_JSON_BASE', f'accounts-{region}')
            filename = os.path.join(Config.ACCOUNTS_FOLDER, f"{json_base}.json")
        entry = {
            'uid': account_data["uid"], 'password': account_data["password"],
            'account_id': account_data.get("account_id","N/A"), 'name': account_data["name"],
            'region': "YASIN" if is_ghost else region,
            'date_created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'thread_id': account_data.get('thread_id','N/A')
        }
        with get_file_lock(filename):
            lst = safe_json_load(filename, [])
            existing = [a.get('account_id') for a in lst]
            if account_data.get("account_id","N/A") not in existing:
                lst.append(entry)
                safe_json_save(filename, lst)
                return True
        return False
    except: return False

def save_rare_account(account_data, rarity_type, reason, rarity_score, is_ghost=False):
    if rarity_score < 10:
        debug_print(f"Rare score {rarity_score} < 10 — not saved to file")
        return False
    try:
        filename = (os.path.join(Config.GHOST_RARE_FOLDER, "rare-ghost.json") if is_ghost
                    else os.path.join(Config.RARE_ACCOUNTS_FOLDER, f"rare-{account_data.get('region','UNKNOWN')}.json"))
        entry = {
            'uid': account_data["uid"], 'password': account_data["password"],
            'account_id': account_data.get("account_id","N/A"), 'name': account_data["name"],
            'region': "YASIN" if is_ghost else account_data.get('region','UNKNOWN'),
            'rarity_type': rarity_type, 'rarity_score': rarity_score, 'reason': reason,
            'date_identified': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'jwt_token': account_data.get('jwt_token',''), 'thread_id': account_data.get('thread_id','N/A')
        }
        with get_file_lock(filename):
            lst = safe_json_load(filename, [])
            existing = [a.get('account_id') for a in lst]
            if account_data.get("account_id","N/A") not in existing:
                lst.append(entry)
                safe_json_save(filename, lst)
                return True
        return False
    except: return False

def save_couples_account(account1, account2, reason, is_ghost=False):
    try:
        region = account1.get('region','UNKNOWN')
        filename = (os.path.join(Config.GHOST_COUPLES_FOLDER, "couples-ghost.json") if is_ghost
                    else os.path.join(Config.COUPLES_ACCOUNTS_FOLDER, f"couples-{region}.json"))
        entry = {
            'couple_id': f"{account1.get('account_id','N/A')}_{account2.get('account_id','N/A')}",
            'account1': {'uid': account1["uid"], 'password': account1["password"],
                         'account_id': account1.get("account_id","N/A"), 'name': account1["name"],
                         'thread_id': account1.get('thread_id','N/A')},
            'account2': {'uid': account2["uid"], 'password': account2["password"],
                         'account_id': account2.get("account_id","N/A"), 'name': account2["name"],
                         'thread_id': account2.get('thread_id','N/A')},
            'reason': reason, 'region': "YASIN" if is_ghost else region,
            'date_matched': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        with get_file_lock(filename):
            lst = safe_json_load(filename, [])
            existing = [c.get('couple_id') for c in lst]
            if entry['couple_id'] not in existing:
                lst.append(entry)
                safe_json_save(filename, lst)
                return True
        return False
    except: return False

# =============================================================================
# 👥 WORKER FUNCTIONS
# =============================================================================

RARE_COUNTER    = 0
COUPLES_COUNTER = 0
SUCCESS_COUNTER = 0

def print_registration_status(count, total, name, uid, password, account_id, region, is_ghost=False, api_label="OB54", tcp_activated=False, jwt_token=""):
    C   = VISUAL.COLORS
    B   = C['bold']
    R   = C['reset']
    TOP = VISUAL.BOX['top']
    BOT = VISUAL.BOX['bottom']
    MID = VISUAL.BOX['mid']
    V   = VISUAL.BOX['v']
    
    W   = 55
    
    HDR_C = C['accent']
    LBL_C = C['c2']
    VAL_C = C['c3']
    ACC_C = C['c4']
    BDR_C = C['border']
    TS_C  = C['c5']
    JWT_C = C['dim']

    INNER = 45

    def box_line(text_colored, text_plain):
        pad = max(0, INNER - len(text_plain))
        print(f"{BDR_C}{V}{R} {text_colored}{' ' * pad} {BDR_C}{V}{R}")

    def row(icon, key, val, vc=VAL_C):
        label     = f"{icon} {key:<12}"
        label_len = len(label)
        val_s     = str(val)
        avail     = INNER - label_len

        if len(val_s) <= avail:
            plain = label + val_s
            colored = f"{LBL_C}{B}{label}{R}{vc}{val_s}{R}"
            box_line(colored, plain)
        else:
            chunk1 = val_s[:avail]
            plain1 = label + chunk1
            colored1 = f"{LBL_C}{B}{label}{R}{vc}{chunk1}{R}"
            box_line(colored1, plain1)
            indent = " " * (label_len)
            rest   = val_s[avail:]
            while rest:
                chunk = rest[:INNER - label_len]
                rest  = rest[INNER - label_len:]
                plain2   = indent + chunk
                colored2 = f"{vc}{indent}{chunk}{R}"
                box_line(colored2, plain2)

    print(f"{BDR_C}{TOP}{R}")
    hdr_txt  = "SUCCESSFUL ACCOUNT GENERATED!"
    print(f"{BDR_C}{V}{R} {HDR_C}{B}{hdr_txt.center(INNER+1)}{R} {BDR_C}{V}{R}")
    print(f"{BDR_C}{MID}{R}")

    row("🆔", "UID:",        str(uid))
    pwd_visible = 8
    pwd_display = str(password)[:pwd_visible] + ("*" * 10)
    row("🔑", "Password:",   pwd_display)
    row("👤", "Name:",       str(name))
    row("🎮", "Account ID:", str(account_id), ACC_C)

    ts_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    row("🕐", "Created At:", ts_now, TS_C)

    jwt_display = jwt_token[:8] + "********" if jwt_token else "N/A"
    row("🔒", "JWT Token:",  jwt_display, JWT_C)

    print(f"{BDR_C}{BOT}{R}")
    print()

def generate_single_account(region, total_accounts, thread_id, session, is_ghost=False):
    global SUCCESS_COUNTER, RARE_COUNTER, COUPLES_COUNTER, BIO_SET_COUNTER
    global ACTIVATED_COUNTER, FAILED_ACTIVATION_COUNTER

    if EXIT_FLAG:
        return None

    with Config.LOCK:
        if SUCCESS_COUNTER >= total_accounts:
            return None

    account_result = create_acc(region, session, is_ghost)
    if not account_result:
        return None

    account_id = str(account_result.get("account_id", "N/A"))
    jwt_token  = account_result.get("jwt_token", "")
    api_label  = account_result.get("api_label", "OB54")
    account_result['thread_id'] = thread_id

    if Config.AUTO_BIO:
        set_account_bio(account_result["uid"], account_result["password"],
                        Config.BIO_TEXT, region,
                        existing_jwt=account_result.get("jwt_token", ""))

    if is_ghost:
        save_normal_account(account_result, "GHOST", is_ghost=True)
        if jwt_token: save_jwt_token(account_result, jwt_token, "GHOST", is_ghost=True)
    else:
        save_normal_account(account_result, region)
        if jwt_token: save_jwt_token(account_result, jwt_token, region)

    try:
        is_rare, rarity_type, rarity_reason, rarity_score = check_account_rarity(account_result)
        if is_rare:
            with Config.LOCK: RARE_COUNTER += 1
            save_rare_account(account_result, rarity_type, rarity_reason, rarity_score, is_ghost)
    except Exception as e:
        debug_log(f"Rarity check skipped: {str(e)[:50]}", "WARNING")

    is_couple, couple_reason, partner_data = check_account_couples(account_result, thread_id)
    if is_couple and partner_data:
        with Config.LOCK: COUPLES_COUNTER += 1
        save_couples_account(account_result, partner_data, couple_reason, is_ghost)

    return {"account": account_result}

def worker(region, total_accounts, thread_id, is_ghost=False):
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=1, pool_maxsize=4, max_retries=0)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    FingerprintSpoofer.apply(session)

    debug_log(f"Thread {thread_id} started | Region: {region} | Ghost: {is_ghost}", "INFO")
    accounts_generated = 0
    
    while not EXIT_FLAG:
        with Config.LOCK:
            if SUCCESS_COUNTER >= total_accounts:
                break
        
        debug_log(f"Thread {thread_id} - Attempting account {SUCCESS_COUNTER+1}/{total_accounts}", "REQUEST")
        result = generate_single_account(region, total_accounts, thread_id, session, is_ghost)
        
        if result:
            accounts_generated += 1
            debug_log(f"Thread {thread_id} - SUCCESS! UID: {result['account'].get('uid', 'N/A')[:10]}...", "SUCCESS")
        else:
            debug_log(f"Thread {thread_id} - FAILED", "ERROR")
    
    debug_log(f"Thread {thread_id} finished | Generated: {accounts_generated}", "INFO")
    session_pool.put(session)
    # =============================================================================
# 📋 MENU FUNCTIONS
# =============================================================================

def generate_accounts_flow():
    global SUCCESS_COUNTER, RARE_COUNTER, COUPLES_COUNTER
    global ACTIVATED_COUNTER, FAILED_ACTIVATION_COUNTER, BIO_SET_COUNTER

    VISUAL.show_header(Config.USER_LEVEL)
    C = VISUAL.COLORS

    print(VISUAL.create_panel("🔑 PASSWORD PREFIX", "Enter password prefix:"))
    while True:
        pass_prefix = input(f"\n{C['primary']}{C['bold']}🔐 Password Prefix: {C['reset']}").strip()
        if pass_prefix:
            Config.CUSTOM_PASS_PREFIX = pass_prefix
            break
        print_error("Prefix cannot be empty!")

    print(VISUAL.create_panel("📊 ACCOUNT COUNT", "Enter the number of accounts to generate:"))
    while True:
        try:
            count_input = input(f"\n{C['secondary']}{C['bold']}🔢 Count: {C['reset']}").strip()
            if count_input.isdigit():
                account_count = int(count_input)
                if account_count > 0:
                    break
                else:
                    print_error("Must be a positive number.")
            else:
                print_error("Enter a valid number.")
        except KeyboardInterrupt:
            safe_exit()

    print(VISUAL.create_panel("👤 CUSTOM ACCOUNT NAME", "Enter the in-game name for generated accounts:"))
    while True:
        custom_name = input(f"\n{C['primary']}{C['bold']}✏️  Account Name: {C['reset']}").strip()
        if custom_name:
            Config.CUSTOM_NAME_PREFIX = custom_name
            break
        print_error("Name cannot be empty!")

    print(VISUAL.create_panel("💾 JSON FILE NAME", "Enter JSON save file name (without .json):"))
    while True:
        json_base_name = input(f"\n{C['secondary']}{C['bold']}📄 JSON Name: {C['reset']}").strip()
        if json_base_name:
            break
        print_error("JSON name cannot be empty!")

    regions_to_show = [r for r in Config.REGION_LANG.keys() if r != "BR"]
    region_menu = ""
    for i, region in enumerate(regions_to_show, 1):
        region_menu += f"{i}) {region}  ({Config.REGION_LANG[region]})\n"
    region_menu += f"{len(regions_to_show)+1}) 👻 GHOST Mode\n00) ⬅️  BACK\n000) 🚪 EXIT"

    print(VISUAL.create_panel("🌍 SELECT REGION", region_menu))

    while True:
        try:
            choice = input(f"\n{C['primary']}{C['bold']}🎯 Choose: {C['reset']}").strip().upper()
            if choice == "00": return
            elif choice == "000":
                print(f"\n{C['primary']}{C['bold']}👋 Goodbye!{C['reset']}")
                sys.exit(0)
            elif choice.isdigit():
                n = int(choice)
                if 1 <= n <= len(regions_to_show):
                    selected_region = regions_to_show[n - 1]; is_ghost = False; break
                elif n == len(regions_to_show) + 1:
                    selected_region = "BR"; is_ghost = True; break
            elif choice in regions_to_show:
                selected_region = choice; is_ghost = False; break
            elif choice == "GHOST":
                selected_region = "BR"; is_ghost = True; break
            else:
                print_error("Invalid option")
        except KeyboardInterrupt:
            safe_exit()

    VISUAL.show_header(Config.USER_LEVEL)
    thread_count  = Config.MAX_THREADS

    region_suffix = selected_region.lower()
    Config.CURRENT_JSON_BASE = f"{json_base_name}-{region_suffix}"
    Config.CURRENT_ACTIVATED_BASE = f"{json_base_name}-{region_suffix}-activated"

    user_level_display = f"{'👑' if Config.USER_LEVEL=='OWNER' else '⚡' if Config.USER_LEVEL=='ADMIN' else '👤'} {Config.USER_LEVEL}"
    custom_settings = (f"\n📝 Name Prefix: {Config.CUSTOM_NAME_PREFIX}\n🔑 Pass Prefix: {Config.CUSTOM_PASS_PREFIX}\n💎 Rarity Threshold: {Config.CUSTOM_RARITY_THRESHOLD}"
                       if Config.USER_LEVEL in ["ADMIN","OWNER"] else "")

    config_text = f"""🎯 Target    : {account_count}
⚡ Threads   : {thread_count}
🔌 APIs      : {API_COUNT}
🛡️ Protection: ACTIVE (Anti-Detect + IP Rotate + Spoof)
📝 Auto Bio  : {'ON' if Config.AUTO_BIO else 'OFF'}
🔥 Auto-Act  : {'OFF' if not Config.AUTO_ACT else 'ON (disabled)'}
🌍 Region    : {'GHOST' if is_ghost else selected_region}
👤 Level     : {user_level_display}
🔄 Retries   : {Config.MAX_RETRIES}
🆕 Version   : OB54 — NEW API ENDPOINTS
👤 Acc Name  : {Config.CUSTOM_NAME_PREFIX}
💾 JSON File : {Config.CURRENT_JSON_BASE}.json
🔥 Activated : {Config.CURRENT_ACTIVATED_BASE}.json{custom_settings}"""

    print(VISUAL.create_panel("🚀 GENERATION CONFIG", config_text))
    print(f"\n{C['warning']}⏳ Starting with protection...{C['reset']}")
    time.sleep(0.5)

    SUCCESS_COUNTER = RARE_COUNTER = COUPLES_COUNTER = 0
    ACTIVATED_COUNTER = FAILED_ACTIVATION_COUNTER = BIO_SET_COUNTER = 0
    start_time = time.time()
    threads = []

    global GENERATION_SILENT
    GENERATION_SILENT = True
    print(f"\n{C['primary']}{C['bold']}🚀 Launching {thread_count} threads with protection...{C['reset']}\n")
    for i in range(thread_count):
        t = threading.Thread(target=worker, args=(selected_region, account_count, i+1, is_ghost))
        t.daemon = True
        t.start()
        threads.append(t)

    try:
        while any(t.is_alive() for t in threads):
            time.sleep(1)
            with Config.LOCK:
                if SUCCESS_COUNTER >= account_count:
                    break
    except KeyboardInterrupt:
        EXIT_FLAG = True

    for t in threads:
        t.join(timeout=3)

    GENERATION_SILENT = False
    elapsed = time.time() - start_time
    final_stats = f"""📊 Generated : {SUCCESS_COUNTER}/{account_count}
💎 Rare      : {RARE_COUNTER}
💑 Couples   : {COUPLES_COUNTER}
🔥 Activated : {ACTIVATED_COUNTER} (disabled)
❌ Failed    : {FAILED_ACTIVATION_COUNTER}
📝 Bio Set   : {BIO_SET_COUNTER} (disabled)
⏱️  Time     : {elapsed:.2f}s
⚡ Speed     : {SUCCESS_COUNTER/elapsed:.2f} acc/s
🔌 Attempts  : {Config.ATTEMPTS}
🛡️ IP Changes: {bulk_protection.generation_count // bulk_protection.ip_change_interval}
👤 Level     : {Config.USER_LEVEL}"""
    print(VISUAL.create_panel("🎉 GENERATION COMPLETE!", final_stats))
    input(f"\n{C['warning']}{C['bold']}⏎ Press Enter to continue...{C['reset']}")

def admin_panel():
    if Config.USER_LEVEL == "USER":
        print_error("Access Denied! Admin/Owner only.")
        time.sleep(2); return
    while True:
        VISUAL.show_header(Config.USER_LEVEL)
        credits = CreditEditor.load_credits()
        C = VISUAL.COLORS
        admin_menu = f"""🔧 ULTIMATE ADMIN CONTROL PANEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Level   : {Config.USER_LEVEL}
🔌 APIs    : {API_COUNT}
🛡️ Protect : ACTIVE

📝 CREDIT MANAGEMENT:
1) ✏️  Edit Primary Credit     (now: {credits['primary_credit']})
2) 📱 Edit Telegram Handles   (now: {credits['telegram1']}, {credits['telegram2']})
3) 🐙 Edit GitHub Link        (now: {credits['github']})
4) 📝 Edit Banner Text        (now: {credits['banner_text'][:25]}...)
5) 📝 Edit Bio Text           (now: {credits['bio_text'][:25]}...)
6) 💾 Save Credit Changes
7) 🔄 Restore Default Credits

⚙️ GENERATION SETTINGS:
8)  🎯 Name Prefix      (now: {Config.CUSTOM_NAME_PREFIX})
9)  🔑 Pass Prefix      (now: {Config.CUSTOM_PASS_PREFIX})
10) 💎 Rarity Threshold (now: {Config.CUSTOM_RARITY_THRESHOLD})
11) 🎯 Custom Target    (now: {Config.CUSTOM_TARGET})
12) ⚡ Max Threads      (now: {Config.MAX_THREADS})
13) 🔄 Max Retries      (now: {Config.MAX_RETRIES})

🛡️ PROTECTION SETTINGS:
14) 🔄 IP Change Interval (now: {bulk_protection.ip_change_interval})
15) 🛡️ Toggle Anti-Detect

📊 SYSTEM CONTROLS:
16) 📈 API Statistics
17) 🗑️  Clear All Data
18) 💾 Backup System
19) ⬅️  Back"""
        if Config.USER_LEVEL == "OWNER":
            admin_menu += "\n\n👑 OWNER EXCLUSIVE:\n20) ⚡ Force Generation Mode\n21) 🚀 Bypass Rate Limits\n22) 🔄 Custom API Priority"
        print(VISUAL.create_panel("🔧 ADMIN CONTROL", admin_menu, color='admin'))
        choice = input(f"\n{C['admin']}{C['bold']}⚡ Option: {C['reset']}").strip()

        if choice == "1":
            nc = input(f"{C['info']}New primary credit: {C['reset']}")
            credits['primary_credit'] = nc; CreditEditor.save_credits(credits)
            print_success("Updated!"); time.sleep(1)
        elif choice == "2":
            t1 = input(f"{C['info']}Telegram 1: {C['reset']}")
            t2 = input(f"{C['info']}Telegram 2: {C['reset']}")
            credits['telegram1'] = t1; credits['telegram2'] = t2
            CreditEditor.save_credits(credits); print_success("Updated!"); time.sleep(1)
        elif choice == "3":
            ng = input(f"{C['info']}GitHub URL: {C['reset']}")
            credits['github'] = ng; CreditEditor.save_credits(credits)
            print_success("Updated!"); time.sleep(1)
        elif choice == "4":
            nb = input(f"{C['info']}Banner text: {C['reset']}")
            credits['banner_text'] = nb; CreditEditor.save_credits(credits)
            print_success("Updated!"); time.sleep(1)
        elif choice == "5":
            nbio = input(f"{C['info']}Bio text: {C['reset']}")
            credits['bio_text'] = nbio; Config.BIO_TEXT = nbio
            CreditEditor.save_credits(credits); print_success("Updated!"); time.sleep(1)
        elif choice == "6":
            CreditEditor.save_credits(credits); print_success("Saved!"); time.sleep(1)
        elif choice == "7":
            d = {"primary_credit":"MASTER","github":"https://github.com/MASTER",
                 "telegram1":"@MASTER","telegram2":"@MASTER","display_name":"MASTER",
                 "banner_text":"⚡ POWERED BY MASTER⚡",
                 "footer_text":"👤 CREDIT: MASTER",
                 "bio_text":"[FF0000]🌈MASTER🌈"}
            CreditEditor.save_credits(d); Config.BIO_TEXT = d['bio_text']
            print_success("Defaults restored!"); time.sleep(1)
        elif choice == "8":
            Config.CUSTOM_NAME_PREFIX = input(f"{C['info']}Name prefix: {C['reset']}")
            print_success(f"Set: {Config.CUSTOM_NAME_PREFIX}"); time.sleep(1)
        elif choice == "9":
            Config.CUSTOM_PASS_PREFIX = input(f"{C['info']}Pass prefix: {C['reset']}")
            print_success(f"Set: {Config.CUSTOM_PASS_PREFIX}"); time.sleep(1)
        elif choice == "10":
            try:
                n = int(input(f"{C['info']}Rarity threshold (1-10): {C['reset']}"))
                if 1 <= n <= 10: Config.CUSTOM_RARITY_THRESHOLD = n; print_success(f"Set: {n}")
                else: print_error("Must be 1–10")
            except: print_error("Invalid input")
            time.sleep(1)
        elif choice == "11":
            try: Config.CUSTOM_TARGET = int(input(f"{C['info']}Target: {C['reset']}")); print_success(f"Set: {Config.CUSTOM_TARGET}")
            except: print_error("Invalid")
            time.sleep(1)
        elif choice == "12":
            try:
                n = int(input(f"{C['info']}Threads (1-64): {C['reset']}"))
                if 1 <= n <= 64: Config.MAX_THREADS = n; print_success(f"Set: {n}")
                else: print_error("Must be 1–64")
            except: print_error("Invalid")
            time.sleep(1)
        elif choice == "13":
            try:
                n = int(input(f"{C['info']}Retries (1-20): {C['reset']}"))
                if 1 <= n <= 20: Config.MAX_RETRIES = n; print_success(f"Set: {n}")
                else: print_error("Must be 1–20")
            except: print_error("Invalid")
            time.sleep(1)
        elif choice == "14":
            try:
                n = int(input(f"{C['info']}IP Change Interval (10-500): {C['reset']}"))
                if 10 <= n <= 500: bulk_protection.ip_change_interval = n; print_success(f"Set: {n}")
                else: print_error("Must be 10–500")
            except: print_error("Invalid")
            time.sleep(1)
        elif choice == "15":
            print_success("Anti-Detect is always ACTIVE")
            time.sleep(1)
        elif choice == "16":
            sr = (SUCCESS_COUNTER / Config.ATTEMPTS * 100) if Config.ATTEMPTS > 0 else 0
            st = f"Total: {Config.ATTEMPTS} | OK: {SUCCESS_COUNTER} | Failed: {Config.ATTEMPTS-SUCCESS_COUNTER} | Rate: {sr:.1f}% | APIs: {API_COUNT}"
            print(VISUAL.create_panel("📊 API STATS", st))
            input(f"\n{C['warning']}⏎ Press Enter...{C['reset']}")
        elif choice == "17":
            if input(f"{C['error']}Type CONFIRM to clear ALL data: {C['reset']}") == "CONFIRM":
                shutil.rmtree(Config.BASE_FOLDER)
                Config.create_folders()
                print_success("Cleared!")
            time.sleep(2)
        elif choice == "18":
            bp = CreditEditor.backup_current_file()
            print_success(f"Backup: {bp}") if bp else print_error("Backup failed")
            time.sleep(2)
        elif choice == "19":
            break
        elif choice == "20" and Config.USER_LEVEL == "OWNER":
            Config.FORCE_GENERATION = not Config.FORCE_GENERATION
            print_success(f"Force Gen: {Config.FORCE_GENERATION}"); time.sleep(1)
        elif choice == "21" and Config.USER_LEVEL == "OWNER":
            Config.BYPASS_RATE_LIMIT = not Config.BYPASS_RATE_LIMIT
            print_success(f"Bypass RL: {Config.BYPASS_RATE_LIMIT}"); time.sleep(1)
        elif choice == "22" and Config.USER_LEVEL == "OWNER":
            Config.CUSTOM_API_PRIORITY = not Config.CUSTOM_API_PRIORITY
            print_success(f"API Priority: {Config.CUSTOM_API_PRIORITY}"); time.sleep(1)
        else:
            print_error("Invalid option or insufficient privileges"); time.sleep(1)

def view_saved_accounts():
    VISUAL.show_header(Config.USER_LEVEL)
    folders = [Config.ACCOUNTS_FOLDER, Config.ACTIVATED_FOLDER,
               Config.RARE_ACCOUNTS_FOLDER, Config.COUPLES_ACCOUNTS_FOLDER]
    total = 0; results = ""
    for folder in folders:
        if os.path.exists(folder):
            for file in [f for f in os.listdir(folder) if f.endswith('.json')]:
                filepath = os.path.join(folder, file)
                try:
                    data = safe_json_load(filepath, [])
                    results += f"📄 {os.path.basename(folder)}/{file}: {len(data)} accounts\n"
                    total += len(data)
                except: pass
    results += f"\n📊 TOTAL: {total} accounts"
    print(VISUAL.create_panel("📁 SAVED ACCOUNTS", results))
    input(f"\n{VISUAL.COLORS['warning']}{VISUAL.COLORS['bold']}⏎ Press Enter...{VISUAL.COLORS['reset']}")

def show_stats():
    VISUAL.show_header(Config.USER_LEVEL)
    sr = (SUCCESS_COUNTER / Config.ATTEMPTS * 100) if Config.ATTEMPTS > 0 else 0
    stats = f"""SESSION STATISTICS
━━━━━━━━━━━━━━━━━━━━━━
✅ Generated  : {SUCCESS_COUNTER}
💎 Rare       : {RARE_COUNTER}
💑 Couples    : {COUPLES_COUNTER}
🔥 Activated  : {ACTIVATED_COUNTER} (unable)
❌ Failed     : {FAILED_ACTIVATION_COUNTER}
📝 Bio        : {BIO_SET_COUNTER} (disabled)
🔌 Attempts   : {Config.ATTEMPTS}
🛡️ IP Changes : {bulk_protection.generation_count // bulk_protection.ip_change_interval}

PERFORMANCE
━━━━━━━━━━━━━━━━━━━━━━
🔌 Total APIs : {API_COUNT}
⚡ Success    : {sr:.1f}%
👤 Level      : {Config.USER_LEVEL}
🔄 Retries    : {Config.MAX_RETRIES}
⚡ Threads    : {Config.MAX_THREADS}
🛡️ Protection : ACTIVE"""
    if Config.USER_LEVEL in ["ADMIN","OWNER"]:
        stats += f"\n📝 Name Prefix: {Config.CUSTOM_NAME_PREFIX}\n🔑 Pass Prefix: {Config.CUSTOM_PASS_PREFIX}"
    print(VISUAL.create_panel("📈 STATISTICS", stats))
    input(f"\n{VISUAL.COLORS['warning']}{VISUAL.COLORS['bold']}⏎ Press Enter...{VISUAL.COLORS['reset']}")

def about():
    VISUAL.show_header(Config.USER_LEVEL)
    credits = CreditEditor.load_credits()
    about_text = f"""🔥 {credits['display_name']} ULTIMATE GENERATOR v12.0
💎 Created by : {credits['primary_credit']}
📱 Telegram   : {credits['telegram1']}, {credits['telegram2']}
🐙 GitHub     : {credits['github']}

✨ FEATURES:
• {API_COUNT} Working APIs (OB54 updated)
• New /api/v2/ JSON endpoints
• Protobuf-based MajorLogin
• ggpolarbear.com host (OB54)
• ULTIMATE ADMIN CONTROL PANEL
• 3 Access Levels USER / ADMIN / OWNER
• Auto Activation · Rare Finder · Couples
• Auto Bio Changer · Multi-threading
• Real-time statistics · Dark Gold UI
• 🛡️ Anti-Detection System
• 🔄 IP Rotation
• 🎭 Fingerprint Spoofing
• 🚦 Smart Rate Limiting

🔐 ACCESS LEVELS:
• USER  — Basic access
• ADMIN — Full control + credit editing
• OWNER — Ultimate + exclusive features

⚠️ DO NOT REMOVE CREDITS
🔒 Protected by MASTER"""
    print(VISUAL.create_panel("ℹ️  ABOUT", about_text))
    input(f"\n{VISUAL.COLORS['warning']}{VISUAL.COLORS['bold']}⏎ Press Enter...{VISUAL.COLORS['reset']}")

def main_menu():
    Config.create_folders()
    while True:
        VISUAL.show_header(Config.USER_LEVEL)
        C = VISUAL.COLORS
        menu = """1) 🚀 Generate Accounts
2) 📁 View Saved Accounts
3) 📊 Statistics
4) ℹ️  About"""
        if Config.USER_LEVEL in ["ADMIN","OWNER"]:
            menu += "\n5) 🔧 ULTIMATE ADMIN PANEL\n6) 🚪 Exit"
        else:
            menu += "\n5) 🚪 Exit"
        print(VISUAL.create_panel("📌 MAIN MENU", menu))
        choice = input(f"\n{C['primary']}{C['bold']}🎯 Choose: {C['reset']}").strip()
        if choice == "1":   generate_accounts_flow()
        elif choice == "2": view_saved_accounts()
        elif choice == "3": show_stats()
        elif choice == "4": about()
        elif choice == "5":
            if Config.USER_LEVEL in ["ADMIN","OWNER"]: admin_panel()
            else: print(f"\n{C['primary']}{C['bold']}👋 Goodbye!{C['reset']}"); sys.exit(0)
        elif choice == "6" and Config.USER_LEVEL in ["ADMIN","OWNER"]:
            print(f"\n{C['primary']}{C['bold']}👋 Goodbye!{C['reset']}"); sys.exit(0)
        else:
            print_error("Invalid option"); time.sleep(1)

# =============================================================================
# 🚀 MAIN EXECUTION
# =============================================================================
# ============================================
# ============================================
# ============================================
# 🤖 TELEGRAM BOT (Fully English)
# ============================================
import os
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8717362798:AAG0MmEuS4ey38QrG5G9jE6bm5rQ1zFgvCg")  # ⚠️ Replace with your bot token

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False

user_sessions = {}

class UserSession:
    def __init__(self):
        self.region = "BD"
        self.prefix = "MASTER"
        self.name = "MASTER"
        self.step = None

def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Start Generation", callback_data="start_gen")],
        [InlineKeyboardButton("🌍 Region", callback_data="region_menu"),
         InlineKeyboardButton("🔑 Prefix", callback_data="prefix_menu")],
        [InlineKeyboardButton("👤 Name", callback_data="name_menu"),
         InlineKeyboardButton("📊 Count", callback_data="count_menu")],
        [InlineKeyboardButton("⚙️ Quick Settings", callback_data="quick_settings")],
    ])

def region_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇧🇩 BD", callback_data="region_BD"),
         InlineKeyboardButton("🇮🇳 IND", callback_data="region_IND")],
        [InlineKeyboardButton("🇵🇰 PK", callback_data="region_PK"),
         InlineKeyboardButton("🇮🇩 ID", callback_data="region_ID")],
        [InlineKeyboardButton("🇹🇭 TH", callback_data="region_TH"),
         InlineKeyboardButton("🇻🇳 VN", callback_data="region_VN")],
        [InlineKeyboardButton("🇧🇷 BR", callback_data="region_BR"),
         InlineKeyboardButton("🇪🇬 ME", callback_data="region_ME")],
        [InlineKeyboardButton("👻 GHOST", callback_data="region_BR_GHOST")],
        [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_sessions[update.effective_user.id] = UserSession()
    await update.message.reply_text(
        "🎮 *Welcome to the Free Fire Account Generator Bot!*\n\n"
        "Use the buttons below to configure generation, then press *Start Generation*.\n"
        "You will be asked for the number of accounts.\n"
        "• Less than 50 accounts → sent as a message\n"
        "• 50 or more → sent as a file",
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )

# ============================================
# 📚 HELP COMMAND
# ============================================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📚 **How to use this bot**\n\n"
        "1️⃣ **Set your preferences** using the buttons:\n"
        "   - 🌍 **Region**: Choose your server (BD, IND, GHOST, etc.)\n"
        "   - 🔑 **Prefix**: Set a custom password prefix\n"
        "   - 👤 **Name**: Set the in‑game name for accounts\n\n"
        "2️⃣ **Start generation**:\n"
        "   - Press **🚀 Start Generation** and send the number of accounts you want\n"
        "   - Or simply type a number directly (e.g., *5*)\n\n"
        "3️⃣ **Receive results**:\n"
        "   - **Less than 50 accounts** ➜ sent as a message\n"
        "   - **50 or more accounts** ➜ sent as a JSON file\n\n"
        "❓ **Need help?** Use /start to return to the main menu.\n"
        "⚡ **Quick example**: Just type *10* to generate 10 accounts instantly.\n\n"
        "🔧 **Commands**:\n"
        "   /start – Open the main menu\n"
        "   /help  – Show this help message"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown", reply_markup=main_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    session = user_sessions.get(user_id, UserSession())
    data = query.data

    if data == "start_gen":
        await query.edit_message_text(
            "🔢 Send the number of accounts to generate:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]])
        )
        session.step = "waiting_count"
    elif data == "main_menu":
        session.step = None
        await query.edit_message_text("Main Menu:", reply_markup=main_keyboard())
    elif data == "region_menu":
        await query.edit_message_text("Select region:", reply_markup=region_keyboard())
    elif data.startswith("region_"):
        reg = data.replace("region_", "")
        if reg == "BR_GHOST":
            session.region = "BR"
            session.is_ghost = True
            await query.edit_message_text("✅ Region set to GHOST 👻", reply_markup=main_keyboard())
        else:
            session.region = reg
            session.is_ghost = False
            await query.edit_message_text(f"✅ Region: {reg}", reply_markup=main_keyboard())
    elif data == "prefix_menu":
        await query.edit_message_text(
            "Send the new password prefix:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]])
        )
        session.step = "waiting_prefix"
    elif data == "name_menu":
        await query.edit_message_text(
            "Send the new account name:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]])
        )
        session.step = "waiting_name"
    elif data == "count_menu":
        await query.edit_message_text(
            "Send the number of accounts:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]])
        )
        session.step = "waiting_count"
    elif data == "quick_settings":
        pass

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = user_sessions.get(user_id)
    if not session:
        session = UserSession()
        user_sessions[user_id] = session

    text = update.message.text.strip()
    step = session.step

    if step == "waiting_prefix":
        session.prefix = text
        session.step = None
        await update.message.reply_text(f"✅ Prefix set to: {text}", reply_markup=main_keyboard())
    elif step == "waiting_name":
        session.name = text
        session.step = None
        await update.message.reply_text(f"✅ Name set to: {text}", reply_markup=main_keyboard())
    elif step == "waiting_count":
        if not text.isdigit():
            await update.message.reply_text("❌ Please send a valid number!")
            return
        count = int(text)
        if count < 1:
            await update.message.reply_text("❌ Number must be at least 1.")
            return
        session.step = None
        await start_generation(update, context, session, count)
    else:
        if text.isdigit():
            count = int(text)
            if count > 0:
                await start_generation(update, context, session, count)
            else:
                await update.message.reply_text("❌ Number must be positive.")
        else:
            await update.message.reply_text(
                "Use the buttons or send a number to generate accounts directly.",
                reply_markup=main_keyboard()
            )

async def start_generation(update, context, session, count):
    msg = await update.message.reply_text(f"⏳ Generating {count} accounts...")
    Config.CUSTOM_PASS_PREFIX = session.prefix
    Config.CUSTOM_NAME_PREFIX = session.name
    region = session.region
    is_ghost = getattr(session, 'is_ghost', False)

    accounts = []
    for i in range(count):
        try:
            sess = requests.Session()
            FingerprintSpoofer.apply(sess)
            acc = create_acc(region, sess, is_ghost=is_ghost)
            if acc:
                accounts.append(acc)
        except Exception as e:
            debug_log(f"Bot gen error: {e}", "ERROR")

    await msg.delete()

    if not accounts:
        await update.message.reply_text("❌ Generation failed. Please try again.")
        return

    if len(accounts) >= 50:
        filename = f"accounts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w") as f:
            json.dump(accounts, f, indent=2)
        with open(filename, "rb") as f:
            await update.message.reply_document(
                document=f,
                caption=f"✅ {len(accounts)} accounts generated"
            )
        os.remove(filename)
    else:
        result = f"✅ *{len(accounts)} accounts generated*\n\n"
        for i, acc in enumerate(accounts[:30], 1):
            result += f"{i}. `{acc['uid']}` | `{acc['password']}`\n"
        if len(accounts) > 30:
            result += f"\n... and {len(accounts)-30} more"
        await update.message.reply_text(result, parse_mode="Markdown")

def run_telegram_bot():
    if not TELEGRAM_AVAILABLE:
        print("❌ python-telegram-bot not installed. Run: pip install python-telegram-bot")
        return
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))  # ✅ تمت إضافة أمر المساعدة
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    print("🤖 Bot is running...")
    app.run_polling()
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "bot":
        run_telegram_bot()
    else:
        try:
            main_menu()
        except KeyboardInterrupt:
            safe_exit()
        except Exception as e:
            print_error(f"Error: {e}")
            time.sleep(2)
            os.execv(sys.executable, [sys.executable] + sys.argv)
