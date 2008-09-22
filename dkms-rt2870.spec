%define module rt2870
%define version 1.3.1.0
%define card Ralink RT2870 WiFi cards

%define distname 2008_0718_RT2870_Linux_STA_v%{version}

Summary: dkms package for %{module} driver
Name: dkms-%{module}
Version: %{version}
Release: %mkrel 2
Source0: http://www.ralinktech.com.tw/data/drivers/%{distname}.tar.bz2
Source1: dkms-rt2870-wext_compat.patch
Source2: dkms-rt2870-pid.patch
Patch0: dkms-rt2870-Makefile.patch
Patch1: dkms-rt2870-firmware.patch
Patch3: dkms-rt2870-strip_firmware.patch
License: GPLv2+
Group: System/Kernel and hardware
URL: http://www.ralinktech.com/
Requires(preun): dkms
Requires(post): dkms
Suggests: rt2870-firmware
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildArch: noarch

%description
This package contains the %{module} driver for
%{card}.

%prep
%setup -q -n %{distname}
%patch0 -p1
%patch1 -p1
%patch3 -p1

rm -rf tools

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/src/%{module}-%{version}-%{release}/patches
cat > %{buildroot}/usr/src/%{module}-%{version}-%{release}/dkms.conf <<EOF
PACKAGE_NAME=%{module}
PACKAGE_VERSION=%{version}-%{release}

DEST_MODULE_LOCATION[0]=/kernel/3rdparty/%{module}
BUILT_MODULE_NAME[0]=%{module}sta
BUILT_MODULE_LOCATION[0]=os/linux

MAKE[0]="make LINUX_SRC=\$kernel_source_dir HAS_WPA_SUPPLICANT=y HAS_NATIVE_WPA_SUPPLICANT_SUPPORT=y"
AUTOINSTALL="yes"

PATCH[0]="dkms-rt2870-wext_compat.patch"
PATCH_MATCH[0]="^2\.6\.(2[7-9])|([3-9][0-9]+)|([1-9][0-9][0-9]+)"
PATCH[1]="dkms-rt2870-pid.patch"
PATCH_MATCH[1]="^2\.6\.(2[7-9])|([3-9][0-9]+)|([1-9][0-9][0-9]+)"
EOF

tar c . | tar x -C %{buildroot}/usr/src/%{module}-%{version}-%{release}/

cp %{_sourcedir}/dkms-rt2870-wext_compat.patch \
   %{buildroot}/usr/src/%{module}-%{version}-%{release}/patches
cp %{_sourcedir}/dkms-rt2870-pid.patch \
   %{buildroot}/usr/src/%{module}-%{version}-%{release}/patches

mkdir -p %{buildroot}%{_sysconfdir}/Wireless/RT2870STA
install -m 644 RT2870STA.dat %{buildroot}%{_sysconfdir}/Wireless/RT2870STA

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%{_sysconfdir}/Wireless
/usr/src/%{module}-%{version}-%{release}/

%post -n dkms-%{module}
/usr/sbin/dkms --rpm_safe_upgrade add -m %{module} -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade build -m %{module} -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade install -m %{module} -v %{version}-%{release}
exit 0

%preun -n dkms-%{module}
/usr/sbin/dkms --rpm_safe_upgrade remove -m %{module} -v %{version}-%{release} --all
exit 0
