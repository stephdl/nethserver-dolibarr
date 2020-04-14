Summary: nethserver-dolibarr  is a CRM
%define name nethserver-dolibarr
Name: %{name}
%define version 0.0.2
%define release 1
Version: %{version}
Release: %{release}%{?dist}
License: GPL
Group: Networking/Daemons
Source: %{name}-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
Requires: nethserver-mysql
Requires: nethserver-rh-php73-php-fpm
Requires: dolibarr = 11.0.3

BuildRequires: nethserver-devtools
BuildArch: noarch

%description
Dolibarr ERP CRM is an open source, free software package for small and medium companies, 
foundations or freelancers. It includes different features for enterprise resource planning 
(ERP) and customer relationship management (CRM) but also other features for different activities.


%prep
%setup

%build
%{makedocs}
perl createlinks

%install
rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)

mkdir -p %{buildroot}/usr/share/cockpit/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/%{name}/
cp -a manifest.json %{buildroot}/usr/share/cockpit/%{name}/
cp -a logo.png %{buildroot}/usr/share/cockpit/%{name}/
cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/%{name}/

rm -f %{name}-%{version}-%{release}-filelist
%{genfilelist} $RPM_BUILD_ROOT \
> %{name}-%{version}-%{release}-filelist

%post

%postun

%clean 
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update
%doc COPYING
%config(noreplace) %attr(0600,apache,apache) /usr/share/dolibarr/htdocs/conf/conf.php


%changelog
* Mon May 13 2020 stephane de Labrusse <stephdl@de-labrusse.fr>
- initial
