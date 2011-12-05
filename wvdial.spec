Summary: A heuristic autodialer for PPP connections
Name: wvdial
Version: 1.60
Release: 12%{?dist}
License: LGPLv2+
URL: http://alumnit.ca/wiki/?WvDial
Group: System Environment/Daemons
#Newlocation for 1.61+ is http://wvstreams.googlecode.com/files/wvdial-%{version}.tar.gz
Source0: http://alumnit.ca/download/wvdial-%{version}.tar.gz

#allow specifying the remotename at startup-time
Patch1: wvdial-1.60-remotename.patch
# added option for dial timeout(#200375) - in upstream now
Patch2: wvdial-1.60-dialtimeout.patch
#added support for up to 9 alternative numbers instead of 4(#178025)
Patch3: wvdial-1.54-9nums.patch
#change Compuserve "Classic" login prompt to the "new" style (#146664)
Patch4: wvdial-1.60-compuserve.patch
#fixed wvdial.conf (5) manpage (#440161)
Patch5: wvdial-manpages.patch
#make wvdial compilable in rawhide (scandir api change),
#reduce compiler warnings
Patch6: wvdial-1.60-dirent.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libwvstreams-devel lockdev-devel openssl-devel
BuildRequires: pkgconfig
Requires: ppp

%description
WvDial automatically locates and configures modems and can log into
almost any ISP's server without special configuration. You need to
input the username, password, and phone number, and then WvDial will
negotiate the PPP connection using any mechanism needed.

%prep
%setup -q
%patch1 -p1 -b .remotename
%patch2 -p1 -b .dialtimeout
%patch3 -p1 -b .9nums
%patch4 -p1 -b .compuserve
%patch5 -p1 -b .manpages
%patch6 -p1 -b .dirent

%build
make \
	CPPOPTS="$RPM_OPT_FLAGS -DUSE_LOCKDEV=1" \
	LOCKDEV=-llockdev \
	XX_LIBS="-lcrypt -llockdev" \
	PREFIX=%{_prefix} \
	BINDIR=%{_bindir} \
	MANDIR=%{_mandir} \
	PPPDIR=%{_sysconfdir}/ppp/peers $@

%install
rm -rf $RPM_BUILD_ROOT
make install \
	PREFIX=${RPM_BUILD_ROOT}%{_prefix} \
	BINDIR=${RPM_BUILD_ROOT}%{_bindir} \
	MANDIR=${RPM_BUILD_ROOT}%{_mandir} \
	PPPDIR=${RPM_BUILD_ROOT}%{_sysconfdir}/ppp/peers
rm $RPM_BUILD_ROOT/%{_sysconfdir}/ppp/peers/wvdial-pipe
touch $RPM_BUILD_ROOT/%{_sysconfdir}/wvdial.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc CHANGES* COPYING* README* TODO FAQ
%{_bindir}/wvdialconf
%{_bindir}/wvdial
%{_mandir}/man1/wvdialconf.*
%{_mandir}/man1/wvdial.*
%{_mandir}/man5/wvdial.conf*
%attr(0600,root,daemon)	%config(noreplace) %{_sysconfdir}/ppp/peers/wvdial
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/wvdial.conf

%changelog
* Fri Dec 18 2009 Ondrej Vasik <ovasik@redhat.com> - 1.60-12
- really fix source0 link

* Thu Dec 10 2009 Ondrej Vasik <ovasik@redhat.com> - 1.60-11
- Merge review cleanup (#226546), comment patches, license
  to LGPLv2+, specify names in files section, fix source0 link...

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.60-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 11 2009 Ondrej Vasik <ovasik@redhat.com> - 1.60-9
- make wvdial compilable in rawhide (scandir api change),
  reduce compiler warnings

* Wed Feb 25 2009 Ondrej Vasik <ovasik@redhat.com> - 1.60-8
- mark /etc/ppp/peers/wvdial as noreplace

* Tue Nov 25 2008 Ondrej Vasik <ovasik@redhat.com> - 1.60-7
- new libwvstreams rebuild, removed -fno-rtti CPP_FLAG to
  compile correctly with new libwvstreams

* Fri Aug 29 2008 Ondrej Vasik <ovasik@redhat.com> - 1.60-6
- patch fuzz clean up

* Wed Apr 02 2008 Ondrej Vasik <ovasik@redhat.com> - 1.60-5
- fixed wvdial.conf (5) manpage (#440161)
- change Compuserve "Classic" login prompt to the "new"
  style (#146664)

* Tue Feb 12 2008 Ondrej Vasik <ovasik@redhat.com> - 1.60-4
- added support for up to 9 alternative numbers instead of 4
  (#178025, patch by V.Mencl)
- gcc43 rebuild

* Mon Oct 29 2007 Bill Nottingham <notting@redhat.com> - 1.60-3
- fix remotename patch (#348831, #344391)

* Wed Oct 10 2007 Ondrej Vasik <ovasik@redhat.com> - 1.60-2
- added option for dial timeout(#200375)

* Fri Aug 17 2007 Harald Hoyer <harald@rawhide.home> - 1.60-1
- version 1.60
- changed license tag to LGPLv2

* Thu Jun 28 2007 Harald Hoyer <harald@redhat.com> - 1.56-1
- version 1.56

* Wed Apr 18 2007 Harald Hoyer <harald@redhat.com> - 1.54.0-6
- specfile review

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.54.0-5.2.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.54.0-5.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.54.0-5.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Dec 19 2005 Harald Hoyer <harald@redhat.com>
- rebuilt

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Mar 03 2005 Harald Hoyer <harald@redhat.com> 
- rebuilt

* Wed Feb 09 2005 Harald Hoyer <harald@redhat.com>
- rebuilt

* Tue Sep 21 2004 Harald Hoyer <harald@redhat.com> 1.54.0-3
- added openssl-devel build req (bug 132887)

* Mon Aug 31 2004 Harald Hoyer <harald@redhat.com> 1.54.0-2
- added empty wvdial.conf file (bug 130622)

* Mon Jun 21 2004 Harald Hoyer <harald@redhat.com> 1.54.0-1
- version 1.54.0

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 01 2004 Karsten Hopp <karsten@redhat.de> 1.53-14 
- remove -O0

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Sep  8 2003 Nalin Dahyabhai <nalin@redhat.com> 1.53-12
- rebuild

* Mon Sep  8 2003 Nalin Dahyabhai <nalin@redhat.com> 1.53-11
- rebuild

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Nov 14 2002 Nalin Dahyabhai <nalin@redhat.com> 1.53-8
- remove unpackaged files after %%install

* Mon Aug 12 2002 Nalin Dahyabhai <nalin@redhat.com> 1.53-7
- add missing URL
- document --remotename in the man page

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com> 1.53-6
- rebuilt with gcc-3.2 (we hope)

* Fri Aug  9 2002 Nalin Dahyabhai <nalin@redhat.com> 1.53-5
- re-allow specifying the remotename at startup-time
- add man page for the configuration file

* Tue Jul 23 2002 Tim Powers <timp@redhat.com> 1.53-4
- build using gcc-3.2-0.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 1.53-3
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com> 1.53-2
- automated rebuild

* Wed Apr 10 2002 Nalin Dahyabhai <nalin@redhat.com> 1.53-1
- update to 1.53

* Thu Apr  4 2002 Nalin Dahyabhai <nalin@redhat.com> 1.52-1
- update to 1.52

* Wed Mar 27 2002 Nalin Dahyabhai <nalin@redhat.com> 1.51-1
- update to 1.51

* Fri Feb 22 2002 Nalin Dahyabhai <nalin@redhat.com> 1.50-1
- update to 1.50
- use lockdev for locking

* Thu Jan 24 2002 Than Ngo <than@redhat.com> 1.41-18
- fix to build against g++ 3

* Wed Sep 12 2001 Tim Powers <timp@redhat.com>
- rebuild with new gcc and binutils

* Mon Jul 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- bump the release and rebuild

* Wed Jul 11 2001 Nalin Dahyabhai <nalin@redhat.com>
- bump the release and rebuild

* Tue Jul  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- change Copyright: tag to License:

* Mon Apr  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- include the actual TODO file in docs, not a dangling symlink to it (#34385)

* Mon Feb 12 2001 Nalin Dahyabhai <nalin@redhat.com>
- Merge in latest -libs patch from rp3.

* Mon Aug 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- Merge in latest -libs patch from rp3.

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul  2 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new C++

* Sat Jun 17 2000 Bill Nottingham <notting@redhat.com>
- add %%defattr

* Fri Jun 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- Merge in latest -libs patch from rp3.

* Sun Jun  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- FHS fixes.

* Fri May  5 2000 Bill Nottingham <notting@redhat.com>
- fix build with more strict c++ compiler

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Fri Jan 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- sync up to copy in rp3's CVS repository for consistency, except for
  changes to Makefiles

* Thu Jan 13 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.41, backing out patches that are now in mainline source

* Sat Sep 18 1999 Michael K. Johnson <johnsonm@redhat.com>
- improved the speed up dialing patch
- improved the inheritance patch

* Fri Sep 17 1999 Michael K. Johnson <johnsonm@redhat.com>
- added explicit inheritance to wvdial.conf
- speed up dialing

* Mon Sep 13 1999 Michael K. Johnson <johnsonm@redhat.com>
- improved the chat mode fix to allow specifying the remotename
  so that multiple wvdial instances can't step on each other.

* Fri Sep 10 1999 Michael K. Johnson <johnsonm@redhat.com>
- chat mode fix to make CHAP/PAP work with chat mode

* Mon Aug 02 1999 Michael K. Johnson <johnsonm@redhat.com>
- Packaged 1.40

* Wed Jul 28 1999 Michael K. Johnson <johnsonm@redhat.com>
- Initial Red Hat package
