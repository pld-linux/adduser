# TODO:
# - finish it...
Summary:	Script for easy adding users
Summary(pl.UTF-8):	Skrypt do prostego dodawania użytkowników
Name:		adduser
Version:	3.156
Release:	0.1
License:	GPL v2+
Group:		Applications/System
Source0:	http://deb.debian.org/debian/pool/main/a/adduser/%{name}_%{version}.tar.xz
# Source0-md5:	1f7c7f194f080f6ee18af157cf5ac413
Patch0:		%{name}-po.patch
URL:		https://salsa.debian.org/debian/adduser
BuildRequires:	gettext-tools
BuildRequires:	po4a
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.745
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	bash >= 2.0
Requires:	shadow
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
%setup -q -c
%patch -P0 -p0

%build
# see debian/rules
install -d build
for f in adduser deluser ; do
	%{__sed} -e 's/DVERSION/%{version}/' "work/$f" > "build/$f"
done
for f in work/*.pm ; do
	%{__sed} -e 's/DVERSION/%{version}/' "$f" > "build/$(basename "$f")"
done

for f in work/po/*.po ; do msgfmt -c -v -o "build/$(basename "$f" .po).mo" "$f" ; done

install -d build/po4a
po4a --keep 60 --previous work/doc/po4a/po4a.conf --destdir build/po4a --srcdir work/doc/po4a

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir},%{_mandir}/man{5,8},%{perl_vendorlib}/Debian,/var/cache/adduser}

install build/{adduser,deluser} $RPM_BUILD_ROOT%{_sbindir}
ln -sf adduser $RPM_BUILD_ROOT%{_sbindir}/addgroup
ln -sf deluser $RPM_BUILD_ROOT%{_sbindir}/delgroup
cp -p build/*.pm $RPM_BUILD_ROOT%{perl_vendorlib}/Debian

for f in build/*.mo ; do
	lang="$(basename "$f" .mo)"
	install -d $RPM_BUILD_ROOT%{_localedir}/${lang}/LC_MESSAGES
	cp -p "$f" $RPM_BUILD_ROOT%{_localedir}/${lang}/LC_MESSAGES/adduser.mo
done

cp -p work/{adduser,deluser}.conf $RPM_BUILD_ROOT%{_sysconfdir}
cp -p work/doc/*.5 $RPM_BUILD_ROOT%{_mandir}/man5
cp -p work/doc/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
echo '.so adduser.8' >$RPM_BUILD_ROOT%{_mandir}/man8/addgroup.8
echo '.so deluser.8' >$RPM_BUILD_ROOT%{_mandir}/man8/delgroup.8
for f in build/*.[58] ; do
	bn=$(basename "$f")
	sect=$(echo "$bn" | sed -e 's/.*\.\([0-9]\)$/\1/')
	bn=$(basename "$bn" .${sect})
	lang=$(echo "$bn" | sed -e 's/.*\.\([a-zA-Z_]\+\)$/\1/')
	bn=$(basename "$bn" .${lang})
	install -d $RPM_BUILD_ROOT%{_mandir}/${lang}/man${sect}
	cp -p "$f" $RPM_BUILD_ROOT%{_mandir}/${lang}/man${sect}/${bn}.${sect}
	if [ "$bn" = "adduser" ]; then
		echo ".so adduser.8" >$RPM_BUILD_ROOT%{_mandir}/${lang}/man${sect}/addgroup.${sect}
	elif [ "$bn" = "deluser" ]; then
		echo ".so deluser.8" >$RPM_BUILD_ROOT%{_mandir}/${lang}/man${sect}/delgroup.${sect}
	fi
done

# tool not packaged
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man8/adduser.local.8
%{__rm} $RPM_BUILD_ROOT%{_mandir}/*/man8/adduser.local.8

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc work/debian/{NEWS,README,TODO,changelog,copyright}
%attr(755,root,root) %{_sbindir}/addgroup
%attr(755,root,root) %{_sbindir}/adduser
%attr(755,root,root) %{_sbindir}/delgroup
%attr(755,root,root) %{_sbindir}/deluser

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/adduser.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/deluser.conf
%dir /var/cache/adduser

%dir %{perl_vendorlib}/Debian
%{perl_vendorlib}/Debian/Adduser*.pm

%{_mandir}/man5/adduser.conf.5*
%{_mandir}/man5/deluser.conf.5*
%{_mandir}/man8/addgroup.8*
%{_mandir}/man8/adduser.8*
%{_mandir}/man8/delgroup.8*
%{_mandir}/man8/deluser.8*
%lang(da) %{_mandir}/da/man5/*.conf.5*
%lang(de) %{_mandir}/de/man5/*.conf.5*
%lang(es) %{_mandir}/es/man5/*.conf.5*
%lang(fr) %{_mandir}/fr/man5/*.conf.5*
%lang(it) %{_mandir}/it/man5/*.conf.5*
%lang(nl) %{_mandir}/nl/man5/*.conf.5*
%lang(pl) %{_mandir}/pl/man5/*.conf.5*
%lang(pt) %{_mandir}/pt/man5/*.conf.5*
%lang(pt_BR) %{_mandir}/pt_BR/man5/*.conf.5*
%lang(ro) %{_mandir}/ro/man5/*.conf.5*
%lang(ru) %{_mandir}/ru/man5/*.conf.5*
%lang(sv) %{_mandir}/sv/man5/*.conf.5*
%lang(de) %{_mandir}/de/man8/*.8*
%lang(fr) %{_mandir}/fr/man8/*.8*
%lang(nl) %{_mandir}/nl/man8/*.8*
%lang(pt) %{_mandir}/pt/man8/*.8*
%lang(pt_BR) %{_mandir}/pt_BR/man8/*.8*
%lang(ro) %{_mandir}/ro/man8/*.8*
%lang(sv) %{_mandir}/sv/man8/*.8*
