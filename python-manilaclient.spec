%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname manilaclient

%if 0%{?fedora}
%global with_python3 1
%endif

%global common_desc \
Client library and command line utility for interacting with Openstack \
Share API.

Name:       python-manilaclient
Version:    1.24.2
Release:    1%{?dist}
Summary:    Client Library for OpenStack Share API
License:    ASL 2.0
URL:        https://pypi.io/pypi/%{name}
Source0:    https://tarballs.openstack.org/python-manilaclient/%{name}-%{upstream_version}.tar.gz

BuildArch:  noarch

%description
%{common_desc}

%package -n python2-%{sname}
Summary:    Client Library for OpenStack Share API
%{?python_provide:%python_provide python2-%{sname}}

# We require a whole set of packages that are not needed by setup.py,
# merely because Sphinx pulls them in when scanning for docstrings.
BuildRequires: python2-devel
BuildRequires: python2-keystoneclient
BuildRequires: python2-oslo-utils
BuildRequires: python2-pbr
BuildRequires: git
BuildRequires: python2-prettytable
BuildRequires: python2-setuptools
BuildRequires: python2-six

Requires:   python2-babel
Requires:   python2-keystoneclient >= 1:3.8.0
Requires:   python2-oslo-config >= 2:5.2.0
Requires:   python2-oslo-i18n >= 3.15.3
Requires:   python2-oslo-log >= 3.36.0
Requires:   python2-oslo-serialization >= 2.18.0
Requires:   python2-oslo-utils >= 3.33.0
Requires:   python2-pbr
Requires:   python2-prettytable
Requires:   python2-requests >= 2.14.2
Requires:   python2-six
Requires:   python2-debtcollector
%if 0%{?fedora} > 0
Requires:   python2-simplejson
Requires:   python2-ipaddress
%else
Requires:   python-simplejson
Requires:   python-ipaddress
%endif

%description -n python2-%{sname}
%{common_desc}

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:    Client Library for OpenStack Share API
%{?python_provide:%python_provide python3-%{sname}}

# We require a whole set of packages that are not needed by setup.py,
# merely because Sphinx pulls them in when scanning for docstrings.
BuildRequires: python3-devel
BuildRequires: python3-keystoneclient
BuildRequires: python3-oslo-utils
BuildRequires: python3-pbr
BuildRequires: python3-prettytable
BuildRequires: python3-setuptools
BuildRequires: python3-six

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
Requires:   python3-simplejson
Requires:   python3-six
Requires:   python3-debtcollector

%description -n python3-%{sname}
%{common_desc}
%endif


%package doc
Summary:    Documentation for OpenStack Share API Client

BuildRequires: python2-sphinx
BuildRequires: python2-openstackdocstheme

%description doc
%{common_desc}

This package contains documentation.

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# Remove bundled egg-info
rm -rf python_manilaclient.egg-info

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

sphinx-build -b html doc/source doc/build/html

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/manila %{buildroot}%{_bindir}/manila-%{python3_version}
ln -s ./manila-%{python3_version} %{buildroot}%{_bindir}/manila-3
# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/manilaclient/tests
%endif

%py2_install
mv %{buildroot}%{_bindir}/manila %{buildroot}%{_bindir}/manila-%{python2_version}
ln -s ./manila-%{python2_version} %{buildroot}%{_bindir}/manila-2

ln -s ./manila-2 %{buildroot}%{_bindir}/manila

# Install bash completion
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 tools/manila.bash_completion \
    %{buildroot}%{_sysconfdir}/bash_completion.d/manila


%files -n python2-%{sname}
%doc README.rst
%license LICENSE
%{_bindir}/manila
%{_bindir}/manila-2*
%{_sysconfdir}/bash_completion.d
%{python2_sitelib}/manilaclient
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-%{sname}
%doc README.rst
%license LICENSE
%{_bindir}/manila-3*
%{python3_sitelib}/manilaclient
%{python3_sitelib}/*.egg-info
%endif

%files doc
%doc doc/build/html
%license LICENSE

%changelog
* Tue Apr 23 2019 RDO <dev@lists.rdoproject.org> 1.24.2-1
- Update to 1.24.2

* Thu Aug 09 2018 RDO <dev@lists.rdoproject.org> 1.24.1-1
- Update to 1.24.1


