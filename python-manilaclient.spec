Name:       python-manilaclient
Version:    1.1.0
Release:    1%{?dist}
Summary:    Client Library for OpenStack Share API
License:    ASL 2.0
URL:        http://pypi.python.org/pypi/%{name}
Source0:    http://tarballs.openstack.org/python-manilaclient/%{name}-%{version}.tar.gz

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
%setup -q

# Remove bundled egg-info
rm -rf python_manilaclient.egg-info

# make doc build compatible with python-oslo-sphinx RPM
sed -i 's/oslosphinx/oslo.sphinx/;s/^html_theme_options/#&/' doc/source/conf.py

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
* Tue Apr 28 2015 Pete Zaitcev <zaitcev@redhat.com> - 1.1.0-1
- Update to upstream Kilo release candidate 1.1.0

* Fri Mar 27 2015 Haikel Guemar <hguemar@fedoraproject.org> 1.0.3-1
- Update to upstream 1.0.3

* Tue Dec 09 2014 Pete Zaitcev <zaitcev@redhat.com> - 1.0.1-3
- Add BuildRequires: python-oslo-sphinx

* Wed Nov 26 2014 Pete Zaitcev <zaitcev@redhat.com> - 1.0.1-2
- Updated with packaging review comments (#1168005)

* Tue Nov 25 2014 Pete Zaitcev <zaitcev@redhat.com> - 1.0.1-1
- Initial Revision
