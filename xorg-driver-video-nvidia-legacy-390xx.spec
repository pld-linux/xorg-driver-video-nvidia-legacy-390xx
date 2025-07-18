# TODO
# - drop binary-only nvidia-settings from here, and use nvidia-settings.spec for it
# - kernel-drm is required on never kernels. driver for kernel-longterm not requires drm
#
# Conditional build:
%bcond_without	glvnd		# with GL vendor neutral libs
%bcond_without	system_libglvnd	# do not use system libglvnd
%bcond_without	kernel		# without kernel packages
%bcond_without	userspace	# don't build userspace programs
%bcond_with	settings	# package nvidia-settings here (GPL version of same packaged from nvidia-settings.spec)
%bcond_with	verbose		# verbose build (V=1)

# The goal here is to have main, userspace, package built once with
# simple release number, and only rebuild kernel packages with kernel
# version as part of release number, without the need to bump release
# with every kernel change.
%if 0%{?_pld_builder:1} && %{with kernel} && %{with userspace}
%{error:kernel and userspace cannot be built at the same time on PLD builders}
exit 1
%endif

%if %{with glvnd}
%define		vulkan_lib	libGLX_nvidia.so.0
%else
%define		vulkan_lib	libGL.so.1
%endif

%define		_enable_debug_packages	0

%define		no_install_post_check_so 1

%define		rel	13
%define		pname	xorg-driver-video-nvidia-legacy-390xx
Summary:	Linux Drivers for nVidia GeForce/Quadro Chips
Summary(hu.UTF-8):	Linux meghajtók nVidia GeForce/Quadro chipekhez
Summary(pl.UTF-8):	Sterowniki do kart graficznych nVidia GeForce/Quadro
Name:		%{pname}%{?_pld_builder:%{?with_kernel:-kernel}}%{_alt_kernel}
# when updating version here, keep nvidia-settings.spec in sync as well
Version:	390.157
Release:	%{rel}%{?_pld_builder:%{?with_kernel:@%{_kernel_ver_str}}}
Epoch:		1
License:	nVidia Binary
Group:		X11
Source0:	https://us.download.nvidia.com/XFree86/Linux-x86/%{version}/NVIDIA-Linux-x86-%{version}.run
# Source0-md5:	0975ee17f9c690555dfb2a342a0138b8
Source1:	https://us.download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}-no-compat32.run
# Source1-md5:	405c2220d5d3711e9f298c871e8d66ee
Source2:	%{pname}-xinitrc.sh
Source3:	gl.pc.in
Source4:	10-nvidia.conf
Source5:	10-nvidia-modules.conf
Patch0:		X11-driver-nvidia-GL.patch
Patch1:		X11-driver-nvidia-desktop.patch
Patch2:		kenrel-6.2.patch
Patch3:		kernel-6.3.patch
Patch4:		kernel-6.3-uvm.patch
Patch5:		kernel-6.4.patch
Patch6:		kernel-6.5-garbage-collect-all-references-to-get_user.patch
Patch7:		kernel-6.5-handle-get_user_pages-vmas-argument-remova.patch
Patch8:		kernel-6.5-handle-get_user_pages-vmas-argument-removal-x8664.patch
Patch9:		kernel-6.6-backport-drm_gem_prime_handle_to_fd-changes-from-470.patch
Patch10:	kernel-6.8.patch
Patch11:	kernel-6.10.patch
Patch12:	gcc14.patch
Patch13:	kernel-6.12.patch
Patch14:	kernel-6.13.patch
Patch15:	kernel-6.14.patch
Patch16:	gcc15.patch
Patch17:	kernel-6.15.patch
URL:		https://www.nvidia.com/en-us/drivers/unix/
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
%{?with_kernel:%{expand:%buildrequires_kernel kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2}}
BuildRequires:	sed >= 4.0
BuildConflicts:	XFree86-nvidia
Requires:	%{pname}-libs = %{epoch}:%{version}-%{rel}
Requires:	xorg-xserver-server
Requires:	xorg-xserver-server(videodrv-abi) <= 25.2
Requires:	xorg-xserver-server(videodrv-abi) >= 2.0
Provides:	ocl-icd(nvidia)
Provides:	ocl-icd-driver
Provides:	vulkan(icd) = 1.0.65
Provides:	xorg-driver-video
Provides:	xorg-xserver-module(glx)
Obsoletes:	XFree86-driver-nvidia < 1.0.5336-4
Obsoletes:	XFree86-nvidia < 1.0
Conflicts:	XFree86-OpenGL-devel <= 4.2.0-3
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{pname}-%{version}-root-%(id -u -n)

# libnvidia-encode.so.*.* links with libnvcuvid.so instead of libnvcuvid.so.1
%define		_noautoreq	libnvcuvid.so

%description
This driver set adds improved 2D functionality to the Xorg X server as
well as high performance OpenGL acceleration, AGP support, support for
most flat panels, and 2D multiple monitor support.

Supported hardware:
- GeForce 400/400M series (excluding 405)
- GeForce 500/500M series
- GeForce 600/600M series
- GeForce 700/700M series
- GeForce 800M series
- GeForce 900/900M series
- GeForce 10 series (excluding GT 1010)
- GeForce 10 mobile series
- GeForce MX100 series
- GeForce TITAN series (GTX TITAN Z/GTX TITAN Black/GTX TITAN/
  GTX TITAN X)
- NVIDIA TITAN series (X/Xp/V)
- NVS series (NVS 310/NVS 315/NVS 510/NVS 810)
- NVS mobile series (NVS 4200M/NVS 5200M/NVS 5400M)
- Quadro SDI
- Quadro Sync series (G-Sync II/Sync/Sync II)
- Quadro NVS series (NVS 310/NVS 315/NVS 510/NVS 810)
- Quadro NVS mobile series (NVS 4200M/NVS 5200M/NVS 5400M)
- Quadro Blade/Embedded series
- Quadro series (excluding P2200 and 400)
- Quadro mobile series (excluding T*/P520)

%description -l hu.UTF-8
Ez a meghajtó kibővíti az Xorg X szerver 2D működését OpenGL
gyorsítással, AGP támogatással és támogatja a több monitort.

Támogatott hardverek:
- GeForce 400/400M series (- 405)
- GeForce 500/500M series
- GeForce 600/600M series
- GeForce 700/700M series
- GeForce 800M series
- GeForce 900/900M series
- GeForce 10 series (- GT 1010)
- GeForce 10 mobile series
- GeForce MX100 series
- GeForce TITAN series (GTX TITAN Z/GTX TITAN Black/GTX TITAN/
  GTX TITAN X)
- NVIDIA TITAN series (X/Xp/V)
- NVS series (NVS 310/NVS 315/NVS 510/NVS 810)
- NVS mobile series (NVS 4200M/NVS 5200M/NVS 5400M)
- Quadro SDI
- Quadro Sync series (G-Sync II/Sync/Sync II)
- Quadro NVS series (NVS 310/NVS 315/NVS 510/NVS 810)
- Quadro NVS mobile series (NVS 4200M/NVS 5200M/NVS 5400M)
- Quadro Blade/Embedded series
- Quadro series (- P2200 and 400)
- Quadro mobile series (- T*/P520)

%description -l pl.UTF-8
Usprawnione sterowniki dla kart graficznych nVidia do serwera Xorg,
dające wysokowydajną akcelerację OpenGL, obsługę AGP i wielu monitorów
2D.

Obsługują karty:
- GeForce serii 400/400M (oprócz 405)
- GeForce serii 500/500M
- GeForce serii 600/600M
- GeForce serii 700/700M
- GeForce serii 800M
- GeForce serii 900/900M
- GeForce serii 10 (oprócz GT 1010)
- GeForce serii 10 mobile
- GeForce serii MX100
- GeForce serii TITAN (GTX TITAN Z/GTX TITAN Black/GTX TITAN/
  GTX TITAN X)
- NVIDIA serii TITAN (X/Xp/V)
- serii NVS (NVS 310/NVS 315/NVS 510/NVS 810)
- serii NVS mobile (NVS 4200M/NVS 5200M/NVS 5400M)
- Quadro SDI
- Quadro serii Sync (G-Sync II/Sync/Sync II)
- Quadro serii NVS (NVS 310/NVS 315/NVS 510/NVS 810)
- Quadro serii NVS mobile (NVS 4200M/NVS 5200M/NVS 5400M)
- Quadro serii Blade/Embedded
- Quadro (oprócz P2200 and 400)
- Quadro mobile (oprócz T*/P520)

%package libs
Summary:	OpenGL (GL and GLX) Nvidia libraries
Summary(pl.UTF-8):	Biblioteki OpenGL (GL i GLX) Nvidia
Group:		X11/Development/Libraries
Requires(post,postun):	/sbin/ldconfig
%if %{with glvnd} && %{with system_libglvnd}
Requires:	libglvnd >= 1.3.4-2
Requires:	libglvnd-libGL >= 1.3.4-2
Requires:	libglvnd-libGLES >= 1.3.4-2
%endif
Requires:	libvdpau >= 0.3
Provides:	OpenGL = 4.3
Provides:	OpenGL-GLX = 1.4
%if %{with glvnd} && %{with system_libglvnd}
Provides:	glvnd(EGL)%{?_isa}
Provides:	glvnd(GL)%{?_isa}
Provides:	glvnd(GLES)%{?_isa}
%endif
Obsoletes:	X11-OpenGL-core < 1:7.0.0
Obsoletes:	X11-OpenGL-libGL < 1:7.0.0
Obsoletes:	XFree86-OpenGL-core < 1:7.0.0
Obsoletes:	XFree86-OpenGL-libGL < 1:7.0.0
%if %{with glvnd} && %{with system_libglvnd}
Obsoletes:	xorg-driver-video-nvidia-legacy-390xx-devel < 390.143-2
%endif

%description libs
NVIDIA OpenGL (GL and GLX only) implementation libraries.

%description libs -l pl.UTF-8
Implementacja OpenGL (tylko GL i GLX) firmy NVIDIA.

%package devel
Summary:	OpenGL (GL and GLX) header files
Summary(hu.UTF-8):	OpenGL (GL és GLX) fejléc fájlok
Summary(pl.UTF-8):	Pliki nagłówkowe OpenGL (GL i GLX)
Group:		X11/Development/Libraries
Requires:	%{pname}-libs = %{epoch}:%{version}-%{rel}
Provides:	OpenGL-GLX-devel = 1.4
Provides:	OpenGL-devel = 3.0
Obsoletes:	X11-OpenGL-devel-base < 1:7.0.0
Obsoletes:	XFree86-OpenGL-devel-base < 1:7.0.0
Obsoletes:	XFree86-driver-nvidia-devel < 1.0.5336-4
Conflicts:	XFree86-OpenGL-devel < 4.3.99.902-0.3

%description devel
OpenGL header files (GL and GLX only) for NVIDIA OpenGL
implementation.

%description devel -l hu.UTF-8
OpenGL fejléc fájlok (csak GL és GLX) NVIDIA OpenGL implementációhoz.

%description devel -l pl.UTF-8
Pliki nagłówkowe OpenGL (tylko GL i GLX) dla implementacji OpenGL
firmy NVIDIA.

%package doc
Summary:	Documentation for NVIDIA Graphics Driver
Summary(pl.UTF-8):	Dokumentacja do sterownika graficznego NVIDIA
Group:		Documentation
BuildArch:	noarch

%description doc
NVIDIA Accelerated Linux Graphics Driver README and Installation
Guide.

%description doc -l pl.UTF-8
Plik README oraz przewodnik instalacji do akcelerowanego sterownika
graficznego NVIDIA dla Linuksa.

%package progs
Summary:	Tools for advanced control of nVidia graphic cards
Summary(hu.UTF-8):	Eszközök az nVidia grafikus kártyák beállításához
Summary(pl.UTF-8):	Narzędzia do zarządzania kartami graficznymi nVidia
Group:		Applications/System
Requires:	%{pname} = %{epoch}:%{version}
Suggests:	pkgconfig
Obsoletes:	XFree86-driver-nvidia-progs < 1.0.5336-4

%description progs
Tools for advanced control of nVidia graphic cards.

%description progs -l hu.UTF-8
Eszközök az nVidia grafikus kártyák beállításához.

%description progs -l pl.UTF-8
Narzędzia do zarządzania kartami graficznymi nVidia.

%define	kernel_pkg()\
%package -n kernel%{_alt_kernel}-video-nvidia-legacy-390xx\
Summary:	nVidia kernel module for nVidia Architecture support\
Summary(de.UTF-8):	Das nVidia-Kern-Modul für die nVidia-Architektur-Unterstützung\
Summary(hu.UTF-8):	nVidia Architektúra támogatás Linux kernelhez.\
Summary(pl.UTF-8):	Moduł jądra dla obsługi kart graficznych nVidia\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
Requires:	dev >= 2.7.7-10\
%requires_releq_kernel\
%if %{_kernel_version_code} >= %{_kernel_version_magic 3 10 0}\
Requires:	%{releq_kernel -n drm}\
%endif\
Requires(postun):	%releq_kernel\
Requires:	%{pname} = %{epoch}:%{version}\
Provides:	X11-driver-nvidia(kernel)\
Obsoletes:	XFree86-nvidia-kernel < 1.0.5336-4\
\
%description -n kernel%{_alt_kernel}-video-nvidia-legacy-390xx\
nVidia Architecture support for Linux kernel.\
\
%description -n kernel%{_alt_kernel}-video-nvidia-legacy-390xx -l de.UTF-8\
Die nVidia-Architektur-Unterstützung für den Linux-Kern.\
\
%description -n kernel%{_alt_kernel}-video-nvidia-legacy-390xx -l hu.UTF-8\
nVidia Architektúra támogatás Linux kernelhez.\
\
%description -n kernel%{_alt_kernel}-video-nvidia-legacy-390xx -l pl.UTF-8\
Obsługa architektury nVidia dla jądra Linuksa. Pakiet wymagany przez\
sterownik nVidii dla Xorg/XFree86.\
\
%if %{with kernel}\
%files -n kernel%{_alt_kernel}-video-nvidia-legacy-390xx\
%defattr(644,root,root,755)\
/lib/modules/%{_kernel_ver}/misc/*.ko*\
%endif\
\
%post	-n kernel%{_alt_kernel}-video-nvidia-legacy-390xx\
%depmod %{_kernel_ver}\
\
%postun	-n kernel%{_alt_kernel}-video-nvidia-legacy-390xx\
%depmod %{_kernel_ver}\
%{nil}

%define build_kernel_pkg()\
cd kernel\
%{__make} SYSSRC=%{_kernelsrcdir} clean\
%{__make} SYSSRC=%{_kernelsrcdir} CONFIG_OBJTOOL_WERROR=n IGNORE_CC_MISMATCH=1 NV_VERBOSE=1 CC=%{__cc} module\
cd ..\
%install_kernel_modules -D installed -m kernel/nvidia,kernel/nvidia-drm,kernel/nvidia-modeset -d misc\
%ifarch %{x8664}\
%install_kernel_modules -D installed -m kernel/nvidia-uvm -d misc\
%endif\
%{nil}

%{?with_kernel:%{expand:%create_kernel_packages}}

%prep
cd %{_builddir}
rm -rf NVIDIA-Linux-x86*-%{version}*
%ifarch %{ix86}
/bin/sh %{SOURCE0} --extract-only
%setup -qDT -n NVIDIA-Linux-x86-%{version}
%else
/bin/sh %{SOURCE1} --extract-only
%setup -qDT -n NVIDIA-Linux-x86_64-%{version}-no-compat32
%endif
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1
%ifarch %{x8664}
%patch -P 4 -p1
%endif
%patch -P 5 -p1
%patch -P 6 -p1
%patch -P 7 -p1
%ifarch %{x8664}
%patch -P 8 -p1
%endif
%patch -P 9 -p1
%patch -P 10 -p1
%patch -P 11 -p1
%patch -P 12 -p1
%patch -P 13 -p1
%patch -P 14 -p1
%patch -P 15 -p1
%patch -P 16 -p1
%patch -P 17 -p1

%build
%{?with_kernel:%{expand:%build_kernel_packages}}

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d $RPM_BUILD_ROOT%{_libdir}/{nvidia,xorg/modules/{drivers,extensions/nvidia}} \
	$RPM_BUILD_ROOT{%{_includedir}/GL,%{_libdir}/vdpau,%{_bindir},%{_mandir}/man1} \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},/etc/X11/xinit/xinitrc.d} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{OpenCL/vendors,ld.so.conf.d,X11/xorg.conf.d} \
	$RPM_BUILD_ROOT%{_datadir}/{glvnd/egl_vendor.d,nvidia,vulkan/icd.d}

%if %{with settings}
install -p nvidia-settings $RPM_BUILD_ROOT%{_bindir}
cp -p nvidia-settings.1* $RPM_BUILD_ROOT%{_mandir}/man1
cp -p nvidia-settings.desktop $RPM_BUILD_ROOT%{_desktopdir}
cp -p nvidia-settings.png $RPM_BUILD_ROOT%{_pixmapsdir}
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/X11/xinit/xinitrc.d/nvidia-settings.sh
%endif

install -p nvidia-{smi,xconfig,bug-report.sh} $RPM_BUILD_ROOT%{_bindir}
install -p nvidia-cuda-mps-{control,server} $RPM_BUILD_ROOT%{_bindir}
cp -p nvidia-{smi,xconfig,cuda-mps-control}.1* $RPM_BUILD_ROOT%{_mandir}/man1
install -p nvidia.icd $RPM_BUILD_ROOT%{_sysconfdir}/OpenCL/vendors

install %{SOURCE4} $RPM_BUILD_ROOT/etc/X11/xorg.conf.d
install %{SOURCE5} $RPM_BUILD_ROOT/etc/X11/xorg.conf.d
sed -i -e 's|@@LIBDIR@@|%{_libdir}|g' $RPM_BUILD_ROOT/etc/X11/xorg.conf.d/10-nvidia-modules.conf
install -p nvidia-drm-outputclass.conf $RPM_BUILD_ROOT/etc/X11/xorg.conf.d/10-nvidia-drm-outputclass.conf

install -p nvidia-application-profiles-%{version}-key-documentation $RPM_BUILD_ROOT%{_datadir}/nvidia
install -p nvidia-application-profiles-%{version}-rc $RPM_BUILD_ROOT%{_datadir}/nvidia

for f in \
%if %{with glvnd}
%if %{without system_libglvnd}
	libGL.so.1.7.0				\
	libGLX.so.0				\
	libOpenGL.so.0				\
	libGLdispatch.so.0			\
	libGLESv1_CM.so.1.2.0			\
	libGLESv2.so.2.1.0			\
	libEGL.so.1.1.0				\
%endif
	libGLX_nvidia.so.%{version}		\
	libEGL_nvidia.so.%{version}		\
	libGLESv1_CM_nvidia.so.%{version}	\
	libGLESv2_nvidia.so.%{version}		\
	libnvidia-egl-wayland.so.1.0.2		\
	libnvidia-eglcore.so.%{version}		\
%else
	libGL.so.%{version}			\
%endif
	libcuda.so.%{version}			\
	libnvcuvid.so.%{version}		\
	libnvidia-cfg.so.%{version}		\
	libnvidia-compiler.so.%{version}	\
	libnvidia-encode.so.%{version}		\
	libnvidia-fatbinaryloader.so.%{version}	\
	libnvidia-fbc.so.%{version}	\
	libnvidia-glcore.so.%{version}		\
	libnvidia-glsi.so.%{version}		\
	libnvidia-ifr.so.%{version}		\
	libnvidia-ml.so.%{version}		\
	libnvidia-opencl.so.%{version}		\
	libnvidia-ptxjitcompiler.so.%{version}	\
	tls/libnvidia-tls.so.%{version}		\
; do
	install -p $f $RPM_BUILD_ROOT%{_libdir}/nvidia
done

install -p libvdpau_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/vdpau

install -p libglx.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia
ln -s libglx.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia/libglx.so
install -p nvidia_drv.so $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/nvidia_drv.so.%{version}
ln -s nvidia_drv.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/nvidia_drv.so
install -p libnvidia-wfb.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia
ln -s libnvidia-wfb.so.1 $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia/libnvidia-wfb.so

/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}/nvidia
/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia

cp -p gl*.h $RPM_BUILD_ROOT%{_includedir}/GL

ln -sf libvdpau_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/vdpau/libvdpau_nvidia.so.1

%ifarch %{x8664}
echo %{_libdir}/nvidia >$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia64.conf
echo %{_libdir}/vdpau >>$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia64.conf
%else
echo %{_libdir}/nvidia >$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia.conf
echo %{_libdir}/vdpau >>$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia.conf
%endif

# OpenGL ABI for Linux compatibility
%if %{with glvnd}
%if %{without system_libglvnd}
ln -sf libGL.so.1.7.0 $RPM_BUILD_ROOT%{_libdir}/nvidia/libGL.so.1
ln -sf libGL.so.1 $RPM_BUILD_ROOT%{_libdir}/nvidia/libGL.so
ln -sf libGLX.so.0 $RPM_BUILD_ROOT%{_libdir}/nvidia/libGLX.so
ln -sf libOpenGL.so.0 $RPM_BUILD_ROOT%{_libdir}/nvidia/libOpenGL.so
ln -sf libGLESv1_CM.so.1.2.0 $RPM_BUILD_ROOT%{_libdir}/nvidia/libGLESv1_CM.so.1
ln -sf libGLESv1_CM.so.1 $RPM_BUILD_ROOT%{_libdir}/nvidia/libGLESv1_CM.so
ln -sf libGLESv2.so.2.1.0 $RPM_BUILD_ROOT%{_libdir}/nvidia/libGLESv2.so.2
ln -sf libGLESv2.so.2 $RPM_BUILD_ROOT%{_libdir}/nvidia/libGLESv2.so
ln -sf libEGL.so.1.1.0 $RPM_BUILD_ROOT%{_libdir}/nvidia/libEGL.so.1
ln -sf libEGL.so.1 $RPM_BUILD_ROOT%{_libdir}/nvidia/libEGL.so
%endif
ln -sf libGLX_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/nvidia/libGLX_nvidia.so.0
ln -sf libGLX_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/nvidia/libGLX_indirect.so.0
ln -sf libEGL_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/nvidia/libEGL_nvidia.so.0
ln -sf libGLESv1_CM_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/nvidia/libGLESv1_CM_nvidia.so.1
ln -sf libGLESv2_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/nvidia/libGLESv2_nvidia.so.2

install -p 10_nvidia.json $RPM_BUILD_ROOT%{_datadir}/glvnd/egl_vendor.d
%else
ln -sf libGL.so.%{version} $RPM_BUILD_ROOT%{_libdir}/nvidia/libGL.so.1
ln -sf libGL.so.1 $RPM_BUILD_ROOT%{_libdir}/nvidia/libGL.so
%endif
ln -sf libcuda.so.1 $RPM_BUILD_ROOT%{_libdir}/nvidia/libcuda.so
ln -sf libnvcuvid.so.1 $RPM_BUILD_ROOT%{_libdir}/nvidia/libnvcuvid.so

sed 's!__NV_VK_ICD__!%{vulkan_lib}!g' nvidia_icd.json.template > $RPM_BUILD_ROOT%{_datadir}/vulkan/icd.d/nvidia_icd.json
%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT
cp -a installed/* $RPM_BUILD_ROOT
%endif

install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
sed -e '
	s|@@prefix@@|%{_prefix}|g;
	s|@@libdir@@|%{_libdir}|g;
	s|@@includedir@@|%{_includedir}|g;
	s|@@version@@|%{version}|g' < %{SOURCE3} \
	> $RPM_BUILD_ROOT%{_pkgconfigdir}/gl.pc

%clean
rm -rf $RPM_BUILD_ROOT

%post
cat << 'EOF'
NOTE: You must also install kernel module for this driver to work
  kernel%{_alt_kernel}-video-nvidia-legacy-390xx-%{version}

EOF

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc LICENSE NVIDIA_Changelog README.txt
%dir %{_libdir}/xorg/modules/extensions/nvidia
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/nvidia/libnvidia-wfb.so.*.*
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/nvidia/libnvidia-wfb.so.1
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/nvidia/libnvidia-wfb.so
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/nvidia/libglx.so.*
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/nvidia/libglx.so
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/nvidia_drv.so.*
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/nvidia_drv.so
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/X11/xorg.conf.d/10-nvidia.conf
%{_sysconfdir}/X11/xorg.conf.d/10-nvidia-modules.conf
%{_sysconfdir}/X11/xorg.conf.d/10-nvidia-drm-outputclass.conf
%dir %{_datadir}/nvidia
%{_datadir}/nvidia/nvidia-application-profiles-%{version}-key-documentation
%{_datadir}/nvidia/nvidia-application-profiles-%{version}-rc

%files libs
%defattr(644,root,root,755)
%dir %{_sysconfdir}/OpenCL
%dir %{_sysconfdir}/OpenCL/vendors
%{_sysconfdir}/OpenCL/vendors/nvidia.icd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ld.so.conf.d/nvidia*.conf
%dir %{_libdir}/nvidia
%if %{with glvnd}
%if %{without system_libglvnd}
%attr(755,root,root) %{_libdir}/nvidia/libGL.so.1.7.0
%attr(755,root,root) %ghost %{_libdir}/nvidia/libGL.so.1
%attr(755,root,root) %{_libdir}/nvidia/libGL.so
%attr(755,root,root) %{_libdir}/nvidia/libGLX.so.0
%attr(755,root,root) %{_libdir}/nvidia/libOpenGL.so.0
%attr(755,root,root) %{_libdir}/nvidia/libGLdispatch.so.0
%attr(755,root,root) %{_libdir}/nvidia/libGLESv1_CM.so.1.2.0
%attr(755,root,root) %ghost %{_libdir}/nvidia/libGLESv1_CM.so.1
%attr(755,root,root) %{_libdir}/nvidia/libGLESv2.so.2.1.0
%attr(755,root,root) %ghost %{_libdir}/nvidia/libGLESv2.so.2
%attr(755,root,root) %{_libdir}/nvidia/libEGL.so.1.1.0
%attr(755,root,root) %ghost %{_libdir}/nvidia/libEGL.so.1
%endif
%attr(755,root,root) %ghost %{_libdir}/nvidia/libEGL_nvidia.so.0
%attr(755,root,root) %{_libdir}/nvidia/libEGL_nvidia.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libGLESv1_CM_nvidia.so.1
%attr(755,root,root) %{_libdir}/nvidia/libGLESv1_CM_nvidia.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libGLESv2_nvidia.so.2
%attr(755,root,root) %{_libdir}/nvidia/libGLESv2_nvidia.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libGLX_indirect.so.0
%attr(755,root,root) %ghost %{_libdir}/nvidia/libGLX_nvidia.so.0
%attr(755,root,root) %{_libdir}/nvidia/libGLX_nvidia.so.*.*
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-egl-wayland.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libnvidia-egl-wayland.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-eglcore.so.*.*
%else
%attr(755,root,root) %{_libdir}/nvidia/libGL.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libGL.so.1
%attr(755,root,root) %{_libdir}/nvidia/libGL.so
%endif
%attr(755,root,root) %{_libdir}/nvidia/libcuda.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libcuda.so.1
%attr(755,root,root) %{_libdir}/nvidia/libcuda.so
%attr(755,root,root) %{_libdir}/nvidia/libnvcuvid.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libnvcuvid.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvcuvid.so
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-cfg.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libnvidia-cfg.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-compiler.so.*.*
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-encode.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libnvidia-encode.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-fatbinaryloader.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libnvidia-fbc.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-fbc.so.*.*
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-glcore.so.*.*
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-glsi.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libnvidia-ifr.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-ifr.so.*.*
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-ptxjitcompiler.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-ml.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libnvidia-ml.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-opencl.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libnvidia-opencl.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-ptxjitcompiler.so.*.*
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-tls.so.*.*
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_nvidia.so.*.*
%attr(755,root,root) %ghost %{_libdir}/vdpau/libvdpau_nvidia.so.1
%if %{with glvnd}
%{_datadir}/glvnd/egl_vendor.d/10_nvidia.json
%endif
%{_datadir}/vulkan/icd.d/nvidia_icd.json

%if %{without glvnd} || %{without system_libglvnd}
%files devel
%defattr(644,root,root,755)
%if %{with glvnd}
%attr(755,root,root) %{_libdir}/nvidia/libGLX.so
%attr(755,root,root) %{_libdir}/nvidia/libOpenGL.so
%attr(755,root,root) %{_libdir}/nvidia/libGLESv1_CM.so
%attr(755,root,root) %{_libdir}/nvidia/libGLESv2.so
%attr(755,root,root) %{_libdir}/nvidia/libEGL.so
%endif
%dir %{_includedir}/GL
%{_includedir}/GL/gl.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glxext.h
%{_pkgconfigdir}/gl.pc
%endif

%files doc
%defattr(644,root,root,755)
%doc html/*

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nvidia-bug-report.sh
%attr(755,root,root) %{_bindir}/nvidia-cuda-mps-control
%attr(755,root,root) %{_bindir}/nvidia-cuda-mps-server
%attr(755,root,root) %{_bindir}/nvidia-smi
%attr(755,root,root) %{_bindir}/nvidia-xconfig
%{_mandir}/man1/nvidia-cuda-mps-control.1*
%{_mandir}/man1/nvidia-smi.1*
%{_mandir}/man1/nvidia-xconfig.1*
%if %{with settings}
%attr(755,root,root) /etc/X11/xinit/xinitrc.d/*.sh
%attr(755,root,root) %{_bindir}/nvidia-settings
%{_mandir}/man1/nvidia-settings.1*
%{_desktopdir}/nvidia-settings.desktop
%{_pixmapsdir}/nvidia-settings.png
%endif
%endif
