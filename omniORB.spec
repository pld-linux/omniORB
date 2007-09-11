# TODO:
#  - ditto for documentation
Summary:	Object Request Broker (ORB) from AT&T (CORBA 2.6)
Summary(pl.UTF-8):	Object Request Broker (ORB) z AT&T (CORBA 2.6)
Name:		omniORB
Version:	4.1.0
Release:	2
License:	GPL/LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/omniorb/%{name}-%{version}.tar.gz
# Source0-md5:	b52dcb1886ffa2a61e6ed56e462edb76
Source1:	%{name}.init
Source2:	%{name}.logrotate
Source3:	%{name}.sysconfig
URL:		http://omniorb.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pkgconfig
BuildRequires:	python
BuildRequires:	python-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Conflicts:	logrotate < 3.7-4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
omniORB is an Object Request Broker (ORB) which implements
specification 2.6 of the Common Object Request Broker Architecture
(CORBA).

%description -l pl.UTF-8
omniORB implementuje wersję 2.6 specyfikacji CORBA.

%package libs
Summary:	Shared libraries for %{name}
Summary(pl.UTF-8):	Dzielone biblioteki dla aplikacji korzystających z %{name}
Group:		Libraries

%description libs
Shared libraries for %{name}.

%description libs -l pl.UTF-8
Dzielone biblioteki dla aplikacji korzystających z %{name}.

%package devel
Summary:	Development files for %{name}
Summary(pl.UTF-8):	Pliki potrzebne do tworzenia aplikacji z użyciem %{name}
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Development files for %{name}.

%description devel -l pl.UTF-8
Pliki potrzebne do tworzenia aplikacji z użyciem %{name}.

%package static
Summary:	Static files for %{name}
Summary(pl.UTF-8):	Statyczne biblioteki dla %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static files for %{name}.

%description static -l pl.UTF-8
Statyczne biblioteki dla %{name}.

%package python
Summary:	Python bindings for %{name}
Summary(pl.UTF-8):	Wiązania Pythona dla %{name}
Group:		Development/Libraries
%pyrequires_eq	python-libs
Requires:	%{name}-libs = %{version}-%{release}

%description python
Python bindings for %{name}. Besides, package includes idl compiler -
omniidl.

%description python -l pl.UTF-8
Wiązania Pythona dla %{name}. Ponadto pakiet zawiera kompilator idl -
omniidl.

%package utils
Summary:	Additional utilities for %{name}
Summary(pl.UTF-8):	Dodatkowe narzędzia dla %{name}
Group:		Development/Tools
Requires:	%{name}-libs = %{version}-%{release}

%description utils
Additional utilities for %{name}.

%description utils -l pl.UTF-8
Dodatkowe narzędzia dla %{name}.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure \
	--with-omniNames-logdir=/var/log/%{name} \
	--with-openssl=/usr/%{_lib}

%{__make} \
	SUBDIR_MAKEFLAGS='CDEBUGFLAGS="%{rpmcflags}" CXXDEBUGFLAGS="%{rpmcflags}"'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man1,/etc/{logrotate.d,rc.d/init.d,sysconfig},/var/log/{,archive/}%{name}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install man/man1/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
install sample.cfg $RPM_BUILD_ROOT%{_sysconfdir}/omniORB.cfg
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

touch $RPM_BUILD_ROOT/var/log/%{name}/omninames-err.log

# rpmdeps doesn't generate ELF deps for non-executable .so
chmod 755 $RPM_BUILD_ROOT%{_libdir}/lib*.so.*.*

rm -f $RPM_BUILD_ROOT%{_bindir}/omniidlrun.py
find $RPM_BUILD_ROOT%{py_sitescriptdir} -name \*py -exec rm -f \{\} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart >&2
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start %{name} daemon." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop >&2
	fi
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc ReleaseNotes.txt CREDITS README.{FIRST.txt,unix}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.cfg
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(755,root,root) %{_bindir}/omniMapper
%attr(755,root,root) %{_bindir}/omniNames
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(750,root,root) %dir /var/log/%{name}
%attr(750,root,root) %dir /var/log/archive/%{name}
%attr(640,root,root) %ghost /var/log/%{name}/*
%{_mandir}/man1/omniNames*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%ghost %{_libdir}/lib*.so.1
%ghost %{_libdir}/lib*.so.3
%{_datadir}/idl/%{name}

%files devel
%defattr(644,root,root,755)
%doc doc/*.html doc/omniORB
%attr(755,root,root) %{_bindir}/omkdepend
%attr(755,root,root) %{_bindir}/omnicpp
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files python
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/omniidl
%attr(755,root,root) %{py_sitedir}/*.so*
%{py_sitescriptdir}/omniidl
%{py_sitescriptdir}/omniidl_be
%{_mandir}/man1/omniidl*

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/catior
%attr(755,root,root) %{_bindir}/convertior
%attr(755,root,root) %{_bindir}/genior
%attr(755,root,root) %{_bindir}/nameclt
%{_mandir}/man1/catior*
%{_mandir}/man1/genior*
%{_mandir}/man1/nameclt*
