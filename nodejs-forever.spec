%define		pkg	forever
Summary:	node.js forever module and CLI tools
Name:		nodejs-%{pkg}
Version:	0.10.0
Release:	0.8
License:	MIT
Group:		Development/Libraries
URL:		https://github.com/nodejitsu/forever
Source0:	http://registry.npmjs.org/forever/-/%{pkg}-%{version}.tgz
# Source0-md5:	f17e356a9550e56e11b7b19e122145b8
BuildRequires:	npm
BuildRequires:	rpmbuild(macros) >= 1.634
BuildRequires:	sed >= 4.0
Requires:	nodejs
Requires:	nodejs-cliff >= 0.1.8
Requires:	nodejs-flatiron >= 0.2.3
Requires:	nodejs-forever-monitor >= 1.0.1
Requires:	nodejs-nconf >= 0.6.1
Requires:	nodejs-nssocket >= 0.3.8
Requires:	nodejs-optimist >= 0.3.4
Requires:	nodejs-pkginfo >= 0.2.3
Requires:	nodejs-timespan >= 2.0.1
Requires:	nodejs-utile >= 0.1.2
Requires:	nodejs-watch >= 0.5.1
Requires:	nodejs-winston >= 0.6.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A simple CLI tool for ensuring that a given script runs continuously
(i.e. forever).

%prep
%setup -qc
mv package/* .

# fix shebangs
%{__sed} -i -e '1s,^#!.*node,#!/usr/bin/node,' bin/*

# you'll need this if you cp -a complete dir in source
# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
# install others local
npm install .

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{nodejs_libdir}/%{pkg},%{_bindir},%{_sbindir}}
cp -pr lib bin package.json $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}

ln -s %{nodejs_libdir}/%{pkg}/bin/forever $RPM_BUILD_ROOT%{_bindir}/forever
ln -s %{nodejs_libdir}/%{pkg}/bin/foreverd $RPM_BUILD_ROOT%{_sbindir}/foreverd

# bundle node_modules
cp -a node_modules $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md LICENSE
%attr(755,root,root) %{_bindir}/forever
%attr(755,root,root) %{_sbindir}/foreverd
%dir %{nodejs_libdir}/%{pkg}
%{nodejs_libdir}/%{pkg}/package.json
%{nodejs_libdir}/%{pkg}/lib
%dir %{nodejs_libdir}/%{pkg}/bin
%attr(755,root,root) %{nodejs_libdir}/%{pkg}/bin/forever
%attr(755,root,root) %{nodejs_libdir}/%{pkg}/bin/foreverd
%attr(755,root,root) %{nodejs_libdir}/%{pkg}/bin/monitor

# bundle node_modules
%defattr(-,root,root,-)
%{nodejs_libdir}/%{pkg}/node_modules
