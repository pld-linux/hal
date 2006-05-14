#
# Conditional build:
%bcond_without	docs		# disable documentation building
#
Summary:	HAL - Hardware Abstraction Layer
Summary(pl):	HAL - abstrakcyjna warstwa dostêpu do sprzêtu
Name:		hal
Version:	0.5.7
Release:	1
License:	AFL v2.0 or GPL v2
Group:		Libraries
Source0:	http://freedesktop.org/~david/dist/%{name}-%{version}.tar.gz
# Source0-md5:	4163afb8285db64e00e7b1392b401d92
Source1:	%{name}daemon.init
Source2:	%{name}d.sysconfig
Source3:	%{name}-device-manager.desktop
Source4:	%{name}-libgphoto2.fdi
Source5:	%{name}-libgphoto_udev.rules
Source6:	%{name}-storage-policy-fixed-drives.fdi
Patch0:		%{name}-device_manager.patch
Patch1:		%{name}-script_path.patch
Patch2:		%{name}-tools.patch
URL:		http://freedesktop.org/Software/hal
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.60
%if %{with docs}
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-utils
BuildRequires:	doxygen
%endif
BuildRequires:	expat-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.6.0
BuildRequires:	intltool
BuildRequires:	libcap-devel
BuildRequires:	libselinux-devel >= 1.17.13
BuildRequires:	libtool
BuildRequires:	pciutils
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	python-modules
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	which
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post,preun):	/sbin/chkconfig
%pyrequires_eq	python
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus >= 0.60-4
Requires:	dmidecode
Requires:	glib2 >= 1:2.6.0
Requires:	python-dbus >= 0.60
Requires:	udev >= 1:079-2
Obsoletes:	hal-fstab-sync
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HAL is an implementation of a hardware abstraction layer.

%description -l pl
HAL jest implementacj± abstrakcyjnej warstwy dostêpu do sprzêtu.

%package libs
Summary:	HAL library
Summary(pl):	Biblioteka HAL
Group:		Libraries
Requires:	dbus-libs >= 0.33

%description libs
HAL library.

%description libs -l pl
Biblioteka HAL.

%package devel
Summary:	Header files for HAL library
Summary(pl):	Pliki nag³ówkowe biblioteki HAL
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus-devel >= 0.33

%description devel
Header files for HAL library.

%description devel -l pl
Pliki nag³ówkowe biblioteki HAL.

%package static
Summary:	Static HAL library
Summary(pl):	Statyczna biblioteka HAL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static HAL library.

%description static -l pl
Statyczna biblioteka HAL.

%package device-manager
Summary:	HAL device manager for GNOME
Summary(pl):	Zarz±dca urz±dzeñ HALa dla GNOME
Group:		X11/Applications
Requires:	python-gnome-ui
Requires:	python-gnome-vfs
Requires:	python-pygtk-glade
Requires:	%{name} = %{version}-%{release}

%description device-manager
GNOME program for displaying devices detected by HAL.

%description device-manager -l pl
Program dla GNOME wy¶wietlaj±cy urz±dzenia wykryte przez HAL.

%package gphoto
Summary:	Userspace support for digital cameras
Summary(pl):	Wsparcie dla kamer cyfrowych w przestrzeni u¿ytkownika
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	libusb >= 0.1.10-2
Requires:	udev >= 1:079-2
Obsoletes:	hotplug-digicam
Obsoletes:	udev-digicam
Provides:	udev-digicam

%description gphoto
Set of Udev rules and HAL device information file to handle digital
cameras in userspace.

%description gphoto -l pl
Zestaw regu³ Udev i plik z informacjami o urz±dzeniach HALa do
obs³ugi kamer cyfrowych w przestrzeni u¿ytkownika.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	%{?with_docs:--enable-docbook-docs} \
	%{!?with_docs:--disable-docbook-docs} \
	%{?with_docs:--enable-doxygen-docs} \
	%{!?with_docs:--disable-doxygen-docs} \
	--enable-fstab-sync \
	--enable-pcmcia-support \
	--enable-selinux \
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

install examples/volumed/*.py $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

find $RPM_BUILD_ROOT%{_datadir}/hal/device-manager -name "*.py" -exec rm -f {} \;

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/haldaemon
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/hald
install %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}

# hal-gphoto
install %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/%{name}/fdi/information/10freedesktop/10-gphoto.fdi
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/gphoto.rules

# policy file to ignore fixed disks.
install %{SOURCE6} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/fdi/policy/10osvendor/99-storage-policy-fixed-drives.fdi

rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/hotplug.d
rm -rf $RPM_BUILD_ROOT%{_libdir}/hal.hotplug
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/sl{_SI,}

%find_lang %{name}

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


%post gphoto
%service haldaemon restart
%banner %{name} -e << EOF
WARNING!
 hal-gphoto NO LONGER uses special "digicam" group.
 Please add yourself to more common "usb" group instead.

EOF

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README doc/TODO
%attr(755,root,root) %{_bindir}/hal-device
%attr(755,root,root) %{_bindir}/hal-find-by-capability
%attr(755,root,root) %{_bindir}/hal-find-by-property
%attr(755,root,root) %{_bindir}/hal-get-property
%attr(755,root,root) %{_bindir}/hal-set-property
%attr(755,root,root) %{_bindir}/lshal
%attr(755,root,root) %{_sbindir}/hald
%attr(755,root,root) %{_libdir}/hald-*
%attr(755,root,root) %{_libexecdir}/hal-*
%dir %{_libdir}/hal
%dir %{_libdir}/hal/scripts
%attr(755,root,root) %{_libdir}/hal/scripts/*

%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/fdi

%attr(754,root,root) /etc/rc.d/init.d/*
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/hald
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dbus*/system.d/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/*

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/fdi

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la

%dir %{_examplesdir}/%{name}-%{version}
%attr(755,root,root) %{_examplesdir}/%{name}-%{version}/*.py
%{_includedir}/%{name}
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files device-manager
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hal-device-manager
%dir %{_datadir}/%{name}/device-manager
%{_datadir}/%{name}/device-manager/*.py[co]
%{_datadir}/%{name}/device-manager/*.png
%{_datadir}/%{name}/device-manager/*.glade
%{_desktopdir}/*.desktop

%files gphoto
%defattr(644,root,root,755)
%{_sysconfdir}/udev/rules.d/gphoto.rules
%{_datadir}/%{name}/fdi/information/10freedesktop/10-gphoto.fdi
