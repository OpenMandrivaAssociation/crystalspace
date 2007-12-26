%define	name	crystalspace
%define version 1.2
%define release %mkrel 1

Summary:	CrystalSpace free 3d engine
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		System/Libraries
License:	LGPL
Source0:	%{name}-src-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://crystal.sourceforge.net/
BuildRequires:	lib3ds-devel >= 1.3.0 MesaGLU-devel oggvorbis-devel libmikmod-devel cal3d-devel
BuildRequires:	jpeg-devel zlib-devel ode-devel png-devel openal-devel >= 0.0.6-5mdk
BuildRequires:	mng-devel arts-devel X11-devel nasm perl-devel wxGTK2.8-devel
BuildRequires:	swig >= 1.3.14 bison >= 1.35 python-devel jam

%description
Crystal Space is a free (LGPL) and portable 3D Development Kit
written in C++. It supports: true six degree's of freedom,
colored lighting, mipmapping, portals, mirrors, alpha transparency,
reflective surfaces, 3D sprites (frame based or with skeletal animation),
procedural textures, radiosity, particle systems, halos, volumetric fog,
scripting (using Python or other languages), 8-bit, 16-bit, and 32-bit
display support, OpenGL and software renderering, font support,
hierarchical transformations, etc.

%package	devel
Group:		Development/C
Summary:	Development headers and libraries for %{name}
Requires:	%{name} = %{version}

%description	devel
Development headers and libraries for %{name}

%package	doc
Summary:	Crystalspace documentation
Group:		Development/C
License:	LGPL
Requires:	%{name} = %{version}
Conflicts:      freetds-devel

%description	doc
Crystalspace documentation

%package	demos
Summary:	Crystalspace demos
Group:		Toys
License:	LGPL
Requires:	%{name} = %{version}

%description	demos
Crystalspace demos.

%prep
%setup -q -n %{name}-src-%{version}

%build
%configure2_5x	--with-mesa \
		--with-x \
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
%defattr(-,root,root,755)
%dir %{_libdir}/%{name}-%{version}
%{_libdir}/%{name}-%{version}/*.so
%{_datadir}/%{name}-%{version}
%dir %{_sysconfdir}/%{name}-%{version}
%config(noreplace) %{_sysconfdir}/%{name}-%{version}/*

%files devel
%defattr(-,root,root,755)
%{_libdir}/*.a
%{_includedir}/*
%{_bindir}/python.cex
%{_datadir}/aclocal/crystal.m4
%{_bindir}/cs-config
%multiarch %{multiarch_bindir}/cs-config

%files doc
%defattr(-,root,root,755)
%doc %{_docdir}/%{name}-%{version}

%files demos
%defattr(-,root,root,755)
%{_bindir}/*
%exclude %{_bindir}/cs-config
%exclude %{multiarch_bindir}


