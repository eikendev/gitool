%global pythonv python3
%global srcname gitool

Name:           %{srcname}
Version:        1.1.3
Release:        1%{?dist}
Summary:        A tool for managing git repositories
License:        MIT
URL:            https://pypi.python.org/pypi/%{srcname}
#Source0:        %%pypi_source
Source0:        https://files.pythonhosted.org/packages/source/g/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  %{pythonv}-devel
BuildRequires:  %{pythonv}-setuptools
BuildRequires:  %{pythonv}-setuptools_scm
Requires:       %{pythonv}-GitPython
Requires:       %{pythonv}-colorama

%description
%{summary}.

%prep
%autosetup

%build
%py3_build

%install
%py3_install

%files
%license LICENSE
%doc README.rst
%doc data/config-example.ini
%{_bindir}/%{srcname}
%{python3_sitelib}/*

%changelog
* Sat May 04 2019 eikendev <raphael@eiken.dev> - 1.1.3-1
- Update to 1.1.3

* Sat Apr 13 2019 eikendev <raphael@eiken.dev> - 1.1.1-1
- Initial package
