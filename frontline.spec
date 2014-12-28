#
# Conditional build:
%bcond_with	gimp	# build GIMP (1.2.x only) plugin
#
Summary:	GUI FRONT end for autotrace that extracts outLINE from images
Summary(pl.UTF-8):	Graficzny interfejs do autotrace wyciągającego obrysy z obrazków
Name:		frontline
Version:	0.5.4
Release:	12
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://dl.sourceforge.net/autotrace/%{name}-%{version}.tar.gz
# Source0-md5:	5fc2c3459b153dbc2b3138c1133f927e
Patch0:		%{name}-shared.patch
Patch1:		%{name}-desktop.patch
URL:		http://autotrace.sourceforge.net/frontline/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	autotrace-devel >= 0.31.1
BuildRequires:	gettext-tools
%{?with_gimp:BuildRequires:	gimp-devel >= 1:1.2.1}
%{?with_gimp:BuildRequires:	gimp-devel < 1.3}
BuildRequires:	gnome-libs-devel >= 1.4.0
BuildRequires:	imlib-devel >= 1.8.2
BuildRequires:	libart_lgpl >= 2.3.8
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{with gimp}
%define		gimpplugindir	%(gimptool --gimpplugindir)
%endif

%description
Frontline provides a GTK+/GNOME based GUI front end for autotrace
(http://autotrace.sourceforge.net/). This package contains the
`frontline' command, which runs as a stand alone program. It will work
well with GNOME desktop and nautilus.

%description -l pl.UTF-8
Frontline udostępnia oparty na GTK+/GNOME graficzny interfejs do
autotrace (http://autotrace.sourceforge.net/). Ten pakiet zawiera
polecenie "frontline", działające jako samodzielny program. Działa
dobrze z pulpitem GNOME i nautilusem.

%package libs
Summary:	Frontline shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone Frontline
Group:		X11/Libraries

%description libs
This package contains Frontline shared libraries, used by all versions
of Frontline GUI.

%description libs -l pl.UTF-8
Ten program zawiera biblioteki współdzielone Frontline, używane przez
wszystkie wersje interfejsu Frontline.

%package devel
Summary:	Frontline development files
Summary(pl.UTF-8):	Pliki dla programistów używających Frontline
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Frontline development files.

%description devel -l pl.UTF-8
Pliki dla programistów używających Frontline.

%package static
Summary:	Frontline static libraries
Summary(pl.UTF-8):	Biblioteki statyczne Frontline
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Frontline static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne Frontline.

%package -n gimp-plugin-frontline
Summary:	GIMP Frontline plugin
Summary(pl.UTF-8):	Wtyczka Frontline dla GIMPa
Group:		X11/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description -n gimp-plugin-frontline
GIMP frontline plugin - you can launch frontline from the GIMP menu.

%description -n gimp-plugin-frontline -l pl.UTF-8
Wtyczka frontline dla GIMPa - pozwala na uruchomienie frontline z menu
GIMPa.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{!?with_gimp:echo 'AC_DEFUN([AM_PATH_GIMP],[$3])' >> acinclude.m4}
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I %{_aclocaldir}/gnome
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	Graphicsdir=%{_desktopdir} \
	m4datadir=%{_aclocaldir} \
	pkgconfigdir=%{_pkgconfigdir}

for f in CHANGES README TODO ; do
	mv -f gundo/$f ${f}.gundo
done

rm -rf $RPM_BUILD_ROOT%{_datadir}/mime-info

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/frontline

%{_desktopdir}/*.desktop

%files libs -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README TODO {CHANGES,README,TODO}.gundo
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_pixmapsdir}/*.png

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/frontline-config
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/frontline
%{_includedir}/gundo
%{_aclocaldir}/frontline.m4
%{_pkgconfigdir}/frontline.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%if %{with gimp}
%files -n gimp-plugin-frontline
%defattr(644,root,root,755)
%attr(755,root,root) %{gimpplugindir}/plug-ins/trace
%endif
