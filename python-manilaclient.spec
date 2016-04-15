%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:       python-manilaclient
Version:    1.8.1
Release:    1%{?dist}
Summary:    Client Library for OpenStack Share API
License:    ASL 2.0
URL:        http://pypi.python.org/pypi/%{name}
Source0:    http://tarballs.openstack.org/python-manilaclient/%{name}-%{upstream_version}.tar.gz

BuildArch:  noarch
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

%description
Client library and command line utility for interacting with Openstack
Share API.

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
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
make html
popd

#install -p -D -m 644 doc/manpages/swift.1 #{buildroot}#{_mandir}/man1/swift.1

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

%files
%doc LICENSE README.rst
%{_bindir}/manila
%{python2_sitelib}/manilaclient
%{python2_sitelib}/*.egg-info
#{_mandir}/man1/swift.1*

%files doc
%doc LICENSE doc/build/html

%changelog
* Wed Mar 23 2016 RDO <rdo-list@redhat.com> 1.8.1-0.1
-  Rebuild for Mitaka 1.8.1
