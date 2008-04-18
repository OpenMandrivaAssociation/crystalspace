Summary:	CrystalSpace free 3d engine
Name:		crystalspace
Version:	1.2
Release:	%mkrel 2
Group:		System/Libraries
License:	LGPLv2+
URL:		http://www.crystalspace3d.org/
Source0:	http://www.crystalspace3d.org/downloads/release/%{name}-src-%{version}.tar.bz2
BuildRequires:	lib3ds-devel >= 1.3.0
BuildRequires:	MesaGLU-devel
BuildRequires:	oggvorbis-devel
BuildRequires:	libmikmod-devel
BuildRequires:	cal3d-devel
BuildRequires:	jpeg-devel
BuildRequires:	zlib-devel
BuildRequires:	ode-devel
BuildRequires:	png-devel
BuildRequires:	openal-devel >= 0.0.6-5mdk
BuildRequires:	mng-devel
BuildRequires:	X11-devel
BuildRequires:	nasm
BuildRequires:	perl-devel
BuildRequires:	wxGTK2.8-devel
BuildRequires:	swig >= 1.3.14
BuildRequires:	bison >= 1.35
BuildRequires:	python-devel
BuildRequires:	ftjam
BuildRequires:	flex
BuildRequires:	doxygen
BuildRequires:	bullet-static-devel
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

%prep
%setup -q -n %{name}-src-%{version}

# work around mikmod not being linked to libdl as it should
sed -i 's/-lmikmod/-lmikmod -ldl/g' configure
# stop configure from adding -L/usr/local/lib to cs-config (and the build)
sed -i 's|-d /usr/local/lib|-d /foobar|' configure

%build
%configure2_5x	\
	--with-mesa \
	--disable-cpu-specific-instructions \
	--enable-linux-joystick \
	--enable-optimize \
	--disable-debug \
	--disable-separate-debug-info \
	--with-pic \
	--with-gnu-ld \
	--enable-mode=optimize \
	--enable-plugins \
	--with-wx

jam -d2 %{_smp_mflags}

%install
rm -rf %{buildroot}
DESTDIR=%{buildroot} jam -d2 install

install -m644 mk/autoconf/crystal.m4 -D %{buildroot}%{_datadir}/aclocal/crystal.m4

sed -i -e "s#/lib/#/%{_lib}/#g" %{buildroot}%{_bindir}/cs-config

#multiarch
%multiarch_binaries %{buildroot}%{_bindir}/cs-config

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{_libdir}/%{name}-%{version}
%{_libdir}/%{name}-%{version}/*.so
%{_datadir}/%{name}-%{version}
%dir %{_sysconfdir}/%{name}-%{version}
%config(noreplace) %{_sysconfdir}/%{name}-%{version}/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_includedir}/*
%{_datadir}/aclocal/crystal.m4
%{_bindir}/cs-config
%multiarch %{multiarch_bindir}/cs-config

%files doc
%defattr(-,root,root)
%doc %{_docdir}/%{name}-%{version}

%files demos
%defattr(-,root,root)
%{_bindir}/*
%exclude %{_bindir}/cs-config
%exclude %{multiarch_bindir}
