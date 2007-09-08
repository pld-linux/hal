# TODO:
#	- review patches
#
# Conditional build:
%bcond_without	doc		# disable documentation building
#
%define	_snap	rc2
Summary:	HAL - Hardware Abstraction Layer
Summary(pl.UTF-8):	HAL - abstrakcyjna warstwa dostępu do sprzętu
Name:		hal
Version:	0.5.10
Release:	0.%{_snap}.1
License:	AFL v2.0 or GPL v2
Group:		Libraries
Source0:	http://hal.freedesktop.org/releases/%{name}-%{version}%{_snap}.tar.gz
# Source0-md5:	fd7770348b4fc52d4df0670f1eeaf806
Source1:	%{name}daemon.init
Source2:	%{name}d.sysconfig
Source3:	%{name}-storage-policy-fixed-drives.fdi
Patch0:		%{name}-tools.patch
Patch1:		%{name}-parted.patch
URL:		http://freedesktop.org/Software/hal
#BuildRequires:	ConsoleKit-devel
BuildRequires:	PolicyKit-devel >= 0.5
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.71
%if %{with doc}
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-utils
BuildRequires:	doxygen
%endif
BuildRequires:	expat-devel >= 1:1.95.8
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.12.1
BuildRequires:	intltool >= 0.22
BuildRequires:	libcap-devel
BuildRequires:	libselinux-devel >= 1.17.13
BuildRequires:	libtool
BuildRequires:	libusb-devel >= 0.1.10a
BuildRequires:	libvolume_id-devel >= 0.97
# 1.7.1/1.8.0/1.8.1/1.8.2 or 1.8.6
BuildRequires:	parted-devel >= 1.7.1
BuildRequires:	pciutils-devel >= 2.2.3
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	which
# R: cryptsetup-luks >= 1.0.1 (at runtime)
Requires(post,preun):	/sbin/chkconfig
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
%pyrequires_eq	python
Requires:	%{name}-libs = %{version}-%{release}
#Requires:	ConsoleKit
Requires:	PolicyKit >= 0.2
Requires:	dbus >= 0.91
Requires:	dmidecode >= 2.7
Requires:	glib2 >= 1:2.12.1
Requires:	python-dbus >= 0.71
Requires:	udev >= 1:089
Obsoletes:	hal-fstab-sync
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
#%%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	%{?with_doc:--enable-docbook-docs} \
	%{!?with_doc:--disable-docbook-docs} \
	%{?with_doc:--enable-doxygen-docs} \
	%{!?with_doc:--disable-doxygen-docs} \
	--enable-fstab-sync \
	--enable-pcmcia-support \
	--enable-selinux \
	--enable-policy-kit \
	--enable-console-kit \
	--enable-parted \
	--enable-acpi-ibm \
	--enable-acpi-toshiba \
	--enable-acl-management \
	--enable-sonypic \
	--enable-umount-helper \
%ifarch %{ix86} %{x8664}
	--with-macbook \
	--with-macbookpro \
%endif
	--with-cpufreq \
	--with-usb-csr \
	--with-html-dir=%{_gtkdocdir} \
	--with-hwdata=%{_sysconfdir} \
	--with-pid-file=%{_localstatedir}/run/hald.pid
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} \
	$RPM_BUILD_ROOT{/etc/{sysconfig,rc.d}/init.d,%{_desktopdir}} \
	$RPM_BUILD_ROOT/etc/hal/fdi/{information,policy,preprobe} \
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
%attr(755,root,root) %{_libdir}/hald-*
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
%dir /var/lib/hal
%dir /var/run/hald
%dir /var/run/hald/hald-local
%dir /var/run/hald/hald-runner

%{_mandir}/man[18]/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhal.so.*.*.*
%attr(755,root,root) %{_libdir}/libhal-storage.so.*.*.*

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
