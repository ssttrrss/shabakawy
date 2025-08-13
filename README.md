# shabakawy - شيكتك في الحفظ والصون

<div align="center">

![shabakawy Logo](assets/images/logo.png)

**أداة احترافية لحماية وتحليل الشبكات**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)]()

[English](#english) | [العربية](#arabic)

</div>

---

## العربية {#arabic}

### نظرة عامة

Network Protector هو تطبيق احترافي مصمم لحماية وتحليل الشبكات بواجهة رسومية أنيقة وسهلة الاستخدام. يوفر التطبيق مراقبة شاملة للشبكة في الوقت الفعلي، كشف التهديدات تلقائياً، والتحكم في إعدادات الراوتر.

### المميزات الرئيسية

#### 🔍 مراقبة الشبكة
- **التقاط الحزم في الوقت الفعلي**: مراقبة جميع حزم البيانات المارة عبر الشبكة
- **تحليل البروتوكولات**: دعم TCP، UDP، ICMP وبروتوكولات أخرى
- **إحصائيات مفصلة**: عرض معلومات شاملة عن حركة الشبكة

#### 🛡️ كشف التهديدات
- **كشف هجمات DDoS**: اكتشاف تلقائي لهجمات الحرمان من الخدمة
- **كشف Port Scanning**: رصد محاولات مسح المنافذ المشبوهة
- **كشف MITM**: اكتشاف هجمات الرجل في المنتصف
- **كشف IP/MAC Spoofing**: رصد محاولات انتحال الهوية
- **تنبيهات فورية**: إشعارات لحظية عند اكتشاف التهديدات

#### 🌐 إدارة الشبكة
- **اكتشاف الأجهزة**: مسح تلقائي لجميع الأجهزة المتصلة بالشبكة
- **خريطة الشبكة**: عرض مرئي لجميع الأجهزة مع معلوماتها
- **معلومات الأجهزة**: عرض IP، MAC، الشركة المصنعة، ونوع الجهاز

#### ⚙️ التحكم في الراوتر
- **دعم راوترات متعددة**: TP-Link، D-Link، Netgear، Linksys
- **تغيير كلمة مرور WiFi**: تحديث كلمة المرور عن بُعد
- **إعادة تشغيل الراوتر**: التحكم في إعادة التشغيل
- **حظر الأجهزة**: منع أجهزة معينة من الاتصال
- **التحكم في السرعة**: تحديد حدود السرعة لكل جهاز

#### 📊 الإحصائيات والتقارير
- **رسوم بيانية تفاعلية**: عرض البيانات بصرياً
- **تقارير مفصلة**: تحليل شامل لحالة الشبكة والأمان
- **تصدير البيانات**: حفظ التقارير بصيغ مختلفة
- **سجل تاريخي**: حفظ جميع الأحداث والتهديدات

#### 🎨 واجهة المستخدم
- **تصميم أنيق**: واجهة حديثة وسهلة الاستخدام
- **الوضع الليلي**: دعم الثيم الداكن
- **دعم اللغات**: العربية والإنجليزية
- **وضع المبتدئ/المتقدم**: واجهات مخصصة حسب مستوى المستخدم
- **تجاوب مع الشاشات**: يعمل على جميع أحجام الشاشات

### متطلبات النظام

#### الحد الأدنى
- **نظام التشغيل**: Windows 10 أو Linux (Ubuntu 18.04+)
- **المعالج**: Intel Core i3 أو AMD Ryzen 3
- **الذاكرة**: 4 GB RAM
- **التخزين**: 500 MB مساحة فارغة
- **الشبكة**: بطاقة شبكة Ethernet أو WiFi

#### المُوصى به
- **نظام التشغيل**: Windows 11 أو Linux (Ubuntu 22.04+)
- **المعالج**: Intel Core i5 أو AMD Ryzen 5
- **الذاكرة**: 8 GB RAM
- **التخزين**: 2 GB مساحة فارغة
- **الشبكة**: بطاقة شبكة Gigabit

### التثبيت

#### Windows

1. **تحميل المثبت**:
   ```
   تحميل NetworkProtectorSetup.exe
   ```

2. **تشغيل المثبت**:
   - انقر بزر الماوس الأيمن على الملف واختر "تشغيل كمسؤول"
   - اتبع تعليمات المثبت

3. **تشغيل التطبيق**:
   - من قائمة ابدأ أو من سطح المكتب
   - أو من سطر الأوامر: `network-protector`

#### Linux

##### التثبيت التلقائي (مُوصى به)
```bash
# تحميل وتشغيل سكريپت التثبيت
wget https://github.com/networksecurity/network-protector/releases/latest/download/install.sh
chmod +x install.sh
sudo ./install.sh
```

##### Ubuntu/Debian
```bash
# تحميل حزمة DEB
wget https://github.com/networksecurity/network-protector/releases/latest/download/network-protector_1.0.0_amd64.deb

# تثبيت الحزمة
sudo dpkg -i network-protector_1.0.0_amd64.deb
sudo apt-get install -f  # لحل التبعيات إن وجدت
```

##### CentOS/RHEL/Fedora
```bash
# تحميل حزمة RPM
wget https://github.com/networksecurity/network-protector/releases/latest/download/network-protector-1.0.0-1.x86_64.rpm

# تثبيت الحزمة
sudo rpm -ivh network-protector-1.0.0-1.x86_64.rpm
```

##### AppImage (جميع توزيعات Linux)
```bash
# تحميل AppImage
wget https://github.com/networksecurity/network-protector/releases/latest/download/NetworkProtector-1.0.0-x86_64.AppImage

# جعل الملف قابل للتنفيذ
chmod +x NetworkProtector-1.0.0-x86_64.AppImage

# تشغيل التطبيق
./NetworkProtector-1.0.0-x86_64.AppImage
```

### الاستخدام

#### البدء السريع

1. **تشغيل التطبيق**:
   - Windows: من قائمة ابدأ أو سطح المكتب
   - Linux: `network-protector` أو من قائمة التطبيقات

2. **منح الصلاحيات**:
   - سيطلب التطبيق صلاحيات المسؤول لمراقبة الشبكة
   - اقبل الطلب للحصول على الوظائف الكاملة

3. **بدء المراقبة**:
   - انقر على زر "بدء المراقبة"
   - سيبدأ التطبيق في رصد حركة الشبكة

#### الواجهة الرئيسية

##### لوحة التحكم
- **الإحصائيات السريعة**: عرض سريع لحالة الشبكة
- **التنبيهات الأخيرة**: آخر التهديدات المكتشفة
- **رسم بياني للحركة**: مراقبة حركة الشبكة في الوقت الفعلي

##### خريطة الشبكة
- **قائمة الأجهزة**: جميع الأجهزة المتصلة بالشبكة
- **معلومات الأجهزة**: IP، MAC، الشركة المصنعة، النوع
- **حالة الاتصال**: متصل/غير متصل

##### مراقبة الحركة
- **سجل الحزم**: تفاصيل جميع الحزم المُلتقطة
- **إحصائيات الحركة**: معدل الحزم والبيانات
- **تصفية البيانات**: عرض أنواع معينة من الحركة

##### كشف التهديدات
- **إعدادات الكشف**: تخصيص أنواع التهديدات المراقبة
- **سجل التهديدات**: جميع التهديدات المكتشفة
- **مستوى الحساسية**: تحديد دقة الكشف

##### التحكم في الراوتر
- **معلومات الراوتر**: نوع وحالة الراوتر
- **إعدادات الشبكة**: تغيير كلمة مرور WiFi
- **إدارة الأجهزة**: حظر أو تحديد سرعة الأجهزة

##### الإحصائيات
- **رسوم بيانية**: تحليل بصري للبيانات
- **تقارير**: ملخصات مفصلة عن حالة الشبكة
- **تصدير البيانات**: حفظ التقارير كملفات

#### الإعدادات المتقدمة

##### إعدادات الكشف
```
- حساسية الكشف: منخفضة/متوسطة/عالية
- أنواع التهديدات: تفعيل/إلغاء تفعيل أنواع معينة
- عتبات التنبيه: تخصيص حدود الكشف
```

##### إعدادات الواجهة
```
- اللغة: العربية/الإنجليزية
- الثيم: فاتح/داكن
- وضع العرض: مبتدئ/متقدم
```

##### إعدادات الشبكة
```
- واجهة الشبكة: اختيار بطاقة الشبكة
- مرشحات الحزم: تحديد أنواع الحزم المراقبة
- حفظ البيانات: مدة الاحتفاظ بالسجلات
```

### استكشاف الأخطاء

#### مشاكل شائعة

##### "فشل في بدء المراقبة"
```
الحل:
1. تأكد من تشغيل التطبيق بصلاحيات المسؤول
2. تحقق من وجود بطاقة شبكة نشطة
3. أعد تشغيل التطبيق
```

##### "لا يمكن الاتصال بالراوتر"
```
الحل:
1. تأكد من صحة عنوان IP للراوتر
2. تحقق من اسم المستخدم وكلمة المرور
3. تأكد من تفعيل الإدارة عن بُعد في الراوتر
```

##### "لا تظهر الأجهزة في خريطة الشبكة"
```
الحل:
1. انتظر بضع دقائق لاكتمال المسح
2. تأكد من وجود أجهزة متصلة بالشبكة
3. أعد تشغيل مسح الشبكة
```

#### ملفات السجل
```
Windows: %APPDATA%\NetworkProtector\logs\
Linux: ~/.local/share/NetworkProtector/logs/
```

### الأمان والخصوصية

#### حماية البيانات
- جميع البيانات تُحفظ محلياً على جهازك
- لا يتم إرسال أي معلومات إلى خوادم خارجية
- كلمات المرور مُشفرة في قاعدة البيانات المحلية

#### الصلاحيات المطلوبة
- **صلاحيات المسؤول**: لمراقبة حركة الشبكة
- **الوصول للشبكة**: لاكتشاف الأجهزة والتحكم في الراوتر
- **كتابة الملفات**: لحفظ السجلات والإعدادات

### التطوير والمساهمة

#### بناء التطبيق من المصدر

##### متطلبات التطوير
```bash
Python 3.7+
PyQt5 5.15+
scapy 2.4+
matplotlib 3.3+
pandas 1.2+
psutil 5.8+
```

##### تحميل المصدر
```bash
git clone https://github.com/networksecurity/network-protector.git
cd network-protector
```

##### تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

##### تشغيل التطبيق
```bash
cd src
python main.py
```

##### بناء الملفات التنفيذية

###### Windows
```bash
python build_windows.py
```

###### Linux
```bash
python build_linux.py
```

#### هيكل المشروع
```
network_protector/
├── src/                    # الكود المصدري
│   ├── main.py            # نقطة الدخول الرئيسية
│   ├── gui/               # واجهة المستخدم
│   ├── network/           # وحدات الشبكة
│   ├── data/              # إدارة البيانات
│   ├── utils/             # أدوات مساعدة
│   └── config/            # ملفات الإعدادات
├── assets/                # الموارد (صور، أيقونات)
├── installers/            # ملفات التثبيت
├── requirements.txt       # متطلبات Python
├── setup.py              # إعداد التثبيت
├── build_windows.py      # سكريپت بناء Windows
├── build_linux.py        # سكريپت بناء Linux
└── README.md             # هذا الملف
```

### الدعم والمساعدة

#### طرق التواصل
- **GitHub Issues**: [رفع تقرير خطأ أو طلب ميزة](https://github.com/networksecurity/network-protector/issues)
- **البريد الإلكتروني**: info@networksecurity.com
- **الوثائق**: [دليل المستخدم الكامل](https://network-protector.readthedocs.io/)

#### الأسئلة الشائعة
سيتم إضافة قسم الأسئلة الشائعة قريباً.

### الترخيص

هذا المشروع مرخص تحت رخصة MIT. راجع ملف [LICENSE](LICENSE) للتفاصيل.

### شكر وتقدير

- **Scapy**: مكتبة تحليل الحزم
- **PyQt5**: إطار عمل الواجهة الرسومية
- **Matplotlib**: مكتبة الرسوم البيانية
- **جميع المساهمين**: الذين ساعدوا في تطوير هذا المشروع

---

## English {#english}

### Overview

Network Protector is a professional network security and analysis application designed with an elegant and user-friendly graphical interface. The application provides comprehensive real-time network monitoring, automatic threat detection, and router management capabilities.

### Key Features

#### 🔍 Network Monitoring
- **Real-time Packet Capture**: Monitor all data packets passing through the network
- **Protocol Analysis**: Support for TCP, UDP, ICMP, and other protocols
- **Detailed Statistics**: Comprehensive network traffic information

#### 🛡️ Threat Detection
- **DDoS Attack Detection**: Automatic detection of denial-of-service attacks
- **Port Scanning Detection**: Monitor suspicious port scanning attempts
- **MITM Detection**: Detect man-in-the-middle attacks
- **IP/MAC Spoofing Detection**: Monitor identity spoofing attempts
- **Instant Alerts**: Real-time notifications when threats are detected

#### 🌐 Network Management
- **Device Discovery**: Automatic scanning of all connected devices
- **Network Map**: Visual display of all devices with their information
- **Device Information**: Display IP, MAC, manufacturer, and device type

#### ⚙️ Router Control
- **Multiple Router Support**: TP-Link, D-Link, Netgear, Linksys
- **WiFi Password Change**: Remote password updates
- **Router Reboot**: Control router restart
- **Device Blocking**: Prevent specific devices from connecting
- **Speed Control**: Set speed limits for each device

#### 📊 Statistics and Reports
- **Interactive Charts**: Visual data representation
- **Detailed Reports**: Comprehensive network and security analysis
- **Data Export**: Save reports in various formats
- **Historical Log**: Store all events and threats

#### 🎨 User Interface
- **Elegant Design**: Modern and user-friendly interface
- **Dark Mode**: Dark theme support
- **Multi-language Support**: Arabic and English
- **Beginner/Advanced Mode**: Customized interfaces based on user level
- **Responsive Design**: Works on all screen sizes

### System Requirements

#### Minimum
- **Operating System**: Windows 10 or Linux (Ubuntu 18.04+)
- **Processor**: Intel Core i3 or AMD Ryzen 3
- **Memory**: 4 GB RAM
- **Storage**: 500 MB free space
- **Network**: Ethernet or WiFi network card

#### Recommended
- **Operating System**: Windows 11 or Linux (Ubuntu 22.04+)
- **Processor**: Intel Core i5 or AMD Ryzen 5
- **Memory**: 8 GB RAM
- **Storage**: 2 GB free space
- **Network**: Gigabit network card

### Installation

#### Windows

1. **Download Installer**:
   ```
   Download NetworkProtectorSetup.exe
   ```

2. **Run Installer**:
   - Right-click the file and select "Run as administrator"
   - Follow the installer instructions

3. **Launch Application**:
   - From Start menu or desktop
   - Or from command line: `network-protector`

#### Linux

##### Automatic Installation (Recommended)
```bash
# Download and run installation script
wget https://github.com/networksecurity/network-protector/releases/latest/download/install.sh
chmod +x install.sh
sudo ./install.sh
```

##### Ubuntu/Debian
```bash
# Download DEB package
wget https://github.com/networksecurity/network-protector/releases/latest/download/network-protector_1.0.0_amd64.deb

# Install package
sudo dpkg -i network-protector_1.0.0_amd64.deb
sudo apt-get install -f  # Resolve dependencies if needed
```

##### CentOS/RHEL/Fedora
```bash
# Download RPM package
wget https://github.com/networksecurity/network-protector/releases/latest/download/network-protector-1.0.0-1.x86_64.rpm

# Install package
sudo rpm -ivh network-protector-1.0.0-1.x86_64.rpm
```

##### AppImage (All Linux Distributions)
```bash
# Download AppImage
wget https://github.com/networksecurity/network-protector/releases/latest/download/NetworkProtector-1.0.0-x86_64.AppImage

# Make executable
chmod +x NetworkProtector-1.0.0-x86_64.AppImage

# Run application
./NetworkProtector-1.0.0-x86_64.AppImage
```

### Usage

#### Quick Start

1. **Launch Application**:
   - Windows: From Start menu or desktop
   - Linux: `network-protector` or from applications menu

2. **Grant Permissions**:
   - The application will request administrator privileges for network monitoring
   - Accept the request to get full functionality

3. **Start Monitoring**:
   - Click the "Start Monitoring" button
   - The application will begin monitoring network traffic

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/networksecurity/network-protector/issues)
- **Email**: info@networksecurity.com
- **Documentation**: [Complete User Guide](https://network-protector.readthedocs.io/)

---

<div align="center">

**Network Protector** - حماية شبكتك، أمان معلوماتك

Made with ❤️ by Network Security Solutions

</div>

