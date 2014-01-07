%{?_javapackages_macros:%_javapackages_macros}
%global base_name       antunit

Name:             ant-%{base_name}
Version:          1.2
Release:          12.0%{?dist}
Summary:          Provide antunit ant task

License:          ASL 2.0
URL:              http://ant.apache.org/antlibs/%{base_name}/
Source0:          http://www.apache.org/dist/ant/antlibs/%{base_name}/source/apache-%{name}-%{version}-src.tar.bz2
BuildArch:        noarch

BuildRequires:    java-devel >= 1:1.6.0
BuildRequires:    jpackage-utils
BuildRequires:    ant-junit
BuildRequires:    ant-testutil

Requires:         java >= 1:1.6.0
Requires:         jpackage-utils
Requires:         ant


%description
The <antunit> task drives the tests much like <junit> does for JUnit tests.

When called on a build file, the task will start a new Ant project for that
build file and scan for targets with names that start with "test". For each
such target it then will:

   1. Execute the target named setUp, if there is one.
   2. Execute the target itself - if this target depends on other targets the
      normal Ant rules apply and the dependent targets are executed first.
   3. Execute the target names tearDown, if there is one.


%package javadoc
Summary:          Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q -n apache-%{name}-%{version}
mv CONTRIBUTORS CONTRIBUTORS.orig
iconv -f ISO-8859-1 -t UTF-8 CONTRIBUTORS.orig > CONTRIBUTORS
touch -r CONTRIBUTORS.orig CONTRIBUTORS


%build
ant package


%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}/ant
install -pm 644 build/lib/%{name}-%{version}.jar %{buildroot}%{_javadir}/ant/%{name}.jar
install -d -m 0755 %{buildroot}%{_datadir}/ant/lib
ln -s ../../java/ant/%{name}.jar %{buildroot}%{_datadir}/ant/lib

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 %{name}-%{version}.pom %{buildroot}%{_mavenpomdir}/JPP.ant-%{name}.pom
%add_maven_depmap JPP.ant-%{name}.pom ant/%{name}.jar

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr docs/* %{buildroot}%{_javadocdir}/%{name}/

# OPT_JAR_LIST fragments
mkdir -p %{buildroot}%{_sysconfdir}/ant.d
echo "%{base_name} ant/%{name}" > %{buildroot}%{_sysconfdir}/ant.d/%{base_name}


%files -f .mfiles
%doc CONTRIBUTORS LICENSE NOTICE README README.html WHATSNEW
%config(noreplace) %{_sysconfdir}/ant.d/%{base_name}
%{_datadir}/ant/lib/%{name}.jar

%files javadoc
%doc LICENSE
%{_javadocdir}/%{name}


%changelog
* Thu Aug 15 2013 Orion Poplawski <orion@cora.nwra.com> 1.2-12
- Another attempt at fixing the install

* Thu Aug 15 2013 Orion Poplawski <orion@cora.nwra.com> 1.2-11
- Fix install locations (bug 988561)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-9
- Update to current packaging guidelines

* Wed Jun 12 2013 Orion Poplawski <orion@cora.nwra.com> 1.2-7
- Update spec for new Java guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-5
- Remove ppc64 ExcludeArch

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 6 2012 Orion Poplawski <orion@cora.nwra.com> 1.2-3
- Drop junit4 references

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jan 4 2012 Orion Poplawski <orion@cora.nwra.com> 1.2-1
- Update to 1.2

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Orion Poplawski <orion@cora.nwra.com> 1.1-4
- ExcludeArch ppc64 - no java >= 1:1.6.0 on ppc64

* Mon Dec 6 2010 Orion Poplawski <orion@cora.nwra.com> 1.1-3
- Rename to ant-antunit
- Drop BuildRoot and %%clean
- Drop unneeded Provides

* Fri Oct 29 2010 Orion Poplawski <orion@cora.nwra.com> 1.1-2
- Add /etc/ant.d/antunit
- Add Requires: ant

* Thu Oct 28 2010 Orion Poplawski <orion@cora.nwra.com> 1.1-1
- Initial package
