%bcond_with test

Name:		liquidctl
Version:	1.14.0
Release:	2
Source0:	https://files.pythonhosted.org/packages/source/l/%{name}/%{name}-%{version}.tar.gz
Summary:	Cross-platform tool and drivers for liquid coolers and other devices
URL:		https://github.com/liquidctl/liquidctl
License:	GPL-3.0-or-later
Group:		Development/Python

BuildSystem:	python
BuildArch:	noarch

BuildRequires:	python
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(setuptools-scm)
BuildRequires:	python%{pyver}dist(wheel)
BuildRequires:	systemd-rpm-macros
# for tests
BuildRequires:	python%{pyver}dist(pytest)
BuildRequires:	python%{pyver}dist(pluggy)
BuildRequires:	python%{pyver}dist(hypothesis)
BuildRequires:	python%{pyver}dist(pytest-asyncio)
BuildRequires:	python%{pyver}dist(pytest-randomly)
BuildRequires:	python%{pyver}dist(pytest-forked)
BuildRequires:	python%{pyver}dist(pytest-flake8)
BuildRequires:	python%{pyver}dist(pytest-mock)
BuildRequires:	python%{pyver}dist(colorlog)
BuildRequires:	python%{pyver}dist(crcmod)
BuildRequires:	python%{pyver}dist(docopt)
BuildRequires:	python%{pyver}dist(hidapi)
BuildRequires:	python%{pyver}dist(pillow)
BuildRequires:	python%{pyver}dist(smbus)
BuildRequires:	pyusb

# Require the python and udev packages with the main package
Requires: python-%{name} = %{version}-%{release}
Requires: %{name}-udev = %{version}-%{release}

Suggests: %{name}-doc = %{version}-%{release}

%description
Cross-platform tool and drivers for liquid coolers and other devices

For a full list of supported devices, visit:
https://github.com/liquidctl/liquidctl#supported-devices

##########################
%package -n python-%{name}
Summary: Module for controlling liquid coolers, case fans and RGB LED devices
Requires:	lib64usb1.0_0
Requires:	python >= 3.9
Requires:	python%{pyver}dist(colorlog)
Requires:	python%{pyver}dist(crcmod)
Requires:	python%{pyver}dist(docopt)
Requires:	python%{pyver}dist(hidapi)
Requires:	python%{pyver}dist(pillow)
Requires:	python%{pyver}dist(smbus)
Requires:	pyusb

Suggests:	%{name}-udev = %{version}-%{release}
Suggests:	%{name}-doc = %{version}-%{release}


%description -n python-%{name}

A python module providing classes for communicating with various cooling
solutions and other RGB LED controllable devices such as Motherboards, GPUs,
Memory, Power Supplies, etc.

For a full list of supported devices, visit:
https://github.com/liquidctl/liquidctl#supported-devices


##########################
%package udev
Summary: Unprivileged device access rules for %{name}
Requires: %{name} = %{version}-%{release}

Suggests:	%{name}
Suggests:	python-%{name}
Suggests:	%{name}-doc

%description udev

This package contains udev rules allowing %{name} access to cooling devices
when ran by an unprivileged user.


##########################
%package doc
Summary: Documentation for %{name}

Suggests:	%{name}
Suggests:	python-%{name}
Suggests:	%{name}-udev

%description doc
This package contains documentation for %{name}.


##########################
%global setuptools_ver %{gsub %{version} %W -}

%prep
%autosetup -p1 -n liquidctl-%{version}
mkdir -p ./build/man/man8
cp README.md ./build
cp LICENSE.txt ./build
cp liquidctl.8 ./build/man/man8

%build
%py_build

%install
%py3_install
install -dpm 0755 %{buildroot}%{_docdir}/%{name}
install -dpm 0755 %{buildroot}%{_mandir}/man8

zstd -r --rm %_vpath_builddir/man/man8
mv %_vpath_builddir/man/man8 %{buildroot}%{_mandir}

install -Dpm 644 extra/completions/liquidctl.bash %{buildroot}%{_datadir}/bash-completion/completions/%{name}
install -Dpm 644 extra/linux/71-%{name}.rules %{buildroot}%{_udevrulesdir}/71-%{name}.rules
install -Dpm 644 -t %{buildroot}%{_docdir}/%{name} CHANGELOG.md README.md LICENSE.txt
cp -a docs/ %{buildroot}%{_docdir}/%{name}

# tests run locally, disabled for abf.
%if %{with test}
%check
%{__python} -m pytest tests/
%endif

%files
%{_bindir}/%{name}
%{_mandir}/man8/%{name}.*
%{_docdir}/%{name}/*.md
%{_datadir}/bash-completion/completions/%{name}

%files -n python-%{name}
%{python3_sitelib}/%{name}-*.dist-info
%{python3_sitelib}/%{name}/*.py
%{python3_sitelib}/%{name}/__pycache__/*.cpython-3*.pyc
%{python3_sitelib}/%{name}/driver/*.py
%{python3_sitelib}/%{name}/driver/__pycache__/*.cpython-3*.pyc

%license LICENSE.txt

%files udev
%{_udevrulesdir}/71-%{name}.rules

%files doc
%{_docdir}/%{name}
