# 🛠️ PyIoT Command Cheat Sheet

> รวมคำสั่งสำคัญที่ใช้บ่อยสำหรับการพัฒนา **PyIoT Command Center**  
> Environment หลัก: **Windows + CMD + VS Code + Git + GitHub Desktop**

---

## 📌 สารบัญ

- [Python Virtual Environment](#-python-virtual-environment)
- [Python Packages และ pip](#-python-packages-และ-pip)
- [คำสั่งเกี่ยวกับ Folder และ File](#-คำสั่งเกี่ยวกับ-folder-และ-file)
- [คำสั่งเกี่ยวกับ CMD](#-คำสั่งเกี่ยวกับ-cmd)
- [Git for Windows](#-git-for-windows)
- [Git Repository](#-git-repository)
- [Workflow ที่ใช้บ่อย](#-workflow-ที่ใช้บ่อย)
- [Quick Reference](#-quick-reference)

---

# 🐍 Python Virtual Environment

## ▶️ เปิดใช้งาน Virtual Environment

```cmd
.venv\Scripts\activate
```

ใช้สำหรับเปิดใช้งาน Python Virtual Environment ของ Project

เมื่อ Activate สำเร็จ CMD จะแสดงชื่อ Environment ด้านหน้า เช่น

```text
(.venv) C:\Projects\PyIoT-Command-Center>
```

หลังจาก Activate แล้ว คำสั่ง `python` จะอ้างอิง Python ภายใน `.venv` เป็นหลัก

ตรวจสอบได้ด้วย:

```cmd
where python
```

โดยตำแหน่งแรกควรเป็นประมาณนี้:

```text
C:\...\PyIoT-Command-Center\.venv\Scripts\python.exe
```

> 💡 แนะนำให้ Activate `.venv` ก่อนติดตั้ง Package หรือ Run Project ทุกครั้ง

---

## ⏹️ ปิด Virtual Environment

```cmd
deactivate
```

ใช้สำหรับออกจาก Virtual Environment ปัจจุบัน

หลังจากรันแล้ว `( .venv )` ที่อยู่หน้าบรรทัด CMD จะหายไป

---

# 📦 Python Packages และ pip

## 🔍 ดู Package ที่ติดตั้งทั้งหมด

```cmd
python -m pip list
```

ใช้แสดง Python Package ทั้งหมดที่ติดตั้งอยู่ใน Environment ปัจจุบัน

ตัวอย่าง:

```text
Package     Version
----------- -------
pip         26.x
setuptools  xx.x
```

เมื่อเปิด `.venv` แล้ว แนะนำให้ใช้:

```cmd
python -m pip list
```

แทน:

```cmd
py -m pip list
```

เพราะ `python` หลัง Activate `.venv` จะชี้ตรงไปยัง Python ของ Project

---

## 🧩 `-m` คืออะไร?

`-m` ย่อมาจาก **module**

ตัวอย่าง:

```cmd
python -m pip list
```

หมายถึง:

> ให้ Python ตัวปัจจุบันเรียก Module ที่ชื่อ `pip` และส่งคำสั่ง `list` ให้ Module นั้น

ข้อดีคือช่วยให้มั่นใจว่า `pip` ที่ใช้อยู่เป็นของ Python Environment เดียวกับที่เรากำลังใช้งาน

ดังนั้นมักแนะนำให้ใช้:

```cmd
python -m pip install ...
```

แทน:

```cmd
pip install ...
```

โดยเฉพาะในเครื่องที่มี Python หลาย Version

---

## 🐍 `python` กับ `py` ต่างกันอย่างไร?

### `python`

```cmd
python
```

เรียก Python executable ตาม `PATH` ปัจจุบัน

เมื่อ Activate `.venv` แล้ว ปกติจะชี้ไปที่:

```text
.venv\Scripts\python.exe
```

### `py`

```cmd
py
```

คือ **Python Launcher for Windows**

สามารถใช้เลือก Version ของ Python ได้ เช่น:

```cmd
py -3
```

หรือ:

```cmd
py -3.12
```

`py` ไม่จำเป็นต้องใช้ `-m` เสมอ เช่น:

```cmd
py script.py
```

ก็สามารถ Run Python File ได้

> ✅ สำหรับ Project นี้ เมื่อ Activate `.venv` แล้ว ให้ใช้ `python` เป็นหลัก

---

## ⬆️ Update pip

```cmd
python -m pip install --upgrade pip
```

ใช้สำหรับ Update `pip` ใน Python Environment ปัจจุบัน

แนะนำให้เปิด `.venv` ก่อน:

```cmd
.venv\Scripts\activate
python -m pip install --upgrade pip
```

---

## 📥 ติดตั้ง Package

```cmd
python -m pip install <package-name>
```

ตัวอย่าง:

```cmd
python -m pip install fastapi
```

---

## 📄 ติดตั้ง Package จาก `requirements.txt`

```cmd
python -m pip install -r requirements.txt
```

ใช้ติดตั้ง Dependency ทั้งหมดที่ระบุไว้ในไฟล์ `requirements.txt`

---

# 📁 คำสั่งเกี่ยวกับ Folder และ File

## 📂 สร้าง Folder

```cmd
mkdir Folder_A
```

ตัวอย่าง:

```cmd
mkdir backend
```

จะได้:

```text
Project/
└── backend/
```

---

## 📂 สร้าง Folder ซ้อนกัน

```cmd
mkdir Folder_A\Folder_B
```

ตัวอย่าง:

```cmd
mkdir frontend\css
```

จะได้:

```text
frontend/
└── css/
```

---

## 📄 สร้าง File เปล่า

```cmd
type nul > backend\__init__.py
```

คำสั่งนี้ประกอบด้วย:

```text
type nul
```

`nul` เป็นอุปกรณ์พิเศษของ Windows ที่ไม่มีข้อมูลจริงให้อ่าน

ส่วน:

```text
>
```

คือ **Output Redirection**

หมายถึง:

> ให้นำ Output ไปเขียนลง File แทนการแสดงบนหน้าจอ CMD

ดังนั้น:

```cmd
type nul > backend\__init__.py
```

จึงสามารถใช้สร้าง File เปล่าได้

ผลลัพธ์:

```text
backend/
└── __init__.py
```

> ⚠️ ระวัง: ถ้า File มีอยู่แล้ว คำสั่ง `>` อาจทำให้เนื้อหาเดิมใน File ถูกเขียนทับ

---

# 🖥️ คำสั่งเกี่ยวกับ CMD

## ▶️ Run Python File

```cmd
python simulator\main.py
```

หมายถึง:

> ใช้ Python ปัจจุบัน Run File `main.py` ที่อยู่ใน Folder `simulator`

ตัวอย่างโครงสร้าง:

```text
PyIoT-Command-Center/
└── simulator/
    └── main.py
```

---

## 🧹 ล้างหน้าจอ CMD

```cmd
cls
```

ใช้ล้างข้อความบนหน้าจอ CMD

ไม่มีผลต่อ File หรือ Program ที่อยู่ใน Project

---

## 👀 ดู File และ Folder ใน Directory ปัจจุบัน

```cmd
dir
```

ตัวอย่างผลลัพธ์:

```text
backend
frontend
simulator
tests
README.md
requirements.txt
```

---

## 👀 ดู File รวม Hidden File / Folder

```cmd
dir /a
```

มีประโยชน์สำหรับดู Folder ที่ซ่อนอยู่ เช่น:

```text
.git
```

---

## 📍 ดู Directory ปัจจุบัน

```cmd
cd
```

ถ้าใช้ `cd` โดยไม่ตามด้วย Path CMD จะแสดง Directory ปัจจุบัน

ตัวอย่าง:

```text
%USERPROFILE%\Desktop\Coding\PyIoT-Command-Center
```

---

## 🚶 เข้า Folder

```cmd
cd FolderName
```

ตัวอย่าง:

```cmd
cd simulator
```

---

## ⬆️ กลับขึ้นไป 1 Directory

```cmd
cd ..
```

ตัวอย่าง:

```text
C:\Project\simulator>
```

รัน:

```cmd
cd ..
```

จะกลับไปเป็น:

```text
C:\Project>
```

---

## 🔄 เปลี่ยน Drive และ Directory พร้อมกัน

```cmd
cd /d D:\Projects\PyIoT-Command-Center
```

`/d` ช่วยให้ CMD สามารถเปลี่ยน Drive เช่น `C:` → `D:` พร้อมกับเปลี่ยน Directory ได้ในคำสั่งเดียว

---

## 🌳 ดูโครงสร้าง Folder

```cmd
tree
```

แสดงโครงสร้าง Folder แบบต้นไม้

---

## 🌳 ดูโครงสร้าง Folder พร้อม File

```cmd
tree /f
```

ตัวอย่าง:

```text
PyIoT-Command-Center
│
├── backend
│   └── __init__.py
│
├── simulator
│   ├── __init__.py
│   └── main.py
│
└── README.md
```

> 💡 มีประโยชน์มากเวลาเช็ก Project Structure หรือส่งโครงสร้าง Project ให้ Codex ดู

---

## 💻 เปิด Project ปัจจุบันด้วย VS Code

```cmd
code .
```

เครื่องหมาย `.` หมายถึง Directory ปัจจุบัน

ตัวอย่าง:

```cmd
cd /d "%USERPROFILE%\Desktop\Coding\PyIoT-Command-Center"
code .
```

---

# 🐙 Git for Windows

## 📥 ติดตั้ง Git for Windows

```cmd
winget install --id Git.Git -e --source winget
```

ใช้ Windows Package Manager (`winget`) เพื่อติดตั้ง Git for Windows

หลังติดตั้งเสร็จ แนะนำให้:

1. ปิด CMD
2. เปิด CMD ใหม่
3. ตรวจสอบ Git อีกครั้ง

---

## 🔎 ดู Version ของ Git

```cmd
git --version
```

ใช้ตรวจสอบว่า Git ถูกติดตั้งและ CMD สามารถเรียกใช้งาน Git ได้หรือไม่

ตัวอย่าง:

```text
git version 2.x.x.windows.x
```

---

## 📍 ดูตำแหน่งของ Git

```cmd
where git
```

ตัวอย่าง:

```text
C:\Program Files\Git\cmd\git.exe
```

---

# 🌿 Git Repository

## 🏗️ เริ่มต้น Git Repository

```cmd
git init
```

ความหมาย:

> Initialize Git Repository ใน Folder ปัจจุบัน

เมื่อรันสำเร็จ Git จะสร้าง Folder ซ่อนชื่อ:

```text
.git/
```

ก่อน:

```text
PyIoT-Command-Center/
├── backend/
└── README.md
```

หลัง:

```text
PyIoT-Command-Center/
├── .git/
├── backend/
└── README.md
```

> ✅ คำที่เหมาะสมคือ “สร้าง/Initialize Git Repository” ไม่ใช่ “ติดตั้ง Git ใน Project”

---

## 🌿 กำหนด Branch หลักเป็น `main`

```cmd
git branch -M main
```

ใช้เปลี่ยนชื่อ Branch ปัจจุบันเป็น:

```text
main
```

`-M` หมายถึง Force Rename หากจำเป็น

---

## 📊 ดูสถานะ Git

```cmd
git status
```

ใช้ตรวจสอบ:

- Branch ปัจจุบัน
- File ใหม่
- File ที่ถูกแก้
- File ที่ถูกลบ
- File ที่ถูก Stage แล้ว

ตัวอย่าง:

```text
On branch main

Untracked files:
    README.md
    backend/
    simulator/
```

ความหมายคือ Git เห็น File เหล่านี้แล้ว แต่ยังไม่ได้เริ่ม Track

> 💡 แนะนำให้ใช้ `git status` ก่อน Commit ทุกครั้ง

---

## ➕ เพิ่ม File เข้า Staging Area

เพิ่มทุก File:

```cmd
git add .
```

หรือเพิ่มเฉพาะ File:

```cmd
git add README.md
```

Staging Area คือพื้นที่เตรียม File ก่อน Commit

---

## 💾 Commit

```cmd
git commit -m "chore: initialize project structure"
```

ใช้บันทึก Snapshot ของ Code ลง Git History

ตัวอย่าง Commit Message:

```text
feat: add virtual temperature sensor
fix: handle mqtt reconnect
refactor: separate device service
test: add simulator tests
docs: update architecture
```

---

## 📜 ดู Commit History

```cmd
git log
```

ถ้าต้องการแบบสั้น:

```cmd
git log --oneline
```

ตัวอย่าง:

```text
a1b2c3d chore: initialize project structure
```

---

## 🔎 ดูความแตกต่างของ File ที่แก้ไข

```cmd
git diff
```

ใช้ดูว่า Code ส่วนใดถูกแก้ไขจาก Version ล่าสุด

---

# 🔄 Workflow ที่ใช้บ่อย

## เริ่มทำงานกับ Project

```cmd
cd /d "%USERPROFILE%\Desktop\Coding\PyIoT-Command-Center"
```

เปิด Virtual Environment:

```cmd
.venv\Scripts\activate
```

เปิด VS Code:

```cmd
code .
```

ตรวจ Git:

```cmd
git status
```

Run Simulator:

```cmd
python simulator\main.py
```

---

## ตรวจ Environment

### Python

```cmd
where python
python --version
python -m pip list
```

### Git

```cmd
where git
git --version
git status
```

### Project Structure

```cmd
tree /f
```

---

# ⚡ Quick Reference

| งาน | Command |
|---|---|
| เปิด `.venv` | `.venv\Scripts\activate` |
| ปิด `.venv` | `deactivate` |
| ดู Python Version | `python --version` |
| ดูตำแหน่ง Python | `where python` |
| ดู Package | `python -m pip list` |
| Update pip | `python -m pip install --upgrade pip` |
| ติดตั้ง Package | `python -m pip install <package>` |
| ติดตั้งจาก requirements | `python -m pip install -r requirements.txt` |
| สร้าง Folder | `mkdir FolderName` |
| สร้าง File เปล่า | `type nul > filename` |
| ดู File | `dir` |
| ดู Hidden File | `dir /a` |
| ดู Directory ปัจจุบัน | `cd` |
| กลับ 1 Directory | `cd ..` |
| ดู Tree | `tree /f` |
| Clear CMD | `cls` |
| เปิด VS Code | `code .` |
| Run Python File | `python path\file.py` |
| ดู Git Version | `git --version` |
| ดูตำแหน่ง Git | `where git` |
| สร้าง Git Repository | `git init` |
| ตั้ง Branch เป็น main | `git branch -M main` |
| ดู Git Status | `git status` |
| Stage ทุก File | `git add .` |
| Commit | `git commit -m "message"` |
| ดู History | `git log --oneline` |
| ดู Diff | `git diff` |

---

# 📝 รูปแบบการเพิ่ม Note ในอนาคต

เมื่อเพิ่มคำสั่งใหม่ แนะนำให้ใช้รูปแบบนี้:

```markdown
## ชื่อคำสั่ง

```cmd
command
```

### ใช้ทำอะไร

อธิบายว่าคำสั่งนี้ใช้สำหรับอะไร

### ตัวอย่าง

```cmd
example command
```

### ข้อควรระวัง

> ⚠️ ระบุกรณีที่อาจทำให้เกิดปัญหา
```

แนวทางนี้จะช่วยให้ Note อ่านง่าย และกลับมาอ่านภายหลังก็ยังเข้าใจว่า **คำสั่งนี้ใช้ทำอะไรและทำไมต้องใช้**

---

## 📚 เอกสารที่เกี่ยวข้อง

```text
AGENTS.md
docs/
├── COMMANDS.md
├── DEVELOPMENT.md
├── PROJECT_MAP.md
└── ARCHITECTURE.md
```

- `COMMANDS.md` — Cheat Sheet คำสั่งที่ใช้บ่อย
- `DEVELOPMENT.md` — วิธี Setup / Run / Test Project
- `PROJECT_MAP.md` — แผนที่ของ Codebase
- `ARCHITECTURE.md` — Architecture และ Data Flow ของระบบ
- `AGENTS.md` — ข้อแนะนำสำหรับ Codex และ AI Coding Agent

---

<p align="center">
  <strong>PyIoT Command Center — Developer Command Reference</strong>
</p>
