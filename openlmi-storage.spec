%global logfile %{_localstatedir}/log/openlmi-install.log

Name:           openlmi-storage
Version:        0.7.1
Release:        7%{?dist}
Summary:        CIM providers for storage management

License:        LGPLv2+
URL:            http://fedorahosted.org/openlmi
Source0:        https://fedorahosted.org/released/openlmi-storage/%{name}-%{version}.tar.gz
Source1:        storage.conf
Source2:        openlmi-storage.tmpfiles.conf
BuildArch:      noarch
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
# To generate documentation
BuildRequires:  python-sphinx
BuildRequires:  python-sphinx-theme-openlmi

Requires:       cmpi-bindings-pywbem
Requires:       python-blivet
Requires:       openlmi-python-providers
# For openlmi-mof-register script:
Requires(pre):  openlmi-providers >= 0.4.1
Requires(preun): openlmi-providers >= 0.4.1
Requires(post): openlmi-providers >= 0.4.1
# For LMI_LogicalFile:
Requires:       openlmi-logicalfile
# For filesystems:
Requires:       xfsprogs, btrfs-progs, e2fsprogs, dosfstools

# https://bugzilla.redhat.com/show_bug.cgi?id=1054144
Patch0:         openlmi-storage-0.7.1-strings-to-object-paths.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1054177
Patch1:         openlmi-storage-0.7.1-reload-mounts.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1057666
Patch2:         openlmi-storage-0.7.1-mount-raid.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1057692
Patch3:         openlmi-storage-0.7.1-remove-pv.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1059114
Patch4:         openlmi-storage-0.7.1-tempdir.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1069140
Patch5:         openlmi-storage-0.7.1-iscsi-deviceid.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1070062
Patch6:         openlmi-storage-0.7.1-raid-uuid.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1072442
Patch7:         openlmi-storage-0.7.1-physical-volume-deviceid.patch

%description
The openlmi-storage package contains CMPI providers for management of storage
using Common Information Managemen (CIM) protocol.

The providers can be registered in any CMPI-aware CIMOM, both OpenPegasus and
SFCB were tested.

%package doc
Summary:        Documentation for %{name}
# We explicitly don't require openlmi-software installed, someone might want
# just to read the documentation on different machine.

%description doc
%{summary}.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# MOF files
install -m 755 -d $RPM_BUILD_ROOT/%{_datadir}/%{name}
install -m 644 mof/* $RPM_BUILD_ROOT/%{_datadir}/%{name}/

# Configuration file
install -m 755 -d $RPM_BUILD_ROOT/%{_sysconfdir}/openlmi/storage
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/openlmi/storage/storage.conf

# Tempfiles file
install -m 755 -d $RPM_BUILD_ROOT/%{_prefix}/lib/tmpfiles.d/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/%{_prefix}/lib/tmpfiles.d/%{name}.conf

# SELinux wrapper
install -m 755 -d $RPM_BUILD_ROOT/%{_libexecdir}/pegasus
install -m 755 pycmpiLMI_Storage-cimprovagt $RPM_BUILD_ROOT/%{_libexecdir}/pegasus/

# Documentation
pushd doc/admin
make html
install -m 755 -d $RPM_BUILD_ROOT/%{_docdir}/%{name}/admin_guide
cp -r _build/html/* $RPM_BUILD_ROOT/%{_docdir}/%{name}/admin_guide/
popd

# /var/lib/ directory
install -m 755 -d $RPM_BUILD_ROOT/%{_localstatedir}/lib/%{name}

%pre
# If upgrading, deregister old version
if [ "$1" -gt 1 ]; then
    # __MethodParameters classes
    openlmi-mof-register -c tog-pegasus --just-mofs unregister \
        %{_datadir}/%{name}/LMI_Storage-MethodParameters.mof || :

    openlmi-mof-register -v %{version} unregister \
        %{_datadir}/%{name}/60_LMI_Storage.mof \
        %{_datadir}/%{name}/LMI_Storage.reg || :


    # static indication filters
    openlmi-mof-register -n root/interop --just-mofs unregister \
        %{_datadir}/%{name}/70_LMI_Storage-IndicationFilters.mof || :

    # Pegasus profile registration
    openlmi-mof-register -c tog-pegasus -n root/interop --just-mofs unregister \
        %{_datadir}/%{name}/70_LMI_Storage-Profiles.mof || :
fi >> %logfile 2>&1

%post
# Register Schema and Provider
if [ "$1" -ge 1 ]; then
    %{_bindir}/openlmi-mof-register -v %{version} register \
        %{_datadir}/%{name}/60_LMI_Storage.mof \
        %{_datadir}/%{name}/LMI_Storage.reg || :

    # __MethodParameters classes
    openlmi-mof-register -c tog-pegasus --just-mofs register \
        %{_datadir}/%{name}/LMI_Storage-MethodParameters.mof || :

    # static indication filters
    openlmi-mof-register -n root/interop --just-mofs register \
        %{_datadir}/%{name}/70_LMI_Storage-IndicationFilters.mof || :

    # Pegasus profile registration
    openlmi-mof-register -c tog-pegasus -n root/interop --just-mofs register \
        %{_datadir}/%{name}/70_LMI_Storage-Profiles.mof || :
fi >> %logfile 2>&1

# Create /run/openlmi-storage in case someone starts the provider
# before the machine is restarted (and tmpfiles.d/openlmi-storage.conf
# is executed)
mkdir -m 0700 /run/openlmi-storage

%preun
# Deregister only if not upgrading
if [ "$1" -eq 0 ]; then
    # __MethodParameters classes
    openlmi-mof-register -c tog-pegasus --just-mofs unregister \
        %{_datadir}/%{name}/LMI_Storage-MethodParameters.mof || :

    %{_bindir}/openlmi-mof-register -v %{version} unregister \
        %{_datadir}/%{name}/60_LMI_Storage.mof \
        %{_datadir}/%{name}/LMI_Storage.reg || :

    # static indication filters
    openlmi-mof-register -n root/interop --just-mofs unregister \
        %{_datadir}/%{name}/70_LMI_Storage-IndicationFilters.mof || :

    # Pegasus profile registration
    openlmi-mof-register -c tog-pegasus -n root/interop --just-mofs unregister \
        %{_datadir}/%{name}/70_LMI_Storage-Profiles.mof || :
fi >> %logfile 2>&1

%files
%doc README COPYING CHANGES
%{python_sitelib}/*
%{_datadir}/%{name}
%config(noreplace,missingok) %{_sysconfdir}/openlmi/storage/storage.conf
%{_libexecdir}/pegasus/pycmpiLMI_Storage-cimprovagt
%dir %{_localstatedir}/lib/%{name}
%{_prefix}/lib/tmpfiles.d/%{name}.conf

%files doc
%{_docdir}/%{name}/admin_guide

%changelog
* Wed Mar  5 2014 Jan Safranek <jsafrane@redhat.com> - 0.7.1-7
- Fixed DeviceID of physical volumes (#1072442)

* Wed Feb 26 2014 Jan Safranek <jsafrane@redhat.com> - 0.7.1-6
- Fixed DeviceID of iSCSI LUNs (#1069140)
- Fixed LMI_MDRAIDFormat.Name (#1070062)

* Thu Jan 30 2014 Jan Safranek <jsafrane@redhat.com> - 0.7.1-5
- Set TempDir to /run/openlmi-storage to secure the temp. files by SELinux
  (#1059114)

* Thu Jan 30 2014 Jan Safranek <jsafrane@redhat.com> - 0.7.1-4
- Added 'TempDir' option to storage.conf (#1059114)

* Tue Jan 28 2014 Jan Safranek <jsafrane@redhat.com> - 0.7.1-3
- The provider now removes physical volume metadata from all member devices
  when a volume group is destroyed (#1057692).
- Fixed listing of mounts of MD RAID volumes (#1057666).

* Wed Jan 22 2014 Jan Safranek <jsafrane@redhat.com> - 0.7.1-2
- Fix CreateOrModifyStoragePool exception (#1054144).
- Fixed reloading of blivet after mount (#1054177).

* Thu Jan  9 2014 Jan Safranek <jsafrane@redhat.com> - 0.7.1-1
- New upstream release (#1049448).

* Tue Jan  7 2014 Jan Safranek <jsafrane@redhat.com> - 0.7.0-8
- Added dist tag to Release.
- Removed unimplemented classed from MOF files (#1042743).
- Fixed LMI_MDRAIDElementCapabilities.GetInstance call (#1043932).

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.7.0-7
- Mass rebuild 2013-12-27

* Thu Dec 12 2013 Jan Synáček <jsynacek@redhat.com> - 0.7.0-6
- Fix error if CreateOrModifyVG() is called with only ElementName and Pool parameters (#1040465).

* Fri Dec  6 2013 Jan Synáček <jsynacek@redhat.com> - 0.7.0-5
- Fix backtrace if InstanceID is None (#1039057).

* Fri Dec  6 2013 Jan Safranek <jsafrane@redhat.com> - 0.7.0-4
- Updated documentation to the latest lmishell (#1027698).

* Thu Nov 28 2013 Jan Safranek <jsafrane@redhat.com> - 0.7.0-3
- Recompiled with correct patch sequence.

* Thu Nov 28 2013 Jan Synáček <jsynacek@redhat.com> - 0.7.0-2
- Fixed mounting associations (#1035354).
- Fixed LMI_LVStorageCapabilities.GetInstance (#1034803)
- Fixed LMI_VGElementCapabilities registration (#1034853)
- Fixed LMI_MemberOfBlockStatisticsManifestCollection.GetInstance (#1035686)
- Added implementation of LMI_FileSystemCapabilities (#1035305)

* Mon Nov  4 2013 Jan Safranek <jsafrane@redhat.com> - 0.7.0-1
- New upstream version.
  - LUKS implemented.

* Mon Sep  2 2013 Jan Safranek <jsafrane@redhat.com> - 0.6.0-2
- Fixed python namespace registration.

* Thu Aug 29 2013 Jan Safranek <jsafrane@redhat.com> - 0.6.0-1
- New upstrem version.
  - Added documentation to openlmi-storage-doc subpackage.
  - Reworked logging.

* Thu Aug 15 2013 Jan Safranek <jsafrane@redhat.com> - 0.5.3-3
- Fixed registration into SFCB (#995561)
- Added logging of RPM scripts.

* Mon Aug 12 2013 Jan Safranek <jsafrane@redhat.com> - 0.5.3-2
- Removed superfluous lmi/__init__.py

* Thu Aug  8 2013 Jan Safranek <jsafrane@redhat.com> - 0.5.3-1
- New upstream release.

* Thu Jun 27 2013 Jan Safranek <jsafrane@redhat.com> - 0.5.2-1
- Added adjustments for separate SELinux policy for the provider.
- Renamed root/PG_interop to root/interop.
- New upstream release.

* Wed Jun 26 2013 Jan Safranek <jsafrane@redhat.com> - 0.5.1-2
- Fixed registration of static indication filters

* Thu May 30 2013 Jan Safranek <jsafrane@redhat.com> - 0.5.1-1
- Update to 0.5.1

* Fri May 10 2013 Jan Safranek <jsafrane@redhat.com> - 0.5.1.pre2-1
- Update to 0.5.1.pre2

* Wed Apr 10 2013 Jan Safranek <jsafrane@redhat.com> - 0.5.1.pre1-1
- Update to 0.5.1.pre1

* Thu Feb  7 2013 Jan Safranek <jsafrane@redhat.com> - 0.5.0-2
- Fixed the dependency on openlmi-providers, it must be available on install
  time.

* Wed Jan  9 2013 Jan Safranek <jsafrane@redhat.com> - 0.5.0-1
- Update to 0.5.0

* Tue Nov 13 2012 Jan Safranek <jsafrane@redhat.com> - 0.4.1-1
- Update to 0.4.1
  - relicensed to LGPLv2+

* Tue Oct 23 2012 Jan Safranek <jsafrane@redhat.com> - 0.4.0-2
- Fixed openlmi-mof-register script name

* Mon Oct 22 2012 Jan Safranek <jsafrane@redhat.com> - 0.4.0-1
- Update to 0.4.0
  - renamed Cura to OpenLMI

* Wed Sep  5 2012 Jan Safranek <jsafrane@redhat.com> - 0.3
- Update to 0.2.1
- Add post/preun RPM scriptlets to register MOFs and providers
  with Pegasus and/or SFCB

* Tue Sep  4 2012 Jan Safranek <jsafrane@redhat.com> - 0.2.1-1
- Update to 0.2.1

* Tue Sep  4 2012 Jan Safranek <jsafrane@redhat.com> - 0.2-1
- Update to 0.2
  - renamed Cura_ to LMI_

* Mon Aug  6 2012 Jan Safranek <jsafrane@redhat.com> - 0.1-3
- Removed rm -rf RPM_BUILD_ROOT

* Thu Aug  2 2012 Jan Safranek <jsafrane@redhat.com> - 0.1-2
- Removed python_sitelib and python_sitearch macro definition
- Removed CFLAGS

* Tue Jul 24 2012 Jan Safranek <jsafrane@redhat.com> - 0.1-1
- Package created.
