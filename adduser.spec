Summary:	Script for easy adding users
Summary(pl):	Skrypt do prostego dodawania u¿ytkowników
Name:		adduser
Version:	1.06
Release:	2
License:	GPL
Source0:	%{name}-%{version}.tar.gz
Group:		Applications/System
Requires:	bash >= 2.0
Requires:	shadow
BuildRequires:	gettext-devel
Obsoletes:	etcskel
Provides:	etcskel
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Interactive shell script for easy adding new users to the system.
Package contains files copied to new users home directories.

%description -l pl
Skrypt shella pozwalaj±cy interaktywnie dodawaæ nowych u¿ytkowników do
systemu. Pakiet zawiera pliki kopiowane do katalogów domowych nowych
u¿ytkowników.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_datadir}/locale/pl/LC_MESSAGES} \
$RPM_BUILD_ROOT%{_sysconfdir}/{skel,adduser.d,default/public_html/{pl,en}}

install adduser $RPM_BUILD_ROOT%{_sbindir}
install adduser.conf $RPM_BUILD_ROOT%{_sysconfdir}/default/adduser

cp -R etcskel/. $RPM_BUILD_ROOT/etc/skel

for lang in pl en; do
cp -R etcskel/$lang/public_html/* $RPM_BUILD_ROOT%{_sysconfdir}/default/public_html/$lang
  rm -rf $RPM_BUILD_ROOT/etc/skel/$lang/public_html
done
ln -sf en $RPM_BUILD_ROOT/etc/skel/default
msgfmt po/pl.po -o $RPM_BUILD_ROOT%{_datadir}/locale/pl/LC_MESSAGES/adduser.mo

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*

%attr(755,root,root) %dir %{_sysconfdir}/adduser.d
%attr(755,root,root) %dir /etc/skel/C
%attr(755,root,root) %dir %lang(pl) /etc/skel/pl
%attr(755,root,root) %dir %lang(en) /etc/skel/en

%config %verify(not size mtime md5) %{_sysconfdir}/default/adduser
%config %verify(not size mtime md5) /etc/skel/C/*
%config %verify(not size mtime md5) /etc/skel/C/.[a-zA-Z0-9]*
#%config %verify(not size mtime md5) %lang(pl) /etc/skel/pl/*
%config %verify(not size mtime md5) %lang(pl) /etc/skel/pl/.[a-zA-Z0-9]*
#%config %verify(not size mtime md5) %lang(en) /etc/skel/en/*
%config %verify(not size mtime md5) %lang(en) /etc/skel/en/.[a-zA-Z0-9]*
%verify(not link) /etc/skel/default

%dir %{_sysconfdir}/default/public_html
%config %verify(not size mtime md5) %{_sysconfdir}/default/public_html/*
