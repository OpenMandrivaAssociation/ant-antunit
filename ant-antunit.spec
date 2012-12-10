%global base_name       antunit

Name:             ant-%{base_name}
Version:          1.1
Release:          7
Summary:          Provide antunit ant task
Group:            Development/Java
License:          ASL 2.0
URL:              http://ant.apache.org/antlibs/%{base_name}/
Source0:          http://www.apache.org/dist/ant/antlibs/%{base_name}/source/apache-%{name}-%{version}-src.tar.bz2
BuildArch:        noarch
ExcludeArch:      ppc64

BuildRequires:    java-devel >= 0:1.6.0
BuildRequires:    jpackage-utils
BuildRequires:    ant

Requires:         java >= 0:1.6.0
Requires:         jpackage-utils
Requires:         ant

Requires(post):   jpackage-utils
Requires(postun): jpackage-utils


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
Group:            Development/Java
Requires:         jpackage-utils

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
rm -rf %{buildroot}
# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -pm 644 build/lib/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 %{name}-%{version}.pom %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap org.apache.ant %{name} %{version} JPP %{name}

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr docs/* %{buildroot}%{_javadocdir}/%{name}/

# OPT_JAR_LIST fragments
mkdir -p %{buildroot}%{_sysconfdir}/%{name}.d
echo "ant/ant-antunit" > %{buildroot}%{_sysconfdir}/%{name}.d/antunit


%post
%update_maven_depmap

%postun
%update_maven_depmap


%files
%defattr(-,root,root,-)
%doc CONTRIBUTORS NOTICE README README.html WHATSNEW common/LICENSE
%config(noreplace) %{_sysconfdir}/%{name}.d/antunit
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%doc common/LICENSE
%{_javadocdir}/%{name}




%changelog
* Sun Nov 27 2011 Guilherme Moro <guilherme@mandriva.com> 1.1-7
+ Revision: 733788
- rebuild
- imported package ant-antunit

