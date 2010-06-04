# TODO:
# - finish it...
Summary:	Script for easy adding users
Summary(pl.UTF-8):	Skrypt do prostego dodawania użytkowników
Name:		adduser
Version:	3.110
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	ftp://ftp.debian.org/debian/pool/main/a/adduser/%{name}_%{version}.tar.gz
# Source0-md5:	826832470e042eedeff7219071c40743
URL:		http://alioth.debian.org/projects/adduser/
BuildRequires:	gettext-devel
Requires:	bash >= 2.0
Requires:	shadow
Provides:	etcskel
Obsoletes:	etcskel
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Interactive shell script for easy adding new users to the system.
Package contains files copied to new users home directories.

%description -l pl.UTF-8
Skrypt shella pozwalający interaktywnie dodawać nowych użytkowników do
systemu. Pakiet zawiera pliki kopiowane do katalogów domowych nowych
użytkowników.

%prep
%setup -q -n trunk

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

%dir %{_sysconfdir}/adduser.d
%dir /etc/skel/C
%dir %lang(pl) /etc/skel/pl
%dir /etc/skel/en

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/default/adduser
%config(noreplace) %verify(not md5 mtime size) /etc/skel/C/*
%config(noreplace) %verify(not md5 mtime size) /etc/skel/C/.[a-zA-Z0-9]*
#%config(noreplace) %verify(not size mtime md5) %lang(pl) /etc/skel/pl/*
%config(noreplace) %verify(not md5 mtime size) %lang(pl) /etc/skel/pl/.[a-zA-Z0-9]*
#%config(noreplace) %verify(not size mtime md5) /etc/skel/en/*
%config(noreplace) %verify(not md5 mtime size) /etc/skel/en/.[a-zA-Z0-9]*
%config(noreplace) %verify(not link) /etc/skel/default

%dir %{_sysconfdir}/default/public_html
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/default/public_html/*
