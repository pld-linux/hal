Summary:	HAL - Hardware Abstraction Layer
Summary(pl):	HAL - Abstrakcyjna Warstwa Dostêpu do Sprzêtu
Name:		hal
Version:	0.2
Release:	1
License:	AFL v2.0 or GPL v2
Group:		Libraries
Source0:	http://freedesktop.org/~david/%{name}-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a2b2bf6aedc9eb24828ccdcde429f0f7
Patch0:		%{name}-no_static.patch
URL:		http://freedesktop.org/Software/hal
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.20
BuildRequires:	expat-devel
BuildRequires:	glib2-devel >= 2.2.2
BuildRequires:	libtool
BuildRequires:	pciutils
Requires(post,postun):	/sbin/ldconfig
Requires:	dbus >= 0.20-2
Requires:	hotplug >= 2003_08_05
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
Requires:	%{name} = %{version}

%description devel
Header files for HAL library.

%description devel -l pl
Pliki nag³ówkowe biblioteki HAL.

%package static
Summary:	Static HAL library
Summary(pl):	Statyczna biblioteka HAL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static HAL library.

%description static -l pl
Statyczna biblioteka HAL.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-hwdata=/etc

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install examples/volumed/*.py $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

if [ -f /var/lock/subsys/messagebus ]; then
	/etc/rc.d/init.d/messagebus restart 1>&2
fi
	
%postun
/sbin/ldconfig

if [ -f /var/lock/subsys/messagebus ]; then
	/etc/rc.d/init.d/messagebus restart 1>&2
fi
	
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README doc/TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/hal.hotplug
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dbus*/system.d/*
%{_sysconfdir}/hotplug.d/default/*.hotplug
%{_datadir}/%{name}
%{_examplesdir}/%{name}-%{version}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/%{name}
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
