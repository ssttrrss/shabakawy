# دليل التثبيت السريع - Network Protector

## نظرة عامة

هذا الدليل يوضح كيفية تثبيت وتشغيل Network Protector على أنظمة Windows وLinux.

## متطلبات النظام

### الحد الأدنى
- **نظام التشغيل**: Windows 10 (64-bit) أو Linux Ubuntu 18.04+
- **المعالج**: Intel Core i3 2.0 GHz أو معادل
- **الذاكرة**: 4 GB RAM
- **التخزين**: 500 MB مساحة فارغة
- **الشبكة**: بطاقة شبكة Ethernet أو WiFi
- **الصلاحيات**: حساب مسؤول (Administrator/Root)

### المُوصى به
- **نظام التشغيل**: Windows 11 أو Linux Ubuntu 22.04+
- **المعالج**: Intel Core i5 3.0 GHz أو أفضل
- **الذاكرة**: 8 GB RAM أو أكثر
- **التخزين**: 2 GB مساحة فارغة
- **الشبكة**: بطاقة شبكة Gigabit

## التثبيت على Windows

### الطريقة الأولى: المثبت التلقائي (مُوصى به)

1. **تحميل المثبت**:
   ```
   تحميل NetworkProtectorSetup.exe من صفحة الإصدارات
   ```

2. **تشغيل المثبت**:
   - انقر بزر الماوس الأيمن على الملف
   - اختر "تشغيل كمسؤول" (Run as administrator)
   - إذا ظهر تحذير Windows Defender، اختر "تشغيل على أي حال"

3. **اتباع خطوات التثبيت**:
   - اقبل اتفاقية الترخيص
   - اختر مجلد التثبيت (افتراضي مُوصى به)
   - اختر إنشاء اختصارات سطح المكتب وقائمة ابدأ
   - انقر "تثبيت" وانتظر اكتمال العملية

4. **التحقق من التثبيت**:
   - ابحث عن "Network Protector" في قائمة ابدأ
   - أو انقر على الاختصار في سطح المكتب

### الطريقة الثانية: التثبيت اليدوي

1. **تحميل الملفات**:
   ```
   تحميل install.bat
   تحميل مجلد dist كاملاً
   ```

2. **تشغيل المثبت**:
   - انقر بزر الماوس الأيمن على `install.bat`
   - اختر "تشغيل كمسؤول"
   - اتبع التعليمات على الشاشة

### الطريقة الثالثة: البناء من المصدر

1. **تثبيت المتطلبات**:
   ```cmd
   # تثبيت Python 3.7+
   # تحميل من https://python.org
   
   # تثبيت Git
   # تحميل من https://git-scm.com
   ```

2. **تحميل المصدر**:
   ```cmd
   git clone https://github.com/networksecurity/network-protector.git
   cd network-protector
   ```

3. **تثبيت المكتبات**:
   ```cmd
   pip install -r requirements.txt
   ```

4. **بناء التطبيق**:
   ```cmd
   python build_windows.py
   ```

## التثبيت على Linux

### Ubuntu/Debian

#### الطريقة الأولى: حزمة DEB (مُوصى به)
```bash
# تحميل الحزمة
wget https://github.com/networksecurity/network-protector/releases/latest/download/network-protector_1.0.0_amd64.deb

# تثبيت الحزمة
sudo dpkg -i network-protector_1.0.0_amd64.deb

# حل التبعيات إن وجدت
sudo apt-get install -f
```

#### الطريقة الثانية: السكريپت التلقائي
```bash
# تحميل وتشغيل سكريپت التثبيت
wget https://github.com/networksecurity/network-protector/releases/latest/download/install.sh
chmod +x install.sh
sudo ./install.sh
```

#### الطريقة الثالثة: التثبيت اليدوي
```bash
# تثبيت المتطلبات
sudo apt-get update
sudo apt-get install python3 python3-pip python3-pyqt5 libpcap0.8

# تحميل المصدر
git clone https://github.com/networksecurity/network-protector.git
cd network-protector

# تثبيت مكتبات Python
pip3 install -r requirements.txt

# تشغيل التطبيق
cd src
sudo python3 main.py
```

### CentOS/RHEL/Fedora

#### حزمة RPM
```bash
# تحميل حزمة RPM
wget https://github.com/networksecurity/network-protector/releases/latest/download/network-protector-1.0.0-1.x86_64.rpm

# تثبيت الحزمة
sudo rpm -ivh network-protector-1.0.0-1.x86_64.rpm

# أو باستخدام dnf (Fedora)
sudo dnf install network-protector-1.0.0-1.x86_64.rpm
```

#### التثبيت اليدوي
```bash
# CentOS/RHEL
sudo yum install python3 python3-pip python3-qt5 libpcap

# Fedora
sudo dnf install python3 python3-pip python3-qt5 libpcap

# باقي الخطوات مثل Ubuntu
```

### جميع توزيعات Linux (AppImage)

```bash
# تحميل AppImage
wget https://github.com/networksecurity/network-protector/releases/latest/download/NetworkProtector-1.0.0-x86_64.AppImage

# جعل الملف قابل للتنفيذ
chmod +x NetworkProtector-1.0.0-x86_64.AppImage

# تشغيل التطبيق
sudo ./NetworkProtector-1.0.0-x86_64.AppImage
```

## البناء من المصدر

### تحميل المصدر
```bash
git clone https://github.com/networksecurity/network-protector.git
cd network-protector
```

### تثبيت المتطلبات
```bash
pip3 install -r requirements.txt
```

### بناء الملفات التنفيذية

#### Windows
```bash
python build_windows.py
```

#### Linux
```bash
python build_linux.py
```

## التشغيل لأول مرة

### Windows
1. ابحث عن "Network Protector" في قائمة ابدأ
2. انقر بزر الماوس الأيمن واختر "تشغيل كمسؤول"
3. اتبع معالج الإعداد الأولي

### Linux
```bash
# من الطرفية
sudo network-protector

# أو من قائمة التطبيقات
# ابحث عن "Network Protector"
```

## الإعداد الأولي

1. **اختيار اللغة**: العربية أو الإنجليزية
2. **اختيار الوضع**: مبتدئ أو متقدم
3. **اختيار واجهة الشبكة**: البطاقة المتصلة بالشبكة
4. **مسح الشبكة الأولي**: اكتشاف الأجهزة المتصلة
5. **إعداد الراوتر** (اختياري): إدخال معلومات الراوتر

## التحقق من التثبيت

### Windows
```cmd
# من سطر الأوامر
network-protector --version

# أو البحث في قائمة ابدأ
```

### Linux
```bash
# من الطرفية
network-protector --version

# أو
which network-protector
```

## استكشاف مشاكل التثبيت

### Windows

**خطأ "يتطلب صلاحيات المسؤول":**
- تأكد من تشغيل المثبت كمسؤول
- انقر بزر الماوس الأيمن واختر "تشغيل كمسؤول"

**خطأ "ملف تالف":**
- أعد تحميل الملف
- تأكد من اكتمال التحميل
- تحقق من برامج مكافحة الفيروسات

**خطأ "فشل في تثبيت المتطلبات":**
- تأكد من اتصال الإنترنت
- ثبت Python 3.7+ يدوياً
- ثبت Visual C++ Redistributable

### Linux

**خطأ "Package dependency issues":**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -f

# CentOS/RHEL/Fedora
sudo yum update
# أو
sudo dnf update
```

**خطأ "Permission denied":**
```bash
# تأكد من الصلاحيات
chmod +x install.sh
sudo ./install.sh
```

**خطأ "Command not found":**
```bash
# إضافة المسار للـ PATH
echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
source ~/.bashrc
```

## إلغاء التثبيت

### Windows
1. اذهب إلى "إعدادات" > "التطبيقات"
2. ابحث عن "Network Protector"
3. انقر "إلغاء التثبيت"

أو من سطر الأوامر:
```cmd
# تشغيل أداة إلغاء التثبيت
"C:\Program Files\Network Security Solutions\Network Protector\uninstall.exe"
```

### Linux

#### Ubuntu/Debian
```bash
sudo dpkg -r network-protector
```

#### CentOS/RHEL/Fedora
```bash
sudo rpm -e network-protector
```

#### التثبيت اليدوي
```bash
sudo rm -rf /opt/network-protector
sudo rm -f /usr/bin/network-protector
sudo rm -f /usr/share/applications/network-protector.desktop
sudo rm -f /etc/systemd/system/network-protector.service
```

## الدعم الفني

إذا واجهت مشاكل في التثبيت:

1. **راجع هذا الدليل** للحلول الشائعة
2. **تحقق من ملفات السجل** في مجلد التثبيت
3. **تواصل معنا**:
   - GitHub Issues: https://github.com/networksecurity/network-protector/issues
   - البريد الإلكتروني: support@networksecurity.com

## الخطوات التالية

بعد التثبيت الناجح:
1. اقرأ [دليل المستخدم](USER_MANUAL.md) للتعرف على المميزات
2. شاهد الفيديوهات التعليمية
3. انضم إلى المجتمع للحصول على المساعدة

---

**Network Protector Team**  
حماية شبكتك، أمان معلوماتك

