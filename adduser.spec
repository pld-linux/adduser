Summary:     Script for easy adding users
Summary(pl): Skrypt do prostego dodawania u¿ytkowników
Name:        adduser
Version:     1.06
Release:     2
Copyright:   GPL
Source:      %{name}-%{version}.tar.gz
Group:       Utilities/System
Group(pl):   Narzêdzia/System
Requires:    shadow
Obsoletes:   etcskel
Provides:    etcskel
BuildArch:   noarch
BuildRoot:	/tmp/%{name}-%{version}-root

%description
Interactive shell script for easy adding new users to the system.
Package contains files copied to new users home directories.

%description -l pl
Skrypt shella pozwalaj±cy interaktywnie dodawaæ nowych u¿ytkowników
do systemu. Pakiet zawiera pliki kopiowane do katalogów domowych
nowych u¿ytkowników.

%prep
%setup -q -n %{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/usr/{sbin,share/locale/pl/LC_MESSAGES} \
	$RPM_BUILD_ROOT/etc/{skel,adduser.d,default/public_html/{pl,en}}

install adduser $RPM_BUILD_ROOT%{_sbindir}
install adduser.conf $RPM_BUILD_ROOT/etc/default/adduser

cp -R etcskel/. $RPM_BUILD_ROOT/etc/skel

for lang in pl en; do
  cp -R etcskel/$lang/public_html/* $RPM_BUILD_ROOT/etc/default/public_html/$lang
  rm -rf $RPM_BUILD_ROOT/etc/skel/$lang/public_html
done
ln -sf en $RPM_BUILD_ROOT/etc/skel/default
msgfmt po/pl.po -o $RPM_BUILD_ROOT%{_datadir}/locale/pl/LC_MESSAGES/adduser.mo

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(700,root,root) %{_sbindir}/*

%lang(pl) %{_datadir}/locale/pl/LC_MESSAGES/adduser.mo

%attr(750,root,root) %dir /etc/adduser.d
%attr(700,root,root) %dir /etc/skel/C
%attr(700,root,root) %dir %lang(pl) /etc/skel/pl
%attr(700,root,root) %dir %lang(en) /etc/skel/en

%attr(640,root,root) %config %verify(not size mtime md5) /etc/default/adduser
%attr(600,root,root) %config %verify(not size mtime md5) /etc/skel/C/*
%attr(600,root,root) %config %verify(not size mtime md5) %lang(pl) /etc/skel/pl/*
%attr(600,root,root) %config %verify(not size mtime md5) %lang(en) /etc/skel/en/*
%verify(not link) /etc/skel/default

%dir /etc/default/public_html
%config %verify(not size mtime md5) /etc/default/public_html/*

%changelog
* Tue Apr 20 1999 Piotr Czerwiñski <pius@pld.org.pl>
  [1.06-2]
- recompiled on rpm 3,
- cosmetics.

* Sun Mar 28 1999 Marek Obuchowicz <elephant@pld.org.pl>
  [1.06-1]
- corrected some quota-setting errors

* Fri Mar 2 1999 Marek Obuchowicz <elephant@shadow.eu.org>
  [1.04-1d]
- international /etc/skel support
- removed .screenrc from skeleton files
- first CVSed release
- updated default home page :)
- default quota support
- command line argument parsing and help
- /etc/adduser.d support

* Mon Dec 20 1998 Marek Obuchowicz <elephant@shadow.eu.org>
  [1.03-1d]
- TMPDIR and .todo support added to /etc/skel/.bash* files

* Sat Dec 19 1998 Marek Obuchowicz <elephant@shadow.eu.org>
  [1.02-1d]
- Updated to newest release
- "not-only-for-polish" release

* Thu Oct 13 1998 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
  [1.01-1d]
- added internationalization
- few fixes

* Sat Oct 10 1998 Marek Obuchowicz <elephant@shadow.eu.org>
  [1-1d]
- first release of packege for Polish Linux Distribution
