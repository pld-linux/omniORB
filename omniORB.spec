# TODO:
#  - python stuff is wrong
#  - move some binaries from main to devel (main should only contain server)
#  - ditto for documentation
#  - logrotate script
#  - enable openssl
Summary:	Object Request Broker (ORB) from AT&T (CORBA 2.6)
Summary(pl):	Object Request Broker (ORB) z AT&T (CORBA 2.6)
Name:		omniORB
Version:	4.0.0
Release:	0.1
License:	GPL/LGPL
Group:		Libraries
Source0:	http://telia.dl.sourceforge.net/omniorb/%{name}-%{version}.tar.gz
# Source0-md5: c5dbd122c992ea1df4f6adf5e72644b1
Source1:	%{name}.init
URL:		http://omniorb.sf.net/
Requires:	%{name}-libs = %{version}-%{release}
Requires(post,preun):	/sbin/chkconfig
BuildRequires:	gcc-c++
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
omniORB is an Object Request Broker (ORB) which implements
specification 2.6 of the Common Object Request Broker Architecture
(CORBA).

%description -l pl
omniORB implementuje wersjê 2.6 specyfikacji CORBA.

%package devel
Summary:	Development files for %{name}
Summary(pl):	Pliki potrzebne do tworzenia aplikacji z u¿yciem %{name}
Requires:	%{name} = %{version}-%{release}
Group:		Development/Libraries

%description devel
Development files for %{name}.

%description devel -l pl
Pliki potrzebne do tworzenia aplikacji z u¿yciem %{name}.

%package libs
Summary:	Shared libraries for %{name}
Summary(pl):	Dzielone biblioteki dla aplikacji korzystaj±cych z %{name}
Group:		Libraries

%description libs
Shared libraries for %{name}.

%description libs -l pl
Dzielone biblioteki dla aplikacji korzystaj±cych z %{name}.

%package static
Summary:	Static files for %{name}
Summary(pl):	Statyczne biblioteki dla %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static files for %{name}.

%description static -l pl
Statyczne biblioteki dla %{name}.

%prep
%setup -q

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure --with-omniNames-logdir=/var/log/%{name}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man1,%{_sysconfdir}/rc.d/init.d,/var/log/%{name}}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install man/man1/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
install sample.cfg $RPM_BUILD_ROOT%{_sysconfdir}/omniORB.cfg
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post 
/sbin/chkconfig --add sensors
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
%doc ReleaseNotes_%{version}.txt CREDITS README.{FIRST,unix}
%attr(755,root,root) %{_bindir}/*
%dir /var/log/%{name}
%attr(755,root,root) %{_sysconfdir}/rc.d/init.d/*
%{_sysconfdir}/%{name}.cfg
%{_mandir}/man1/*
%attr(755,root,root) %{_libdir}/python*/site-packages/*.so*
%{_libdir}/python*/site-packages/omniidl
%{_libdir}/python*/site-packages/omniidl_be

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so.*

%files static
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.a

%files devel
%defattr(644,root,root,755)
%doc doc/*.html doc/omniORB
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/*
%{_datadir}/idl/%{name}
