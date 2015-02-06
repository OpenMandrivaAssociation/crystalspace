%define major 2.0
%define libname %mklibname %{name} %{major}

Summary:	CrystalSpace free 3d engine
Name:		crystalspace
Version:	%{major}
Release:	3
Group:		System/Libraries
License:	LGPLv2+
Url:		http://www.crystalspace3d.org/
Source0:	http://www.crystalspace3d.org/downloads/release/%{name}-src-%{version}.tar.bz2
Patch0:		crystalspace-2.0-gcc47.patch
BuildRequires:	bison
BuildRequires:	doxygen
BuildRequires:	flex
BuildRequires:	ftjam
BuildRequires:	icoutils
BuildRequires:	imagemagick
BuildRequires:	libtool
BuildRequires:	nasm
BuildRequires:	swig >= 1.3.14
BuildRequires:	tetex-dvipdfm
BuildRequires:	tetex-dvips
BuildRequires:	texinfo
BuildRequires:	perl(Template::Base)
BuildRequires:	jpeg-devel
BuildRequires:	mng-devel
BuildRequires:	perl-devel
BuildRequires:	wxgtku2.8-devel
BuildRequires:	lib3ds-devel >= 1.3.0
BuildRequires:	libmikmod-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(bullet)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(cairomm-1.0)
BuildRequires:	pkgconfig(cal3d)
BuildRequires:	pkgconfig(CEGUI)
BuildRequires:	pkgconfig(cppunit)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(lcms)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(ode)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(zlib)
# Dropped in 2.0 upstream:
Obsoletes:	crystalspace-bindings-java < 2.0
Obsoletes:	crystalspace-bindings-perl < 2.0

%description
Crystal Space is a free (LGPL) and portable 3D Development Kit
written in C++. It supports: true six degree's of freedom,
colored lighting, mipmapping, portals, mirrors, alpha transparency,
reflective surfaces, 3D sprites (frame based or with skeletal animation),
procedural textures, radiosity, particle systems, halos, volumetric fog,
scripting (using Python or other languages), 8-bit, 16-bit, and 32-bit
display support, OpenGL and software renderering, font support,
hierarchical transformations, etc.

%files
%dir %{_libdir}/%{name}-%{major}
%{_libdir}/%{name}-%{major}/*.so
%{_libdir}/%{name}-%{major}/*.csplugin
%exclude %{_libdir}/%{name}-%{major}/cspython.so
%exclude %{_libdir}/%{name}-%{major}/cspython.csplugin
%dir %{_datadir}/%{name}-%{major}/bindings
%{_datadir}/%{name}-%{major}/build
%{_datadir}/%{name}-%{major}/conversion
%{_datadir}/%{name}-%{major}/data
%dir %{_sysconfdir}/%{name}-%{major}
%config(noreplace) %{_sysconfdir}/%{name}-%{major}/*
%{_sysconfdir}/profile.d/90crystalspace.sh

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared libraries for %{name}
Group:		System/Libraries
Requires:	%{name} = %{EVRD}

%description -n %{libname}
Shared libraries for %{name}.

%files -n %{libname}
%{_libdir}/libcrystalspace*-%{major}.so

#----------------------------------------------------------------------------

%package devel
Summary:	Development headers and libraries for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}

%description devel
Development headers and libraries for %{name}.

%files devel
%{_includedir}/*
%{_datadir}/aclocal/crystal.m4
%{_bindir}/cs-config*
%exclude %{_includedir}/%{name}-%{major}/bindings/python

#----------------------------------------------------------------------------

%package doc
Summary:	Crystalspace documentation
Group:		Development/C
Requires:	%{name} = %{EVRD}
Conflicts:	freetds-devel
BuildArch:	noarch

%description doc
Crystalspace documentation.

%files doc
%doc %{_docdir}/%{name}-%{version}

#----------------------------------------------------------------------------

%package demos
Summary:	Crystalspace demos
Group:		Toys
Requires:	%{name} = %{EVRD}

%description demos
Crystalspace demos.

%files demos
%{_bindir}/*
%exclude %{_bindir}/cs-config
%exclude %{_bindir}/cs-config-%{major}

#----------------------------------------------------------------------------

%package	bindings-python
Summary:	Python bindings for Crystal Space free 3D SDK
Group:		Development/Python
Requires:	%{name} = %{EVRD}

%description bindings-python
Python bindings for Crystal Space free 3D SDK.

%files bindings-python
%{python_sitearch}/cspace.pth
%dir %{_datadir}/%{name}-%{major}/bindings/python
%{_libdir}/%{name}-%{major}/cspython.so
%{_libdir}/%{name}-%{major}/cspython.csplugin
%{_datadir}/%{name}-%{major}/bindings/python/*
%{_includedir}/%{name}-%{major}/bindings/python

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-src-%{version}
%patch0 -p1

%build
CXXFLAGS="%{optflags} -fpermissive" \
%configure2_5x	\
	--enable-cpu-specific-optimizations=no \
	--with-mesa \
	--disable-optimize \
	--disable-debug \
	--disable-separate-debug-info \
	--without-Cg \
	--with-wx \
	--disable-meta-info-embedding

jam -d2 %{_smp_mflags}

%install
DESTDIR=%{buildroot} jam -d2 install

# Fix unstripped-binary-or-object
chmod 0755 %{buildroot}%{_libdir}/*.so

install -m644 mk/autoconf/crystal.m4 -D %{buildroot}%{_datadir}/aclocal/crystal.m4

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
echo "export CRYSTAL_PLUGIN=%{_libdir}/%{name}-%{major}" > %{buildroot}%{_sysconfdir}/profile.d/90crystalspace.sh
echo "export CRYSTAL_CONFIG=/%{name}-%{major}/" >> %{buildroot}%{_sysconfdir}/profile.d/90crystalspace.sh

