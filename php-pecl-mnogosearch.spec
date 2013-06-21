%define		php_name	php%{?php_suffix}
%define		modname	mnogosearch
%define		status		alpha
Summary:	%{modname} - mnoGoSearch extension module for PHP
Summary(pl.UTF-8):	%{modname} - moduł mnoGoSearch dla PHP
Name:		%{php_name}-pecl-%{modname}
# extension has no version yet (defiend as NO_VERSION_YET), keep it last pecl release
Version:	1.0.0
Release:	6
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://www.mnogosearch.org/Download/mnogosearch-3.3.9.tar.gz
# Source0-md5:	18d3e6c6cca3f816d05d04bd3943ed6a
URL:		http://pecl.php.net/package/mnogosearch/
BuildRequires:	mnogosearch-devel
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
Provides:	php-mnogosearch = %{version}-%{release}
Obsoletes:	php-mnogosearch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension is a complete PHP binding for the mnoGoSearch API. For
details please see to <http://www.mnogosearch.org/> or the manual.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Rozszerzenie to jest kompletnym zestawem dowiązań PHP do API
mnoGoSearch. Dokładne informacje dostępne są pod adresem
<http://www.mnogosearch.org/> lub w podręczniku.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv mnogosearch-*/php/* .

%build
phpize
%configure \
	--with-mnogosearch=shared,/usr
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT

cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
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
%doc CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
