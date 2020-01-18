%global logfile %{_localstatedir}/log/openlmi-install.log

Name:           openlmi-storage
Version:        0.8.0
Release:        1
Summary:        CIM providers for storage management

License:        LGPLv2+
URL:            http://fedorahosted.org/openlmi
Source0:        https://fedorahosted.org/released/openlmi-storage/%{name}-%{version}.tar.gz
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
# For scsi-rescan:
Requires:       sg3_utils

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

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# MOF files
install -m 755 -d $RPM_BUILD_ROOT/%{_datadir}/%{name}
install -m 644 mof/* $RPM_BUILD_ROOT/%{_datadir}/%{name}/

# Configuration file
install -m 755 -d $RPM_BUILD_ROOT/%{_sysconfdir}/openlmi/storage
install -m 644 storage.conf $RPM_BUILD_ROOT/%{_sysconfdir}/openlmi/storage/storage.conf

# Tempfiles file
install -m 755 -d $RPM_BUILD_ROOT/%{_prefix}/lib/tmpfiles.d/
install -m 644 openlmi-storage.tmpfiles.conf $RPM_BUILD_ROOT/%{_prefix}/lib/tmpfiles.d/%{name}.conf

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
systemd-tmpfiles --create %{_prefix}/lib/tmpfiles.d/%{name}.conf

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
* Wed Sep  3 2014 Jan Safranek <jsafrane@redhat.com> - 0.8.0-1
- Released new version.

* Fri Jan 31 2014 Jan Safranek <jsafrane@redhat.com> - 0.7.1-2
- Use /run/openlmi-storage for temporary files.

* Tue Jan  7 2014 Jan Safranek <jsafrane@redhat.com> - 0.7.1-1
- Released new version.

* Mon Nov  4 2013 Jan Safranek <jsafrane@redhat.com> - 0.7.0-1
- Released new version.
- LUKS implemented.

* Tue Aug 27 2013 Jan Safranek <jsafrane@redhat.com> - 0.6.0-1
- Released new version.
- Added documentation to openlmi-storage-doc subpackage.
- Reworked logging.

* Wed Aug 14 2013 Jan Safranek <jsafrane@redhat.com> - 0.5.3-2
- Register __MethodParameters classes only in Pegasus.
- Added logging of RPM scripts.

* Thu Aug  1 2013  <jsafrane@redhat.com> - 0.5.3-1
- Released new version.

* Fri Jul 26 2013  <jsafrane@redhat.com> - 0.5.2-1
- Released new version.

* Wed Jul 24 2013  <jsafrane@redhat.com> - 0.5.1-3
- Renamed root/PG_interop to root/interop to reflect current Rawhide.

* Thu Jun 27 2013 Jan Safranek <jsafrane@redhat.com> - 0.5.1-2
- Added sample configuration file.
- Added cimprovagt wrapper for SELinux.
- Added registration of static indication filters.

* Mon May 13 2013 Jan Safranek <jsafrane@redhat.com> - 0.5.1-1
- Create the spec file.
