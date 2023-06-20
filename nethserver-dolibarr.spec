Summary: nethserver-dolibarr  is a CRM
%define name nethserver-dolibarr
Name: %{name}
%define version 17.0.2
# we must stick to dolibarr version
# please increment version
%define release 1
Version: %{version}
Release: %{release}%{?dist}
License: GPL
Group: Networking/Daemons
Source: %{name}-%{version}.tar.gz
Source1: https://github.com/Dolibarr/dolibarr/archive/%{version}.tar.gz

BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
Requires: nethserver-mysql
Requires: nethserver-rh-php73-php-fpm
Obsoletes: dolibarr

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
sed -i 's/_RELEASE_/%{version}/' %{name}.json

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

# Temp directory
mkdir -p %{buildroot}/usr/share/dolibarr/documents
mkdir -p %{buildroot}/usr/share/dolibarr/documents/bank
mkdir -p %{buildroot}/usr/share/dolibarr/htdocs/custom
tar xzvf %{SOURCE1}
cp -r dolibarr-%{version}/* %{buildroot}%{_datadir}/dolibarr

%post

%postun
if [ $1 == 0 ] ; then
    /usr/bin/rm -f /etc/httpd/conf.d/zzz_dolibarr.conf
    /usr/bin/systemctl reload httpd
fi

%clean 
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update
%doc COPYING
%config(noreplace) %attr(0600,apache,apache) /usr/share/dolibarr/htdocs/conf/conf.php
%config(noreplace) %attr(0700,root,root) /etc/cron.daily/dolibarr
%{_datadir}/dolibarr
%dir %attr(0750,apache,apache) %{_datadir}/dolibarr/documents
%dir %attr(0750,apache,apache) %{_datadir}/dolibarr/documents/bank
%dir %attr(0750,apache,apache) %{_datadir}/dolibarr/htdocs/custom

%changelog
* Tue Jun 20 2023 stephane de Labrusse <stephdl@de-labrusse.fr>
- Bump to 17.0.2
* Tue Apr 4 2023 stephane de Labrusse <stephdl@de-labrusse.fr>
- Bump to 17.0.1

* Wed Dec 21 2022 stephane de Labrusse <stephdl@de-labrusse.fr>
- Add date in log install and do not overwrite logs
- test if the webserver is available before to launch database upgrade
- Bump to 16.0.3

* Tue Aug 9 2022 stephane de Labrusse <stephdl@de-labrusse.fr>
- Bump to 15.0.2

* Sat Apr 2 2022 stephane de Labrusse <stephdl@de-labrusse.fr>
- Bump to 15.0.1

* Fri Dec 24 2021 stephane de Labrusse <stephdl@de-labrusse.fr>
- Bump to 14.0.4

* Thu Oct 21 2021  stephane de Labrusse <stephdl@de-labrusse.fr>
- Add good permissions to apache for /usr/share/dolibarr/htdocs/conf/conf.php

* Thu Sep 30 2021  stephane de Labrusse <stephdl@de-labrusse.fr>
- One rpm to tule dolibarr

* Wed Sep 22 2021  stephane de Labrusse <stephdl@de-labrusse.fr>
- Bump to 14.0.2

* Tue Aug 10 2021 stephane de Labrusse <stephdl@de-labrusse.fr>
- Bump to 13.0.4

* Fri Jul 2 2021 stephane de Labrusse <stephdl@de-labrusse.fr>
- Bump to 13.0.3

* Thu Apr 23 2021 stephane de Labrusse <stephdl@de-labrusse.fr>
- Upstream upgrade to 13.0.2
- Adapt mysql script migration for major version

* Thu Jan 14 2021 stephane de Labrusse <stephdl@de-labrusse.fr>
- Upstream upgrade to 12.0.4

* Thu Nov 19 2020  stephane de Labrusse <stephdl@de-labrusse.fr> 12.0.3-3
- Remove the trailling / of linux fpm socket

* Thu Nov 05 2020 stephane de Labrusse <stephdl@de-labrusse.fr>
- Upstream upgrade to 12.0.3

* Tue Aug 04 2020 stephane de Labrusse <stephdl@de-labrusse.fr>
- Upstream upgrade to 12.0.1

* Sat Jul 04 2020 stephane de Labrusse <stephdl@de-labrusse.fr> 0.0.11
- Remove http templates after rpm removal

* Sat May 09 2020 stephane de labrusse  <stephdl@de-labrusse.fr> 0.0.10
- Fix SSL redirection
- Fix Nethgui application link

* Fri May 01 2020  stephane de labrusse  <stephdl@de-labrusse.fr> 0.0.9
- Vhost is possible in cockpit and nethgui applications

* Thu Apr 30 2020 stephane de labrusse  <stephdl@de-labrusse.fr> 0.0.8
- dolibarr can use a virtualhost

* Sun Apr 26 2020 stephane de labrusse  <stephdl@de-labrusse.fr> 0.0.7
- removed string from bareos 

* Sat Apr 18 2020 stephane de Labrusse <stephdl@de-labrusse.fr> 0.0.6
- Fix the url_root 

* Sat Apr 18 2020 stephane de Labrusse <stephdl@de-labrusse.fr> 0.0.5
- Ldap integration (openldap & samba AD)
- Backup of mysql DB  by cron.daily
- Version is displayed in cockpit application
- Backup-data of /usr/share/dolibarr/documents

* Wed Apr 15 2020 stephane de Labrusse <stephdl@de-labrusse.fr> 0.0.3
- Move backup of DB to /var/lib/nethserver 

* Mon Apr 13 2020 stephane de Labrusse <stephdl@de-labrusse.fr> 0.0.1
- initial
