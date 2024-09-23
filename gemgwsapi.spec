%define _prefix __auto__
%define gemopt opt
%define name gemgwsapi
%define version __auto__
%define release __auto__
%define repository gemini
%define debug_package %{nil}

Summary: %{name} Package: GWS API server for VSCADA
Name: %{name}
Version: %{version}
Release: %{release}.%{dist}.%{repository}
License: GPL
## Source:%{name}-%{version}.tar.gz
Group: Gemini
Source0: %{name}-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-%{version}-root
BuildArch: %{arch}
#Prefix: %{_prefix}
## You may specify dependencies here
BuildRequires: gemini-top
Requires: gemini-top python3 python3-pip
## Switch dependency checking off
# AutoReqProv: no

%description
Web server for GWS API. This API was created to serve the VSCADA used for PR control.

%prep
## Do some preparation stuff, e.g. unpacking the source with
%setup -n %{name}


%build
## Write build instructions here, e.g
# sh configure
# make

%install
## Write install instructions here, e.g
## install -D zzz/zzz  $RPM_BUILD_ROOT/%{_prefix}/zzz/zzz
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/system/
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/bin/
#mkdir -p $RPM_BUILD_ROOT/%{_prefix}/var/log/nuvuMon/
install -D -m 644 systemd/* $RPM_BUILD_ROOT/usr/lib/systemd/system/
install -D -m 755 scripts/* $RPM_BUILD_ROOT/%{_prefix}/bin/
#install -D -m 666 log/* $RPM_BUILD_ROOT/%{_prefix}/var/log/nuvuMon/

## if you want to do something after installation uncomment the following
## and list the actions to perform:
%post
## actions, e.g. /sbin/ldconfig
#systemctl enable nuvuMon
#systemctl start nuvuMon

## Its similar for %pre, %preun, %pre devel, %preun devel.
%preun
#if [ "$1" = "0" ]; then
#    systemctl stop nuvuMon 
#    systemctl disable nuvuMon
#fi


%clean
## Usually you won't do much more here than
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
## list files that are installed here, e.g
## %{_prefix}/zzz/zzz
/usr/lib/systemd/system/gemgwsapi.service
%{_prefix}/bin/gemgwsapi.py
#%{_prefix}/var/log/nuvuMon/nuvuMonLog.conf

## If you want to have a devel-package to be generated uncomment the following
# %files devel
# %defattr(-,root,root)
## list files that are installed by the devel package here, e.g
## %{_prefix}/zzz/zzz


%changelog
## Write changes here, e.g.
# * Thu Dec 6 2007 John Doe <jdoe@gemini.edu> VERSION-RELEASE
# - change made
# - other change made
#* Mon Sep 23 2024 Ignacio Arriagada <ignacio.arriagada@noirlab.edu> Package created for gemgwsapi 
