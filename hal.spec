%define		_snap	20040918
Summary:	HAL - Hardware Abstraction Layer
Summary(pl):	HAL - abstrakcyjna warstwa dostêpu do sprzêtu
Name:		hal
Version:	0.2.98
Release:	3
License:	AFL v2.0 or GPL v2
Group:		Libraries
#Source0:	%{name}-%{version}-%{_snap}.tar.bz2
Source0:	http://freedesktop.org/~david/dist/%{name}-%{version}.tar.gz
# Source0-md5:	cc289e50e00330032604e02392ffde3a
Source1:	haldaemon.init
Source2:	%{name}-device-manager.desktop
URL:		http://freedesktop.org/Software/hal
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.22
BuildRequires:	docbook-dtd412-xml
Buildrequires:	docbook-utils
BuildRequires:	doxygen
BuildRequires:	expat-devel
BuildRequires:	glib2-devel >= 2.2.2
BuildRequires:	libcap-devel
BuildRequires:	libselinux-devel >= 1.17.13
BuildRequires:	libtool
BuildRequires:	pciutils
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post,preun):		/sbin/chkconfig
Requires(post,postun):	/sbin/ldconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus >= 0.22
Requires:	hotplug >= 2003_08_05
Requires:	python-dbus >= 0.22
Requires:	python-gnome-ui
Requires:	python-pygtk-glade
Requires:	udev >= 015-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HAL is an implementation of a hardware abstraction layer.

%description -l pl
HAL jest implementacj± abstrakcyjnej warstwy dostêpu do sprzêtu.

%package devel
Summary:	Header files for HAL library
Summary(pl):	Pliki nag³ówkowe biblioteki HAL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for HAL library.

%description devel -l pl
Pliki nag³ówkowe biblioteki HAL.

%package libs
Summary:	HAL library
Summary(pl):	Biblioteka HAL
Group:		Libraries
Requires:	dbus-libs

%description libs
HAL library.

%description libs -l pl
Biblioteka HAL

%package static
Summary:	Static HAL library
Summary(pl):	Statyczna biblioteka HAL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static HAL library.

%description static -l pl
Statyczna biblioteka HAL.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--enable-doxygen-docs \
	--enable-docbook-docs \
	--enable-fstab-sync \
	--enable-selinux \
	--enable-hotplug-map \
	--with-hwdata=/etc

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} \
	$RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_desktopdir},/var/run/hald}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install examples/volumed/*.py $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

find $RPM_BUILD_ROOT%{_datadir}/hal/device-manager -name "*.py" -exec rm -f {} \;

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/haldaemon
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}

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

if [ -f /var/lock/subsys/messagebus ]; then
	/etc/rc.d/init.d/messagebus restart 1>&2
fi

%preun
if [ "$1" = "0" ];then
	if [ -f /var/lock/subsys/haldaemon ]; then
		/etc/rc.d/init.d/haldaemon stop >&2
	fi
	/sbin/chkconfig --del haldaemon
fi
	
%postun
if [ -f /var/lock/subsys/messagebus ]; then
	/etc/rc.d/init.d/messagebus restart 1>&2
fi
	
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README doc/TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
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
%dir %{_datadir}/%{name}/device-manager
%{_datadir}/%{name}/device-manager/*.py[co]
%{_datadir}/%{name}/device-manager/*.png
%{_datadir}/%{name}/device-manager/*.glade
%attr(755,root,root) %{_datadir}/%{name}/device-manager/hal-device-manager
%{_desktopdir}/*.desktop
%{_examplesdir}/%{name}-%{version}
%dir /var/lib/hal
%dir /var/run/hald

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/%{name}
%{_pkgconfigdir}/*.pc

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
