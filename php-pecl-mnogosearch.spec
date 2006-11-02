%define		_modname	mnogosearch
%define		_status		alpha
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

Summary:	%{_modname} - mnoGoSearch extension module for PHP
Summary(pl):	%{_modname} - modu³ mnoGoSearch dla PHP
Name:		php-pecl-%{_modname}
Version:	1.0.0
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	07fa9afd0c6fa4a3772f84a0eb4f1965
URL:		http://pecl.php.net/package/mnogosearch/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.322
%{?requires_php_extension}
Requires:	%{_sysconfdir}/conf.d
Obsoletes:	php-mnogosearch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Until PHP 5.1.0, this package was bundled in PHP.

This extension is a complete PHP binding for the mnoGoSearch API. For
details please see to http://www.mnogosearch.org/ or the manual.

In PECL status of this extension is: %{_status}.

%description -l pl
Do wersji PHP 5.1.0, to rozszerzenie by³o czê¶ci± PHP.

Rozszerzenie to jest kompletnym zestawem dowi±zañ PHP do API
mnoGoSearch. Dok³adne informacje dostêpne s± pod adresem
http://www.mnogosearch.org/ lub w podrêczniku.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure \
	--with-mnogosearch=shared,/usr
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/conf.d

%{__make} install \
	-C %{_modname}-%{version} \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{extensionsdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
