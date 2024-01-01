# Copyright 2025 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

%global _lto_cflags %{?_lto_cflags} -ffat-lto-objects

Name: capstone
Epoch: 100
Version: 5.0.3
Release: 1%{?dist}
Summary: A lightweight multi-platform, multi-architecture disassembly framework
License: BSD-3-Clause
URL: https://github.com/capstone-engine/capstone/tags
Source0: %{name}_%{version}.orig.tar.gz
%if 0%{?rhel} == 7
BuildRequires: devtoolset-11
BuildRequires: devtoolset-11-gcc
BuildRequires: devtoolset-11-gcc-c++
BuildRequires: devtoolset-11-libatomic-devel
%endif
BuildRequires: cmake
BuildRequires: fdupes
BuildRequires: gcc-c++
BuildRequires: libtool
BuildRequires: make
BuildRequires: python-rpm-macros
BuildRequires: python3-Cython3
BuildRequires: python3-devel
BuildRequires: python3-setuptools

%description
Capstone is a disassembly framework with the target of becoming the
ultimate disasm engine for binary analysis and reversing in the security
community.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
%if 0%{?rhel} == 7
. /opt/rh/devtoolset-11/enable
%endif
%cmake \
    -DBUILD_SHARED_LIBS="ON" \
    -DBUILD_STATIC_LIBS="OFF" \
    -DCAPSTONE_BUILD_STATIC_RUNTIME="OFF" \
    -DCAPSTONE_ARCHITECTURE_DEFAULT="OFF" \
    -DCAPSTONE_X86_SUPPORT="ON"
%cmake_build
pushd bindings/python && \
    %py3_build && \
    popd

%install
%cmake_install
pushd bindings/python && \
    %py3_install && \
    popd
rm -rf %{buildroot}%{python3_sitelib}/*/include
rm -rf %{buildroot}%{python3_sitelib}/*/lib    
find %{buildroot}%{python3_sitelib} -type f -name '*.pyc' -exec rm -rf {} \;
fdupes -qnrps %{buildroot}%{python3_sitelib}

%check

%if 0%{?suse_version} > 1500
%package -n libcapstone-devel
Summary: Development files for capstone
Requires: libcapstone5 = %{epoch}:%{version}-%{release}

%description -n libcapstone-devel
The libcapstone-devel package contains libraries and header files for
developing applications that use capstone.

%package -n libcapstone5
Summary: A multi-platform, multi-architecture disassembly framework

%description -n libcapstone5
Capstone is a disassembly framework.

%package -n python%{python3_version_nodots}-capstone
Summary: Python3 bindings for capstone
Requires: python3
Requires: libcapstone5 = %{epoch}:%{version}-%{release}
Provides: python3-capstone = %{epoch}:%{version}-%{release}
Provides: python3dist(capstone) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-capstone = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(capstone) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-capstone = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(capstone) = %{epoch}:%{version}-%{release}

%description -n python%{python3_version_nodots}-capstone
This package contains the Capstone bindings for Python.

%post -n libcapstone5 -p /sbin/ldconfig
%postun -n libcapstone5 -p /sbin/ldconfig

%files
%license LICENSE.TXT
%{_bindir}/*

%files -n libcapstone5
%{_libdir}/*.so.*

%files -n libcapstone-devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/capstone
%{_libdir}/pkgconfig/*

%files -n python%{python3_version_nodots}-capstone
%{python3_sitelib}/*
%endif

%if 0%{?sle_version} > 150000
%package -n libcapstone-devel
Summary: Development files for capstone
Requires: libcapstone5 = %{epoch}:%{version}-%{release}

%description -n libcapstone-devel
The libcapstone-devel package contains libraries and header files for
developing applications that use capstone.

%package -n libcapstone5
Summary: A multi-platform, multi-architecture disassembly framework

%description -n libcapstone5
Capstone is a disassembly framework.

%package -n python3-capstone
Summary: Python3 bindings for capstone
Requires: python3
Requires: libcapstone5 = %{epoch}:%{version}-%{release}
Provides: python3-capstone = %{epoch}:%{version}-%{release}
Provides: python3dist(capstone) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-capstone = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(capstone) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-capstone = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(capstone) = %{epoch}:%{version}-%{release}

%description -n python3-capstone
This package contains the Capstone bindings for Python.

%post -n libcapstone5 -p /sbin/ldconfig
%postun -n libcapstone5 -p /sbin/ldconfig

%files
%license LICENSE.TXT
%{_bindir}/*

%files -n libcapstone5
%{_libdir}/*.so.*

%files -n libcapstone-devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/capstone
%{_libdir}/pkgconfig/*

%files -n python3-capstone
%{python3_sitelib}/*
%endif

%if !(0%{?suse_version} > 1500) && !(0%{?sle_version} > 150000)
%package -n capstone-devel
Summary: Development files for capstone
Requires: capstone = %{epoch}:%{version}-%{release}

%description -n capstone-devel
The capstone-devel package contains libraries and header files for
developing applications that use capstone.

%package -n python3-capstone
Summary: Python3 bindings for capstone
Requires: capstone = %{epoch}:%{version}-%{release}
Requires: python3
Provides: python3-capstone = %{epoch}:%{version}-%{release}
Provides: python3dist(capstone) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-capstone = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(capstone) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-capstone = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(capstone) = %{epoch}:%{version}-%{release}

%description -n python3-capstone
This package contains the Capstone bindings for Python.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.TXT
%{_bindir}/*
%{_libdir}/*.so.*

%files -n capstone-devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/capstone
%{_libdir}/pkgconfig/*

%files -n python3-capstone
%{python3_sitelib}/*
%endif

%changelog
