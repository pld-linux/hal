Summary:	HAL - Hardware Abstraction Layer
Summary(pl):	HAL - abstrakcyjna warstwa dostêpu do sprzêtu
Name:		hal
Version:	0.4.7
Release:	3
License:	AFL v2.0 or GPL v2
Group:		Libraries
Source0:	http://freedesktop.org/~david/dist/%{name}-%{version}.tar.gz
# Source0-md5:	3386817a6811cce803bcfa8a20b05c51
Source1:	haldaemon.init
Source2:	hald.sysconfig
Source3:	%{name}-device-manager.desktop
Source4:	%{name}.readme
Patch0:		%{name}-device_manager.patch
Patch1:		%{name}-mount-options.patch
Patch2:		%{name}-link.patch
URL:		http://freedesktop.org/Software/hal
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.23.4
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-utils
BuildRequires:	doxygen
BuildRequires:	expat-devel
BuildRequires:	glib2-devel >= 2.2.2
BuildRequires:	intltool
BuildRequires:	libcap-devel
BuildRequires:	libselinux-devel >= 1.17.13
BuildRequires:	libtool
BuildRequires:	pciutils
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	python-modules
BuildRequires:	which
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post,preun):		/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus >= 0.23.4
Requires:	hotplug >= 2003_08_05
Requires:	mount >= 2.12-14
%pyrequires_eq	python
Requires:	python-dbus >= 0.23.4
Requires:	udev >= 015-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HAL is an implementation of a hardware abstraction layer.

%description -l pl
HAL jest implementacj± abstrakcyjnej warstwy dostêpu do sprzêtu.

%package libs
Summary:	HAL library
Summary(pl):	Biblioteka HAL
Group:		Libraries
Requires:	dbus-libs >= 0.22-5

%description libs
HAL library.

%description libs -l pl
Biblioteka HAL.

%package devel
Summary:	Header files for HAL library
Summary(pl):	Pliki nag³ówkowe biblioteki HAL
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus-devel >= 0.22-5

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
Requires:	python-pygtk-glade
Requires:	%{name} = %{version}-%{release}

%description device-manager
GNOME program for displaying devices detected by HAL.

%description device-manager -l pl
Program dla GNOME wy¶wietlaj±cy urz±dzenia wykryte przez HAL.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--enable-docbook-docs \
	--enable-doxygen-docs \
	--enable-fstab-sync \
	--enable-hotplug-map \
	--enable-pcmcia-support \
	--enable-selinux \
	--enable-verbose-mode \
	--with-hwdata=/etc

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} \
	$RPM_BUILD_ROOT{/etc/{sysconfig,rc.d}/init.d,%{_desktopdir},/var/run/hald}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install examples/volumed/*.py $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

find $RPM_BUILD_ROOT%{_datadir}/hal/device-manager -name "*.py" -exec rm -f {} \;

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/haldaemon
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/hald
install %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE4} .

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`/usr/bin/getgid haldaemon`" ]; then
	if [ "`getgid haldaemon`" != "126" ]; then
		echo "Error: group haldaemon doesn't have gid=126. Correct this before installing hal." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 126 -r -f haldaemon
fi
if [ -n "`/bin/id -u haldaemon 2>/dev/null`" ]; then
	if [ "`/bin/id -u haldaemon`" != "126" ]; then
		echo "Error: user haldaemon doesn't have uid=126. Correct this before installing hal." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 126 -r -d /usr/share/empty -s /bin/false -c "HAL daemon" -g haldaemon haldaemon 1>&2
fi

%post
/sbin/chkconfig --add haldaemon

if [ -f /var/lock/subsys/haldaemon ]; then
	/etc/rc.d/init.d/haldaemon restart >&2
else
	echo "Run \"/etc/rc.d/init.d/haldaemon start\" to start HAL daemon."
fi

%preun
if [ "$1" = "0" ];then
	if [ -f /var/lock/subsys/haldaemon ]; then
		/etc/rc.d/init.d/haldaemon stop >&2
	fi
	/sbin/chkconfig --del haldaemon
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig
	
%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README doc/TODO hal.readme
%attr(755,root,root) %{_bindir}/hal-get-property
%attr(755,root,root) %{_bindir}/hal-set-property
%attr(755,root,root) %{_bindir}/lshal
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/hald
%attr(755,root,root) %{_libdir}/hal.dev
%attr(755,root,root) %{_libdir}/hal.hotplug
%attr(755,root,root) %{_libdir}/hal-hotplug-map
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dbus*/system.d/*
%{_sysconfdir}/dev.d/default/*.dev
%{_sysconfdir}/hotplug.d/default/*.hotplug
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/capability.d
%dir %{_sysconfdir}/%{name}/device.d
%{_sysconfdir}/%{name}/device.d/*
%dir %{_sysconfdir}/%{name}/property.d
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}/hald.conf

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/fdi
%{_mandir}/man8/fstab-sync.8*
%{_examplesdir}/%{name}-%{version}
%dir /var/lib/hal
%dir /var/run/hald

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
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
%attr(755,root,root) %{_datadir}/%{name}/device-manager/hal-device-manager
%{_desktopdir}/*.desktop
