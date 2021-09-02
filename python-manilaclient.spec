%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname manilaclient
%global with_doc 1

%global common_desc \
Client library and command line utility for interacting with Openstack \
Share API.

Name:       python-manilaclient
Version:    XXX
Release:    XXX
Summary:    Client Library for OpenStack Share API
License:    ASL 2.0
URL:        https://pypi.io/pypi/%{name}
Source0:    https://tarballs.openstack.org/python-manilaclient/%{name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/python-manilaclient/%{name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
%{common_desc}

%package -n python3-%{sname}
Summary:    Client Library for OpenStack Share API
%{?python_provide:%python_provide python3-%{sname}}
Obsoletes: python2-%{sname} < %{version}-%{release}

# We require a whole set of packages that are not needed by setup.py,
# merely because Sphinx pulls them in when scanning for docstrings.
BuildRequires: python3-devel
BuildRequires: python3-keystoneclient
BuildRequires: python3-oslo-utils
BuildRequires: python3-pbr
BuildRequires: git-core
BuildRequires: python3-prettytable
BuildRequires: python3-setuptools

Requires:   python3-babel
Requires:   python3-keystoneclient >= 1:3.8.0
Requires:   python3-oslo-config >= 2:5.2.0
Requires:   python3-oslo-i18n >= 3.15.3
Requires:   python3-oslo-log >= 3.36.0
Requires:   python3-oslo-serialization >= 2.18.0
Requires:   python3-oslo-utils >= 3.33.0
Requires:   python3-pbr
Requires:   python3-prettytable
Requires:   python3-requests >= 2.14.2
Requires:   python3-debtcollector
Requires:   python3-osc-lib >= 1.10.0

Requires:   python3-simplejson


%description -n python3-%{sname}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:    Documentation for OpenStack Share API Client

BuildRequires: python3-sphinx
BuildRequires: python3-sphinxcontrib-programoutput
BuildRequires: python3-openstackclient
BuildRequires: python3-openstackdocstheme

%description doc
%{common_desc}

This package contains documentation.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{name}-%{upstream_version} -S git

# Remove bundled egg-info
rm -rf python_manilaclient.egg-info

%build
%{py3_build}

%if 0%{?with_doc}
sphinx-build -b html doc/source doc/build/html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

%install
%{py3_install}

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s manila %{buildroot}%{_bindir}/manila-3

# Install bash completion
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 tools/manila.bash_completion \
    %{buildroot}%{_sysconfdir}/bash_completion.d/manila


%files -n python3-%{sname}
%doc README.rst
%license LICENSE
%{_bindir}/manila
%{_bindir}/manila-3
%{_sysconfdir}/bash_completion.d
%{python3_sitelib}/manilaclient
%{python3_sitelib}/*.egg-info

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
