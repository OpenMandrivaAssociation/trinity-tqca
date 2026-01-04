%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 4

%define tde_pkg tqca

%define libtqca %{_lib}tqca

%define libtqt3 %{_lib}tqt3

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity

Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	1.0
Release:	%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:	TQt Cryptographic Architecture
Group:		Development/Libraries/C and C++
URL:		http://www.trinitydesktop.org/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/dependencies/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz
Source1:		trinity-tqca-rpmlintrc

Obsoletes:		%{libtqt3}-mt-tqca-tls < %{version}-%{release}
Provides:		%{libtqt3}-mt-tqca-tls = %{version}-%{release}

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo" 
BuildOption:    -DWITH_ALL_OPTIONS="ON"
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:  libtqt4-devel >= %{tde_epoch}:4.2.0
BuildRequires:	trinity-tde-cmake >= %{tde_version}

%{!?with_clang:BuildRequires:	gcc-c++}

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

%prep -a
# Fix 'lib64' library directory
perl -pi -e 's,target\.path=\$PREFIX/lib,target.path=\$PREFIX/%{_lib},g' qcextra
