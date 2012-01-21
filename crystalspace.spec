%bcond_with	java

Summary:	CrystalSpace free 3d engine
Name:		crystalspace
Version:	1.4.1
Release:	1
Group:		System/Libraries
License:	LGPLv2+
URL:		http://www.crystalspace3d.org/
Source0:	http://www.crystalspace3d.org/downloads/release/%{name}-src-%{version}.tar.bz2
Patch0:		crystalspace-src-1.4.1-cs-config.patch
Patch1:		crystalspace-src-1.2.1-fix-str-fmt.patch
BuildRequires:	lib3ds-devel >= 1.3.0
#BuildRequires:	MesaGLU-devel
BuildRequires:	oggvorbis-devel
BuildRequires:	libmikmod-devel
BuildRequires:	cal3d-devel
BuildRequires:	jpeg-devel
BuildRequires:	zlib-devel
BuildRequires:	ode-devel
BuildRequires:	pkgconfig(libpng12)
BuildRequires:	openal-devel >= 0.0.6-5mdk
BuildRequires:	mng-devel
BuildRequires:	X11-devel
BuildRequires:	nasm
BuildRequires:	perl-devel
BuildRequires:	wxgtku-devel
BuildRequires:	swig >= 1.3.14
BuildRequires:	bison >= 1.35
BuildRequires:	python-devel
BuildRequires:	ftjam
BuildRequires:	flex
BuildRequires:	doxygen
BuildRequires:	pkgconfig(bullet)
BuildRequires:	libtool
BuildRequires:	texinfo
BuildRequires:	librsvg
BuildRequires:	libcaca-devel
BuildRequires:	tetex-dvipdfm
BuildRequires:	tetex-dvips
BuildRequires:	imagemagick
BuildRequires:	cppunit-devel
BuildRequires:	icoutils
BuildRequires:	CEGUI-devel
BuildRequires:	perl(Template::Base)
%if %{with java}
BuildRequires:	java-rpmbuild
BuildRequires:	ant
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Crystal Space is a free (LGPL) and portable 3D Development Kit
written in C++. It supports: true six degree's of freedom,
colored lighting, mipmapping, portals, mirrors, alpha transparency,
reflective surfaces, 3D sprites (frame based or with skeletal animation),
procedural textures, radiosity, particle systems, halos, volumetric fog,
scripting (using Python or other languages), 8-bit, 16-bit, and 32-bit
display support, OpenGL and software renderering, font support,
hierarchical transformations, etc.

%package devel
Group:		Development/C
Summary:	Development headers and libraries for %{name}
Requires:	%{name} = %{version}-%{release}

%description devel
Development headers and libraries for %{name}.

%package doc
Summary:	Crystalspace documentation
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Conflicts:	freetds-devel

%description doc
Crystalspace documentation.

%package demos
Summary:	Crystalspace demos
Group:		Toys
Requires:	%{name} = %{version}-%{release}

%description	demos
Crystalspace demos.

%package bindings-python
Summary:	Python bindings for Crystal Space free 3D SDK
Group:		Development/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python

%description bindings-python
Python bindings for Crystal Space free 3D SDK.

%if %{with java}
%package bindings-java
Group:		Development/Java
Summary:	Java bindings for Crystal Space free 3D SDK
Requires:	%{name} = %{version}-%{release}
Requires:	java

%description bindings-java
Java bindings for Crystal Space free 3D SDK.
%endif

%package bindings-perl
Summary:	Perl bindings for Crystal Space free 3D SDK
Group:		Development/Perl
Requires:	%{name} = %{version}-%{release}
Requires:	perl

%description bindings-perl
Perl bindings for Crystal Space free 3D SDK.

%prep
%setup -q -n %{name}-src-%{version}
%patch0 -p1
#patch1 -p0

# work around mikmod not being linked to libdl as it should
#sed -i 's/-lmikmod/-lmikmod -ldl/g' configure
# stop configure from adding -L/usr/local/lib to cs-config (and the build)
#sed -i 's|-d /usr/local/lib|-d /foobar|' configure

# (tpg) kill arch optimizations, in case of mdv -march= is always set to generic
for i in i486 i586 i686 athlon k8; do
    sed -i -e 's/march='$i'//g' configure*
    sed -i -e 's/mtune='$i'//g' configure*;
done

sed	-e 's#--exists libpng#--exists libpng12#g' \
	-e 's#--cflags libpng#--cflags libpng12#g' \
	-e 's#--libs libpng#--libs libpng12#g' \
	-i configure

%build
export CFLAGS="%{optflags} -I%{_includedir} -I%{_includedir}/AL -fpermissive"
export CXXFLAGS=$CFLAGS
export LDFLAGS=$CFLAGS

sed -i -e 's#/usr/local/lib#%{_libdir}#g' configure
sed -i -e 's#/usr/local/include#%{_includedir}#g' configure
sed -i -e 's#/usr/local#%{_prefix}#g' configure

%configure2_5x	\
	--with-mesa \
	--disable-optimize \
	--disable-debug \
	--disable-separate-debug-info \
%if %{with java}
	--with-java \
%else
	--without-java \
%endif
	--with-wx \
	--with-caca=%{_prefix} \
	--disable-meta-info-embedding

jam -d2 %{_smp_mflags}

%install
rm -rf %{buildroot}
DESTDIR=%{buildroot} jam -d2 install

install -m644 mk/autoconf/crystal.m4 -D %{buildroot}%{_datadir}/aclocal/crystal.m4

sed -i -e "s#/lib/#/%{_lib}/#g" %{buildroot}%{_bindir}/cs-config
sed -i 's| -L%{_libdir}/python2.5||' %{buildroot}%{_bindir}/cs-config

#multiarch
%multiarch_binaries %{buildroot}%{_bindir}/cs-config*

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{_libdir}/%{name}-1.2
%{_libdir}/%{name}-1.2/*.so
%{_libdir}/%{name}-1.2/*.csplugin
%exclude %{_libdir}/%{name}-1.2/cspython.so
%exclude %{_libdir}/%{name}-1.2/cspython.csplugin
%dir %{_datadir}/%{name}-1.2/bindings
%{_datadir}/%{name}-1.2/build
%{_datadir}/%{name}-1.2/conversion
%{_datadir}/%{name}-1.2/data
%dir %{_sysconfdir}/%{name}-1.2
%config(noreplace) %{_sysconfdir}/%{name}-1.2/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_includedir}/*
%{_datadir}/aclocal/crystal.m4
%{_bindir}/cs-config*
%multiarch %{multiarch_bindir}/cs-config*
%if %{with java}
%exclude %{_includedir}/%{name}-1.2/bindings/java
%endif
%exclude %{_includedir}/%{name}-1.2/bindings/perl
%exclude %{_includedir}/%{name}-1.2/bindings/python

%files doc
%defattr(-,root,root)
%doc %{_docdir}/%{name}-%{version}

%files demos
%defattr(-,root,root)
%{_bindir}/*
%exclude %{_bindir}/cs-config
%exclude %{_bindir}/cs-config-1.2
%exclude %{multiarch_bindir}

%if %{with java}
%files bindings-java
%defattr(-,root,root)
%dir %{_datadir}/%{name}-1.2/bindings
%dir %{_datadir}/%{name}-1.2/bindings/java
%{_datadir}/%{name}-1.2/bindings/java/*
%{_includedir}/%{name}-1.2/bindings/java
%endif

%files bindings-perl
%defattr(-,root,root)
%dir %{_datadir}/%{name}-1.2/bindings/perl5
%{_datadir}/%{name}-1.2/bindings/perl5/*
%{_includedir}/%{name}-1.2/bindings/perl

%files bindings-python
%defattr(-,root,root)
%dir %{_datadir}/%{name}-1.2/bindings/python
%{_libdir}/%{name}-1.2/cspython.so
%{_libdir}/%{name}-1.2/cspython.csplugin
%{_datadir}/%{name}-1.2/bindings/python/*
%{_includedir}/%{name}-1.2/bindings/python
