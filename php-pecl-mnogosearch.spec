%define		_modname	mnogosearch
%define		_status		alpha
Summary:	%{_modname} - mnoGoSearch extension module for PHP
Summary(pl.UTF-8):   %{_modname} - moduł mnoGoSearch dla PHP
Name:		php-pecl-%{_modname}
Version:	1.0.0
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	07fa9afd0c6fa4a3772f84a0eb4f1965
URL:		http://pecl.php.net/package/mnogosearch/
BuildRequires:	mnogosearch-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Obsoletes:	php-mnogosearch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Until PHP 5.1.0, this package was bundled in PHP.

This extension is a complete PHP binding for the mnoGoSearch API. For
details please see to http://www.mnogosearch.org/ or the manual.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
Do wersji PHP 5.1.0, to rozszerzenie było częścią PHP.

Rozszerzenie to jest kompletnym zestawem dowiązań PHP do API
mnoGoSearch. Dokładne informacje dostępne są pod adresem
http://www.mnogosearch.org/ lub w podręczniku.

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
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	-C %{_modname}-%{version} \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
