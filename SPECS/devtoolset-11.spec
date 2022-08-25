%global package_speccommit 7b062e4a8046aa79520dbab62886dfa4d41800ed
%global usver 11.0
%global xsver 4
%global xsrel %{xsver}%{?xscount}%{?xshash}

%global __python /usr/bin/python3
%global scl devtoolset-11


#--- begin macros.scl.inc
# Our definitions
%global __python %{__python2}

# From devtoolset-11-build
%global scl devtoolset-11
%undefine nfsmountable
%define enable_devtoolset11 %global ___build_pre %{___build_pre}; source scl_source enable devtoolset-11 || :

# From /etc/rpm/macros.scl
# scl-utils RPM macros
#
# Copyright (C) 2012 Red Hat, Inc.
#   Written by Jindrich Novy <jnovy@redhat.com>.

%define scl_debug() %{expand:
%define old_debug %{lua:print(rpm.expand("%{debug_package}"):len())}
%define debug_package %{expand:
%if "%{?old_debug}" == "0"
       %{expand: %{nil}}
%else
%if "%{?scl}%{!?scl:0}" == "%{pkg_name}"
        %{expand: %{nil}}
%else
%ifnarch noarch
%package debuginfo
Summary: Debug information for package %{name}
Group: Development/Debug
AutoReqProv: 0
Requires: %scl_runtime
Provides: scl-package(%scl)
%{lua:
        debuginfo=tonumber(rpm.expand("%{old_debug}"))
        if debuginfo > 0 then
                rpm.define("__debug_package 1")
        end
}
%description debuginfo
This package provides debug information for package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.
%files debuginfo -f debugfiles.list
%defattr(-,root,root)
%endif
%endif
%endif
%{nil}}}

%define scl_package() %{expand:%{!?_root_prefix:
%global pkg_name		%1
%global scl_name		%{scl}
%global scl_prefix		%{scl}-
%global scl_runtime		%{scl}-runtime
%{!?_scl_prefix:		%global _scl_prefix /opt/rh}
%global _scl_scripts		%{_scl_prefix}/%{scl}
%global _scl_root		%{_scl_prefix}/%{scl}/root
%global _root_prefix		%{_prefix}
%global _root_exec_prefix	%{_root_prefix}
%global _root_bindir		%{_exec_prefix}/bin
%global _root_sbindir		%{_exec_prefix}/sbin
%global _root_libexecdir	%{_exec_prefix}/libexec
%global _root_datadir		%{_prefix}/share
%global _root_sysconfdir	%{_sysconfdir}
%global _root_sharedstatedir	%{_prefix}/com
%global _root_localstatedir	%{_localstatedir}
%global _root_libdir		%{_exec_prefix}/%{_lib}
%global _root_includedir	%{_prefix}/include
%global _root_infodir		%{_datadir}/info
%global _root_mandir		%{_datadir}/man
%global _root_initddir		%{_sysconfdir}/rc.d/init.d
%global _prefix			%{_scl_root}/usr
%global _exec_prefix		%{_prefix}
%global _bindir			%{_exec_prefix}/bin
%global _sbindir		%{_exec_prefix}/sbin
%global _libexecdir		%{_exec_prefix}/libexec
%global _datadir		%{_prefix}/share
%global _sysconfdir		%{_scl_root}/etc
%{?nfsmountable:		%global _sysconfdir %{_root_sysconfdir}%{_scl_prefix}/%{scl}}
%global _sharedstatedir		%{_scl_root}/var/lib
%{?nfsmountable:		%global _sharedstatedir %{_root_localstatedir}%{_scl_prefix}/%{scl}/lib}
%global _localstatedir		%{_scl_root}/var
%{?nfsmountable:		%global _localstatedir %{_root_localstatedir}%{_scl_prefix}/%{scl}}
%global _libdir			%{_exec_prefix}/%{_lib}
%global _includedir		%{_prefix}/include
%global _infodir		%{_datadir}/info
%global _mandir			%{_datadir}/man
%global _docdir			%{_datadir}/doc
%global _defaultdocdir		%{_docdir}
}
%{?scl_dependency_generators:%scl_dependency_generators}
%global scl_pkg_name		%{scl}-%{pkg_name}
%scl_debug
%global __os_install_post %{expand:
    /usr/lib/rpm/brp-scl-compress %{_scl_root}
    %{!?__debug_package:/usr/lib/rpm/brp-strip %{__strip}
    /usr/lib/rpm/brp-strip-comment-note %{__strip} %{__objdump}
    }
    /usr/lib/rpm/brp-strip-static-archive %{__strip}
    /usr/lib/rpm/brp-scl-python-bytecompile %{__python} %{?_python_bytecompile_errors_terminate_build} %{_scl_root}
    /usr/lib/rpm/brp-python-hardlink
    %{!?__jar_repack:/usr/lib/rpm/redhat/brp-java-repack-jars}
%{nil}}
BuildRequires: scl-utils-build
%if "%{?scl}%{!?scl:0}" == "%{pkg_name}"
Requires: %{scl_runtime}
Provides: scl-package(%{scl})
%endif
%{?scl_package_override:%scl_package_override}
}

%define scl_require()	%{_scl_prefix}/%1/enable, %1
%define scl_require_package() %1-%2
%define scl_files %{expand:
%defattr(-,root,root,-)
%dir %_scl_prefix
%dir %attr(555,root,root) %{_scl_root}
%dir %attr(555,root,root) %{_scl_scripts}
%{_scl_scripts}/enable
%{_root_sysconfdir}/scl/prefixes/%scl
%{_scl_root}/bin
%attr(555,root,root) %{_scl_root}/boot
%{_scl_root}/dev
%dir %{_sysconfdir}
%{_sysconfdir}/X11
%{_sysconfdir}/xdg
%{_sysconfdir}/opt
%{_sysconfdir}/pm
%{_sysconfdir}/xinetd.d
%{_sysconfdir}/skel
%{_sysconfdir}/sysconfig
%{_sysconfdir}/pki
%{_scl_root}/home
%{_scl_root}/lib
%ifarch x86_64 ppc ppc64 ppc64le aarch64 sparc sparc64 s390 s390x
%{_scl_root}/%{_lib}
%endif
%{_scl_root}/media
%dir %{_scl_root}/mnt
%dir %{_scl_root}/opt
%attr(555,root,root) %{_scl_root}/proc
%attr(550,root,root) %{_scl_root}/root
%{_scl_root}/run
%{_scl_root}/sbin
%{_scl_root}/srv
%{_scl_root}/sys
%attr(1777,root,root) %{_scl_root}/tmp
%dir %{_scl_root}/usr
%attr(555,root,root) %{_scl_root}/usr/bin
%{_scl_root}/usr/etc
%{_scl_root}/usr/games
%{_scl_root}/usr/include
%dir %attr(555,root,root) %{_scl_root}/usr/lib
%ifarch x86_64 ppc ppc64 ppc64le aarch64 sparc sparc64 s390 s390x
%attr(555,root,root) %{_scl_root}/usr/%{_lib}
%endif
%{_scl_root}/usr/libexec
%{_scl_root}/usr/local
%attr(555,root,root) %{_scl_root}/usr/sbin
%dir %{_scl_root}/usr/share
%{_scl_root}/usr/share/aclocal
%{_scl_root}/usr/share/applications
%{_scl_root}/usr/share/augeas
%{_scl_root}/usr/share/backgrounds
%{_scl_root}/usr/share/desktop-directories
%{_scl_root}/usr/share/dict
%{_scl_root}/usr/share/doc
%attr(555,root,root) %dir %{_scl_root}/usr/share/empty
%{_scl_root}/usr/share/games
%{_scl_root}/usr/share/ghostscript
%{_scl_root}/usr/share/gnome
%{_scl_root}/usr/share/icons
%{_scl_root}/usr/share/idl
%{_scl_root}/usr/share/info
%dir %{_scl_root}/usr/share/locale
%dir %{_scl_root}/usr/share/man
%{_scl_root}/usr/share/mime-info
%{_scl_root}/usr/share/misc
%{_scl_root}/usr/share/omf
%{_scl_root}/usr/share/pixmaps
%{_scl_root}/usr/share/sounds
%{_scl_root}/usr/share/themes
%{_scl_root}/usr/share/xsessions
%{_scl_root}/usr/share/X11
%{_scl_root}/usr/src
%{_scl_root}/usr/tmp
%dir %{_localstatedir}
%{_localstatedir}/adm
%{_localstatedir}/cache
%{_localstatedir}/db
%{_localstatedir}/empty
%{_localstatedir}/games
%{_localstatedir}/gopher
%{_localstatedir}/lib
%{_localstatedir}/local
%ghost %dir %attr(755,root,root) %{_localstatedir}/lock
%ghost %{_localstatedir}/lock/subsys
%{_localstatedir}/log
%{_localstatedir}/mail
%{_localstatedir}/nis
%{_localstatedir}/opt
%{_localstatedir}/preserve
%ghost %attr(755,root,root) %{_localstatedir}/run
%dir %{_localstatedir}/spool
%attr(755,root,root) %{_localstatedir}/spool/lpd
%attr(775,root,mail) %{_localstatedir}/spool/mail
%attr(1777,root,root) %{_localstatedir}/tmp
%{_localstatedir}/yp
}

%define scl_install %{expand:
# scl specific stuff
mkdir -p %{buildroot}%{_root_sysconfdir}/{rpm,scl/prefixes}
cat >> %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config << EOF
%%%%scl %scl
%{?nfsmountable:%%%%nfsmountable %{nfsmountable}}
%{!?nfsmountable:%%%%undefine nfsmountable}
EOF
cat >> %{buildroot}%{_root_sysconfdir}/scl/prefixes/%{scl} << EOF
%_scl_prefix
EOF
# filelist
set +x
cat >> %{buildroot}/lang-exceptions << EOF
af_ZA
am_ET
ast_ES
az_IR
bg_BG
bn_IN
ca@valencia
ca_ES
ca_ES@valencian
cs_CZ
de_AT
de_CH
de_DE
default
el_GR
en_AU
en_CA
en_GB
en_US
en_NZ
es_AR
es_CL
es_CO
es_CR
es_DO
es_EC
es_ES
es_GT
es_HN
es_MX
es_NI
es_PA
es_PE
es_PR
es_SV
es_UY
es_VE
et_EE
eu_ES
fa_IR
fi_FI
fr_BE
fr_CA
fr_CH
fr_FR
gl_ES
he_IL
hr_HR
hu_HU
it_CH
it_IT
ja_JP
ko_KR
ks@devanagari
lv_LV
ms_MY
my_MM
nb_NO
nds_DE
nl_BE
nl_NL
pl_PL
pt_BR
pt_PT
ru_RU
sl_SI
sq_AL
sr_RS
sv_SE
uk_UA
ur_PK
zh_CN
zh_CN.GB2312
zh_HK
zh_TW
zh_TW.Big5
en@boldquot
en@quot
nds@NFE
sr@ije
sr@ijekavian
sr@ijekavianlatin
sr@latin
sr@Latn
uz@cyrillic
uz@Latn
be@latin
en@shaw
brx
brx_IN
EOF
cat >> %{buildroot}/iso_639.sed << EOF
1,/<iso_639_entries/b
# on each new iso-code process the current one
\\!\\(<iso_639_entry\\|</iso_639_entries>\\)!{
    x
    s/^$//
    # we are on the first iso-code--nothing to process here
    t
    # process and write to output
    s/\\s\\+/ /g
    s/<iso_639_entry//
    s!/\\s*>!!
    # use '%' as a separator of parsed and unparsed input
    s/\\(.*\\)iso_639_2T_code="\\([^"]\\+\\)"\\(.*\\)/\\2 % \\1 \\3/
    s/\\([^%]\\+\\)%\\(.*\\)iso_639_2B_code="\\([^"]\\+\\)"\\(.*\\)/\\1\\t\\3 % \\2 \\4/
    #  clear subst. memory for the next t
    t clear
    :clear
    s/\\([^%]\\+\\)%\\(.*\\)iso_639_1_code="\\([^"]\\+\\)"\\(.*\\)/\\1\\t\\3 % \\2 \\4/
    t name
    # no 639-1 code--write xx
    s/%/\\tXX %/
    :name
    s/\\([^%]\\+\\)%\\(.*\\)name="\\([^"]\\+\\)"\\(.*\\)/\\1\\t\\3/
    s/ \\t/\\t/g
    p
    b
    :noout
}
H
EOF
cat >> %{buildroot}/iso_3166.sed << EOF
1,/<iso_3166_entries/b
# on each new iso-code process the current one
\\!\\(<iso_3166_entry\\|</iso_3166_entries>\\)!{
    x
    s/^$//
    # we are on the first iso-code--nothing to process here
    t
    # process and write to output
    s/\\s\\+/ /g
    s/<iso_3166_entry//
    s!/\\s*>!!
    # use '%' as a separator of parsed and unparsed input
    s/\\(.*\\)alpha_2_code="\\([^"]\\+\\)"\\(.*\\)/\\2 % \\1 \\3/
    s/\\([^%]\\+\\)%\\(.*\\)alpha_3_code="\\([^"]\\+\\)"\\(.*\\)/\\1% \\2 \\4/
    #  clear subst. memory for the next t
    t clear
    :clear
    s/\\([^%]\\+\\)%\\(.*\\)numeric_code="\\([^"]\\+\\)"\\(.*\\)/\\1% \\2 \\4/
    t name
    # no 3166 code--write xx
    s/%/\\tXX %/
    :name
    s/\\([^%]\\+\\)%\\(.*\\)name="\\([^"]\\+\\)"\\(.*\\)/\\1\\t\\3/
    s/ \\t/\\t/g
    p
    b
    :noout
}
H
EOF
mkdir -p %{buildroot}%{_localstatedir}
pushd  %{buildroot}%{_localstatedir}
mkdir -p {adm,empty,gopher,lib/{games,misc,rpm-state},local,lock/subsys,log,nis,preserve,run,spool/{mail,lpd},tmp,db,cache,opt,games,yp}
popd
mkdir -p %{buildroot}%{_sysconfdir}
pushd %{buildroot}%{_sysconfdir}
mkdir -p {X11/{applnk,fontpath.d},xdg/autostart,opt,pm/{config.d,power.d,sleep.d},xinetd.d,skel,sysconfig,pki}
popd
mkdir -p %{buildroot}%{_scl_root}
rm -f $RPM_BUILD_DIR/%{buildsubdir}/filelist
rm -f $RPM_BUILD_DIR/%{buildsubdir}/filesystem
pushd %{buildroot}%{_scl_root}
mkdir -p boot dev \\
        home media mnt opt proc root run/lock srv sys tmp \\
        usr/{bin,etc,games,include,lib/{games,locale,modules,sse2},libexec,local/{bin,etc,games,lib,sbin,src,share/{applications,man/man{1,2,3,4,5,6,7,8,9,n,1x,2x,3x,4x,5x,6x,7x,8x,9x},info},libexec,include,},sbin,share/{aclocal,applications,augeas/lenses,backgrounds,desktop-directories,dict,doc,empty,games,ghostscript/conf.d,gnome,icons,idl,info,man/man{1,2,3,4,5,6,7,8,9,n,1x,2x,3x,4x,5x,6x,7x,8x,9x,0p,1p,3p},mime-info,misc,omf,pixmaps,sounds,themes,xsessions,X11},src,src/kernels,src/debug}
%ifarch x86_64 ppc ppc64 ppc64le aarch64 sparc sparc64 s390 s390x
mkdir -p usr/{%{_lib}/{games,sse2,tls,X11,pm-utils/{module.d,power.d,sleep.d}},local/%{_lib}}
%endif
ln -snf %{_localstatedir}/tmp usr/tmp
ln -snf spool/mail %{buildroot}%{_localstatedir}/mail
ln -snf usr/bin bin
ln -snf usr/sbin sbin
ln -snf usr/lib lib
%ifarch x86_64 ppc ppc64 ppc64le aarch64 sparc sparc64 s390 s390x
ln -snf usr/%{_lib} %{_lib}
%endif
sed -n -f %{buildroot}/iso_639.sed /usr/share/xml/iso-codes/iso_639.xml >%{buildroot}/iso_639.tab
sed -n -f %{buildroot}/iso_3166.sed /usr/share/xml/iso-codes/iso_3166.xml >%{buildroot}/iso_3166.tab
grep -v "^$" %{buildroot}/iso_639.tab | grep -v "^#" | while read a b c d ; do
    [[ "$d" =~ "^Reserved" ]] && continue
    [[ "$d" =~ "^No linguistic" ]] && continue
    locale=$c
    if [ "$locale" = "XX" ]; then
        locale=$b
    fi
    echo "%lang(${locale})      %{_scl_root}/usr/share/locale/${locale}" >> $RPM_BUILD_DIR/%{buildsubdir}/filelist
    echo "%lang(${locale}) %ghost %config(missingok) %{_scl_root}/usr/share/man/${locale}" >> $RPM_BUILD_DIR/%{buildsubdir}/filelist
done
cat %{buildroot}/lang-exceptions | grep -v "^#" | grep -v "^$" | while read loc ; do
    locale=$loc
    locality=
    special=
    [[ "$locale" =~ "@" ]] && locale=${locale%%%%@*}
    [[ "$locale" =~ "_" ]] && locality=${locale##*_}
    [[ "$locality" =~ "." ]] && locality=${locality%%%%.*}
    [[ "$loc" =~ "_" ]] || [[ "$loc" =~ "@" ]] || special=$loc
    # If the locality is not official, skip it
    if [ -n "$locality" ]; then
        grep -q "^$locality" %{buildroot}/iso_3166.tab || continue
    fi
    # If the locale is not official and not special, skip it
    if [ -z "$special" ]; then
        egrep -q "[[:space:]]${locale%%_*}[[:space:]]" \\
           %{buildroot}/iso_639.tab || continue
    fi
    echo "%lang(${locale})      %{_scl_root}/usr/share/locale/${loc}" >> $RPM_BUILD_DIR/%{buildsubdir}/filelist
    echo "%lang(${locale})  %ghost %config(missingok) %{_scl_root}/usr/share/man/${loc}" >> $RPM_BUILD_DIR/%{buildsubdir}/filelist
done
rm -f %{buildroot}/iso_639.tab
rm -f %{buildroot}/iso_639.sed
rm -f %{buildroot}/iso_3166.tab
rm -f %{buildroot}/iso_3166.sed
rm -f %{buildroot}/lang-exceptions
cat $RPM_BUILD_DIR/%{buildsubdir}/filelist | grep "locale" | while read a b ; do
    mkdir -p -m 755 %{buildroot}/$b/LC_MESSAGES
done
cat $RPM_BUILD_DIR/%{buildsubdir}/filelist | grep "/share/man" | while read a b c d; do
    mkdir -p -m 755 %{buildroot}/$d/man{1,2,3,4,5,6,7,8,9,n,1x,2x,3x,4x,5x,6x,7x,8x,9x,0p,1p,3p}
done
for i in man{1,2,3,4,5,6,7,8,9,n,1x,2x,3x,4x,5x,6x,7x,8x,9x,0p,1p,3p}; do
   echo "%{_scl_root}/usr/share/man/$i" >> $RPM_BUILD_DIR/%{buildsubdir}/filelist
done
ln -s $RPM_BUILD_DIR/%{buildsubdir}/filelist $RPM_BUILD_DIR/%{buildsubdir}/filesystem
set -x
popd
}
#--- end macros.scl.inc

%scl_package %scl

Summary: Package that installs %scl
Name: %scl_name
Version: 11.0
Release: %{?xsrel}%{?dist}
License: GPLv2+
Group: Applications/File
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: README
Source1: sudo.sh

# The base package requires just the toolchain and the perftools.
%if 0
Requires: %{scl_prefix}toolchain %{scl_prefix}perftools
%endif
Obsoletes: %{name} < %{version}-%{release}
Obsoletes: %{scl_prefix}dockerfiles < %{version}-%{release}

BuildRequires: scl-utils-build >= 20120927-11
BuildRequires: iso-codes
BuildRequires: help2man
%if 0%{?rhel} >= 8
BuildRequires: python3-devel
%endif

%description
This is the main package for %scl Software Collection.

%package runtime
Summary: Package that handles %scl Software Collection.
Group: Applications/File
Requires: scl-utils >= 20120927-11
Obsoletes: %{name}-runtime < %{version}-%{release}
%if 0%{?rhel} >= 7
Requires(post): %{_root_sbindir}/semanage %{_root_sbindir}/restorecon
Requires(postun): %{_root_sbindir}/semanage %{_root_sbindir}/restorecon
%else
Requires(post): libselinux policycoreutils-python
Requires(postun): libselinux policycoreutils-python
%endif

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary: Package shipping basic build configuration
Group: Applications/File
Requires: %{scl_prefix}runtime
Requires: scl-utils-build >= 20120927-11
Obsoletes: %{name}-build < %{version}-%{release}

%description build
Package shipping essential configuration macros to build %scl Software Collection.

%if 0
%package toolchain
Summary: Package shipping basic toolchain applications
Group: Applications/File
Requires: %{scl_prefix}runtime
Requires: %{scl_prefix}gcc %{scl_prefix}gcc-c++ %{scl_prefix}gcc-gfortran
Requires: %{scl_prefix}binutils %{scl_prefix}gdb %{scl_prefix}strace
Requires: %{scl_prefix}dwz %{scl_prefix}elfutils
Requires: %{scl_prefix}ltrace %{scl_prefix}make
Requires: %{scl_prefix}annobin
%if 0%{?rhel} <= 7
Requires: %{scl_prefix}memstomp
%endif
Obsoletes: %{name}-toolchain < %{version}-%{release}

%description toolchain
Package shipping basic toolchain applications (compiler, debugger, ...)
%endif

%if 0
%package perftools
Summary: Package shipping performance tools
Group: Applications/File
Requires: %{scl_prefix}runtime
Requires: %{scl_prefix}systemtap %{scl_prefix}valgrind
%if 0%{?rhel} <= 7
Requires: %{scl_prefix}oprofile
%ifarch x86_64
Requires: %{scl_prefix}dyninst
%endif
%else
%ifarch x86_64 ppc64le aarch64
Requires: %{scl_prefix}dyninst
%endif
%endif
Obsoletes: %{name}-perftools < %{version}-%{release}

%description perftools
%if 0%{?rhel} <= 7
Package shipping performance tools (systemtap, oprofile)
%else
Package shipping performance tools (systemtap)
%endif
%endif

%prep
%setup -c -T

# Manually copied the README from upstream with macros already expanded
# The macro trickery upstream used doesn't work in our version of Koji
cp %{SOURCE0} README

%build

# Temporary helper script used by help2man.
cat <<\EOF | tee h2m_helper
#!/bin/sh
if [ "$1" = "--version" ]; then
  printf '%%s' "%{?scl_name} %{version} Software Collection"
else
  cat README
fi
EOF
chmod a+x h2m_helper
# Generate the man page.
help2man -N --section 7 ./h2m_helper -o %{?scl_name}.7

# Enable collection script
# ========================
cat <<EOF >enable
# General environment variables
export PATH=%{_bindir}\${PATH:+:\${PATH}}
export MANPATH=%{_mandir}:\${MANPATH}
export INFOPATH=%{_infodir}\${INFOPATH:+:\${INFOPATH}}
export PCP_DIR=%{_scl_root}
# bz847911 workaround:
# we need to evaluate rpm's installed run-time % { _libdir }, not rpmbuild time
# or else /etc/ld.so.conf.d files?
rpmlibdir=\$(rpm --eval "%%{_libdir}")
# bz1017604: On 64-bit hosts, we should include also the 32-bit library path.
# bz1873882: On 32-bit hosts, we should include also the 64-bit library path.
if [ "\$rpmlibdir" != "\${rpmlibdir/lib64/}" ]; then
  rpmlibdir32=":%{_scl_root}\${rpmlibdir/lib64/lib}"
  dynpath32="\$rpmlibdir32/dyninst"
else
  rpmlibdir64=":%{_scl_root}\${rpmlibdir/lib/lib64}"
  dynpath64="\$rpmlibdir64/dyninst"
fi
# Add SCL dyninst to LD_LIBRARY_PATH, both 64- and 32-bit paths.
export LD_LIBRARY_PATH=%{_scl_root}\$rpmlibdir/dyninst\$dynpath64\$dynpath32\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}
# Now prepend the usual /opt/.../usr/lib{64,}.
export LD_LIBRARY_PATH=%{_scl_root}\$rpmlibdir\$rpmlibdir64\$rpmlibdir32\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}
export PKG_CONFIG_PATH=%{_libdir}/pkgconfig\${PKG_CONFIG_PATH:+:\${PKG_CONFIG_PATH}}
EOF

# Sudo script
# ===========
cp %{SOURCE1} sudo

%install
(%{scl_install})

# This allows users to build packages using DTS/GTS.
cat >> %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config << EOF
%%enable_devtoolset11 %%global ___build_pre %%{___build_pre}; source scl_source enable %{scl} || :
EOF

mkdir -p %{buildroot}%{_scl_root}/etc/alternatives %{buildroot}%{_scl_root}/var/lib/alternatives

install -d -m 755 %{buildroot}%{_scl_scripts}
install -p -m 755 enable %{buildroot}%{_scl_scripts}/

install -d -m 755 %{buildroot}%{_scl_scripts}
install -p -m 755 sudo %{buildroot}%{_bindir}/

# Other directories that should be owned by the runtime
install -d -m 755 %{buildroot}%{_datadir}/appdata
# Otherwise unowned perl directories
install -d -m 755 %{buildroot}%{_libdir}/perl5
install -d -m 755 %{buildroot}%{_libdir}/perl5/vendor_perl
install -d -m 755 %{buildroot}%{_libdir}/perl5/vendor_perl/auto

# Install generated man page.
install -d -m 755 %{buildroot}%{_mandir}/man7
install -p -m 644 %{?scl_name}.7 %{buildroot}%{_mandir}/man7/

%files
%doc README
%{_mandir}/man7/%{?scl_name}.*

%files runtime
%scl_files
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_sysconfdir}/selinux-equiv.created
%dir %{_scl_root}/etc/alternatives
%dir %{_datadir}/appdata

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}*

%if 0
%files toolchain
%endif

%if 0
%files perftools
%endif

%post runtime
if [ ! -f %{_sysconfdir}/selinux-equiv.created ]; then
  /usr/sbin/semanage fcontext -a -e / %{_scl_root}
  restorecon -R %{_scl_root}
  touch %{_sysconfdir}/selinux-equiv.created
fi

%preun runtime
[ $1 = 0 ] && rm -f %{_sysconfdir}/selinux-equiv.created || :

%postun runtime
if [ $1 = 0 ]; then
  /usr/sbin/semanage fcontext -d %{_scl_root}
  [ -d %{_scl_root} ] && restorecon -R %{_scl_root} || :
fi

%changelog
* Wed Jul 28 2021 Marek Polacek <polacek@redhat.com> - 11.0-3
- require annobin

* Tue Jul 27 2021 Marek Polacek <polacek@redhat.com> - 11.0-2
- fix LD_LIBRARY_PATH wrt dyninst, avoid duplicate paths (#1873882)

* Wed Jun  2 2021 Marek Polacek <polacek@redhat.com> - 11.0-1
- on 32-bit hosts, include also the 64-bit library path (#1873882)

* Wed May 19 2021 Marek Polacek <polacek@redhat.com> - 11.0-0
- new package (#1946794)
