%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname manilaclient

%if 0%{?fedora}
%global with_python3 1
%endif

Name:       python-manilaclient
Version:    XXX
Release:    XXX
Summary:    Client Library for OpenStack Share API
License:    ASL 2.0
URL:        http://pypi.python.org/pypi/%{name}
Source0:    http://tarballs.openstack.org/python-manilaclient/%{name}-%{upstream_version}.tar.gz

BuildArch:  noarch

%description
Client library and command line utility for interacting with Openstack
Share API.

%package -n python2-%{sname}
Summary:    Client Library for OpenStack Share API
%{?python_provide:%python_provide python2-%{sname}}

# We require a whole set of packages that are not needed by setup.py,
# merely because Sphinx pulls them in when scanning for docstrings.
BuildRequires: python2-devel
BuildRequires: python-keystoneclient
BuildRequires: python-oslo-sphinx
BuildRequires: python-oslo-utils
BuildRequires: python-pbr
BuildRequires: python-prettytable
BuildRequires: python-setuptools
BuildRequires: python-six

Requires:   python-babel
Requires:   python-iso8601
Requires:   python-keystoneclient
Requires:   python-oslo-config
Requires:   python-oslo-i18n >= 1.5.0
Requires:   python-oslo-serialization
Requires:   python-oslo-utils >= 1.4.0
Requires:   python-prettytable
Requires:   python-requests >= 2.2.0
Requires:   python-simplejson
Requires:   python-six

%description -n python2-%{sname}
Client library and command line utility for interacting with Openstack
Share API.

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:    Client Library for OpenStack Share API
%{?python_provide:%python_provide python3-%{sname}}

# We require a whole set of packages that are not needed by setup.py,
# merely because Sphinx pulls them in when scanning for docstrings.
BuildRequires: python3-devel
BuildRequires: python3-keystoneclient
BuildRequires: python3-oslo-sphinx
BuildRequires: python3-oslo-utils
BuildRequires: python3-pbr
BuildRequires: python3-prettytable
BuildRequires: python3-setuptools
BuildRequires: python3-six

Requires:   python3-babel
Requires:   python3-iso8601
Requires:   python3-keystoneclient
Requires:   python3-oslo-config
Requires:   python3-oslo-i18n >= 1.5.0
Requires:   python3-oslo-serialization
Requires:   python3-oslo-utils >= 1.4.0
Requires:   python3-prettytable
Requires:   python3-requests >= 2.2.0
Requires:   python3-simplejson
Requires:   python3-six

%description -n python3-%{sname}
Client library and command line utility for interacting with Openstack
Share API.
%endif


%package doc
Summary:    Documentation for OpenStack Share API Client

BuildRequires: python-sphinx

%description doc
Documentation for the client library for interacting with Openstack
Share API.

%prep
%setup -q -n %{name}-%{upstream_version}

# Remove bundled egg-info
rm -rf python_manilaclient.egg-info

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
make html
popd

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
%doc LICENSE README.rst
%{_bindir}/manila
%{_bindir}/manila-2*
%{_sysconfdir}/bash_completion.d
%{python2_sitelib}/manilaclient
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-%{sname}
%doc LICENSE README.rst
%{_bindir}/manila-3*
%{python3_sitelib}/manilaclient
%{python3_sitelib}/*.egg-info
%endif

%files doc
%doc LICENSE doc/build/html

%changelog

