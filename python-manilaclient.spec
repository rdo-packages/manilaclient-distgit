# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname manilaclient
%global with_doc 1

%if 0%{?fedora}
%global with_python3 1
%endif

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

BuildArch:  noarch

%description
%{common_desc}

%package -n python%{pyver}-%{sname}
Summary:    Client Library for OpenStack Share API
%{?python_provide:%python_provide python%{pyver}-%{sname}}
Obsoletes: python2-%{sname} < %{version}-%{release}

# We require a whole set of packages that are not needed by setup.py,
# merely because Sphinx pulls them in when scanning for docstrings.
BuildRequires: python%{pyver}-devel
BuildRequires: python%{pyver}-keystoneclient
BuildRequires: python%{pyver}-oslo-utils
BuildRequires: python%{pyver}-pbr
BuildRequires: git
BuildRequires: python%{pyver}-prettytable
BuildRequires: python%{pyver}-setuptools
BuildRequires: python%{pyver}-six

Requires:   python%{pyver}-babel
Requires:   python%{pyver}-keystoneclient >= 1:3.8.0
Requires:   python%{pyver}-oslo-config >= 2:5.2.0
Requires:   python%{pyver}-oslo-i18n >= 3.15.3
Requires:   python%{pyver}-oslo-log >= 3.36.0
Requires:   python%{pyver}-oslo-serialization >= 2.18.0
Requires:   python%{pyver}-oslo-utils >= 3.33.0
Requires:   python%{pyver}-pbr
Requires:   python%{pyver}-prettytable
Requires:   python%{pyver}-requests >= 2.14.2
Requires:   python%{pyver}-six
Requires:   python%{pyver}-debtcollector
Requires:   python%{pyver}-osc-lib >= 1.10.0

Requires:   python%{pyver}-simplejson


%description -n python%{pyver}-%{sname}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:    Documentation for OpenStack Share API Client

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-sphinxcontrib-programoutput
BuildRequires: python%{pyver}-openstackdocstheme

%description doc
%{common_desc}

This package contains documentation.
%endif

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# Remove bundled egg-info
rm -rf python_manilaclient.egg-info

%build
%{pyver_build}

%if 0%{?with_doc}
sphinx-build-%{pyver} -b html doc/source doc/build/html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

%install
%{pyver_install}

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s manila %{buildroot}%{_bindir}/manila-%{pyver}

# Install bash completion
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 tools/manila.bash_completion \
    %{buildroot}%{_sysconfdir}/bash_completion.d/manila


%files -n python%{pyver}-%{sname}
%doc README.rst
%license LICENSE
%{_bindir}/manila
%{_bindir}/manila-%{pyver}
%{_sysconfdir}/bash_completion.d
%{pyver_sitelib}/manilaclient
%{pyver_sitelib}/*.egg-info

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
