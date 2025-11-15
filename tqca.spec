#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg tqca
%define tde_prefix /opt/trinity
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}

%if 0%{?mdkversion} || 0%{?mgaversion} || 0%{?pclinuxos}
%define libtqca %{_lib}tqca
%else
%define libtqca libtqca
%endif

%if 0%{?mdkversion} || 0%{?mgaversion} || 0%{?pclinuxos}
%define libtqt3 %{_lib}tqt3
%else
%define libtqt3 libtqt3
%endif

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	1.0
Release:	%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	TQt Cryptographic Architecture
Group:		Development/Libraries/C and C++
URL:		http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/dependencies/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz
Source1:		trinity-tqca-rpmlintrc

Obsoletes:		%{libtqt3}-mt-tqca-tls < %{version}-%{release}
Provides:		%{libtqt3}-mt-tqca-tls = %{version}-%{release}

BuildSystem:    cmake
BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo" 
BuildOption:    -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" 
BuildOption:    -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" 
BuildOption:    -DCMAKE_SKIP_RPATH=ON 
BuildOption:    -DCMAKE_VERBOSE_MAKEFILE=ON 
BuildOption:    -DWITH_GCC_VISIBILITY=OFF
BuildOption:    -DWITH_ALL_OPTIONS="ON"

BuildRequires:  libtqt4-devel >= %{tde_epoch}:4.2.0
BuildRequires:	trinity-tde-cmake >= %{tde_version}
%if "%{?toolchain}" != "clang"
BuildRequires:	gcc-c++
%endif

BuildRequires:  pkgconfig(openssl)

%description
Taking a hint from the similarly-named Java Cryptography Architecture,
TQCA aims to provide a straightforward and cross-platform crypto API,
using TQt datatypes and conventions. TQCA separates the API from the
implementation, using plugins known as Providers. The advantage of this
model is to allow applications to avoid linking to or explicitly depending
on any particular cryptographic library. This allows one to easily change
or upgrade crypto implementations without even needing to recompile the
application!

##########

%package -n %{libtqca}1
Summary:	TQt Cryptographic Architecture
Group:		Development/Libraries/C and C++

Obsoletes:	trinity-libtqca < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-libtqca = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	libtqca = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	libtqca1 = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libtqca}1
Taking a hint from the similarly-named Java Cryptography Architecture,
TQCA aims to provide a straightforward and cross-platform crypto API,
using TQt datatypes and conventions. TQCA separates the API from the
implementation, using plugins known as Providers. The advantage of this
model is to allow applications to avoid linking to or explicitly depending
on any particular cryptographic library. This allows one to easily change
or upgrade crypto implementations without even needing to recompile the
application!

%post -n %{libtqca}1
/sbin/ldconfig

%postun -n %{libtqca}1
/sbin/ldconfig

%files -n %{libtqca}1
%defattr(-,root,root,-)
%doc COPYING README TODO
%{_libdir}/libtqca.so.1
%{_libdir}/libtqca.so.1.0.0

##########

%package -n %{libtqca}-devel
Summary:	TQt Cryptographic Architecture development files
Group:		Development/Libraries/C and C++
Requires:	%{libtqca}1 = %{?epoch:%{epoch}:}%{version}-%{release}

Obsoletes:	trinity-libtqca-devel < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-libtqca-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	libtqca-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libtqca}-devel
This packages contains the development files for TQCA

%post -n %{libtqca}-devel
/sbin/ldconfig

%postun -n %{libtqca}-devel
/sbin/ldconfig

%files -n %{libtqca}-devel
%defattr(-,root,root,-)
%{_includedir}/tqt3/tqca.h
%{_includedir}/tqt3/tqcaprovider.h
%{_libdir}/libtqca.la
%{_libdir}/libtqca.so
%{_libdir}/pkgconfig/tqca.pc
%dir %{_libdir}/tqt3/plugins/crypto
%{_libdir}/tqt3/plugins/crypto/libtqca-tls.so

##########

%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}

# Fix 'lib64' library directory
perl -pi -e 's,target\.path=\$PREFIX/lib,target.path=\$PREFIX/%{_lib},g' qcextra


%build
unset QTDIR QTINC QTLIB

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=ON \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
   \
  -DINCLUDE_INSTALL_DIR=%{_includedir} \
  -DLIB_INSTALL_DIR=%{_libdir} \
  \
  -DWITH_ALL_OPTIONS="ON" \
  ..

%__make %{?_smp_mflags} || %__make


%install
%__make install DESTDIR=%{?buildroot} -C build
