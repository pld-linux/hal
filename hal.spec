#
# Conditional build:
%bcond_without	doc		# disable documentation building
#
Summary:	HAL - Hardware Abstraction Layer
Summary(pl.UTF-8):	HAL - abstrakcyjna warstwa dostępu do sprzętu
Name:		hal
Version:	0.5.14
Release:	3
License:	AFL v2.0 or GPL v2
Group:		Libraries
Source0:	http://hal.freedesktop.org/releases/%{name}-%{version}.tar.gz
# Source0-md5:	e9163df591a6f38f59fdbfe33e73bf20
Source1:	%{name}daemon.init
Source2:	%{name}d.sysconfig
Source3:	%{name}-storage-policy-fixed-drives.fdi
Patch0:		%{name}-tools.patch
Patch1:		%{name}-ac.patch
Patch2:		%{name}-link.patch
Patch3:		%{name}-rethink.patch
Patch4:		%{name}-showexec.patch
Patch5:		%{name}-x11-zap.patch
Patch6:		%{name}-out.patch
URL:		http://freedesktop.org/Software/hal
BuildRequires:	ConsoleKit-devel
BuildRequires:	PolicyKit-devel >= 0.7
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-glib-devel >= 0.71
%if %{with doc}
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-utils
BuildRequires:	doxygen
%endif
BuildRequires:	expat-devel >= 1:1.95.8
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.14.0
BuildRequires:	gperf
BuildRequires:	gtk-doc >= 1.3
BuildRequires:	intltool >= 0.22
BuildRequires:	libblkid-devel >= 2.15
%ifarch %{ix86} %{x8664}
BuildRequires:	libsmbios-devel >= 0.13.4
%endif
BuildRequires:	libtool
BuildRequires:	libusb-compat-devel
# 1.7.1 or 1.8.0+
BuildRequires:	parted-devel >= 1.8.0
BuildRequires:	pciutils-devel >= 2.2.3
BuildRequires:	pkgconfig
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	sed >= 4.0
BuildRequires:	which
BuildRequires:	xmlto
# R: cryptsetup-luks >= 1.0.1 (at runtime)
Requires(post,preun):	/sbin/chkconfig
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/bin/polkit-auth
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
%pyrequires_eq	python
Requires:	%{name}-libs = %{version}-%{release}
#Requires:	ConsoleKit
Requires:	PolicyKit >= 0.7
Requires:	dbus >= 0.91
Requires:	dmidecode >= 2.7
Requires:	glib2 >= 1:2.14.0
Requires:	hal-info
Requires:	python-dbus >= 0.71
Requires:	udev-acl
Requires:	udev-core >= 1:125
# require pciutils and usbutils with .ids in expected location
Requires:	/etc/pci.ids
Requires:	/etc/usb.ids
Obsoletes:	hal-device-manager
Obsoletes:	hal-fstab-sync
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
HAL is an implementation of a hardware abstraction layer.

%description -l pl.UTF-8
HAL jest implementacją abstrakcyjnej warstwy dostępu do sprzętu.

%package libs
Summary:	HAL library
Summary(pl.UTF-8):	Biblioteka HAL
Group:		Libraries
Requires:	dbus-libs >= 0.91

%description libs
HAL library.

%description libs -l pl.UTF-8
Biblioteka HAL.

%package devel
Summary:	Header files for HAL library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki HAL
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus-devel >= 0.91

%description devel
Header files for HAL library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki HAL.

%package static
Summary:	Static HAL library
Summary(pl.UTF-8):	Statyczna biblioteka HAL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static HAL library.

%description static -l pl.UTF-8
Statyczna biblioteka HAL.

%package apidocs
Summary:	HAL API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki HAL
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
HAL API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki HAL.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
sed '450,550 s/USE_LIBUSB/USE_LIBUSB_/g' -i configure.in

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	POLKIT_POLICY_FILE_VALIDATE=%{_bindir}/polkit-policy-file-validate \
	%{?with_doc:--enable-docbook-docs} \
	%{!?with_doc:--disable-docbook-docs} \
	%{?with_doc:--enable-doxygen-docs} \
	%{!?with_doc:--disable-doxygen-docs} \
	--enable-acl-management \
	--enable-acpi-ibm \
	--enable-acpi-toshiba \
	--enable-console-kit \
	--enable-parted \
	--enable-policy-kit \
	--enable-sonypic \
	--enable-umount-helper \
	--with-cpufreq \
	--with-html-dir=%{_gtkdocdir} \
	--with-hwdata=%{_sysconfdir} \
	--with-udev-prefix=%{_sysconfdir} \
%ifarch %{ix86} %{x8664}
	--with-macbook \
	--with-macbookpro \
%endif
	--with-pid-file=%{_localstatedir}/run/hald.pid \
	--with-usb-csr
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} \
	$RPM_BUILD_ROOT{/etc/{sysconfig,rc.d}/init.d,%{_desktopdir}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/hal/fdi/{information,policy,preprobe} \
	$RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

#find $RPM_BUILD_ROOT%{_datadir}/hal/device-manager -name "*.py" -exec rm -f {} \;

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/haldaemon
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/hald

# policy file to ignore fixed disks.
install %{SOURCE3} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/fdi/policy/10osvendor/99-storage-policy-fixed-drives.fdi

rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/hotplug.d
rm -rf $RPM_BUILD_ROOT%{_libdir}/hal.hotplug


%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 126 -r -f haldaemon
%useradd -u 126 -r -d /usr/share/empty -s /bin/false -c "HAL daemon" -g haldaemon haldaemon
/usr/bin/polkit-auth --user haldaemon --grant org.freedesktop.policykit.read 2> /dev/null || :


%post
/sbin/chkconfig --add haldaemon
%service haldaemon restart

%preun
if [ "$1" = "0" ]; then
	%service -q haldaemon stop
	/sbin/chkconfig --del haldaemon
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig


%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README doc/TODO
%attr(755,root,root) %{_bindir}/hal-device
%attr(755,root,root) %{_bindir}/hal-disable-polling
%attr(755,root,root) %{_bindir}/hal-find-by-capability
%attr(755,root,root) %{_bindir}/hal-find-by-property
%attr(755,root,root) %{_bindir}/hal-get-property
%attr(755,root,root) %{_bindir}/hal-is-caller-locked-out
%attr(755,root,root) %{_bindir}/hal-is-caller-privileged
%attr(755,root,root) %{_bindir}/hal-lock
%attr(755,root,root) %{_bindir}/hal-set-property
%attr(755,root,root) %{_bindir}/hal-setup-keymap
%attr(755,root,root) %{_bindir}/lshal
%attr(755,root,root) %{_sbindir}/hald
%attr(755,root,root) /sbin/umount.hal
%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/hald-*
%attr(755,root,root) %{_libexecdir}/hal-*
%dir %{_libdir}/hal
%dir %{_libdir}/hal/scripts
%attr(755,root,root) %{_libdir}/hal/scripts/*

%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/fdi

%attr(754,root,root) /etc/rc.d/init.d/*
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/hald
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dbus*/system.d/hal.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/90-hal.rules
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/PolicyKit/policy/*.policy

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/fdi

%dir /var/cache/hald
%dir /var/run/hald
%dir /var/run/hald/hald-local
%dir /var/run/hald/hald-runner

%{_mandir}/man[18]/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhal.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhal.so.1
%attr(755,root,root) %{_libdir}/libhal-storage.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhal-storage.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhal.so
%attr(755,root,root) %{_libdir}/libhal-storage.so
%{_libdir}/libhal.la
%{_libdir}/libhal-storage.la
%{_includedir}/%{name}
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libhal.a
%{_libdir}/libhal-storage.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libhal
%{_gtkdocdir}/libhal-storage
