%define oname ParseTree

Name:       rubygem-%{oname}
Version:    3.0.6
Release:    %mkrel 1
Summary:    A C extension that extracts the parse tree for an entire class
Group:      Development/Ruby
License:    MIT
URL:        http://rubyforge.org/projects/parsetree/
Source0:    http://rubygems.org/gems/%{oname}-%{version}.gem
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}
Requires:   rubygems
Requires:   rubygem(RubyInline) >= 3.7.0
Requires:   rubygem(sexp_processor) >= 3.0.0
Requires:   rubygem(rubyforge) >= 2.0.4
Requires:   rubygem(minitest) >= 1.6.0
Requires:   rubygem(hoe) >= 2.6.0
BuildRequires: rubygems
BuildArch:  noarch
Provides:   rubygem(%{oname}) = %{version}

%description
ParseTree is a C extension (using RubyInline) that extracts the parse
tree for an entire class or a specific method and returns it as a
s-expression (aka sexp) using ruby's arrays, strings, symbols, and
integers.
As an example:
def conditional1(arg1)
if arg1 == 0 then
return 1
end
return 0
end
becomes:
[:defn,
:conditional1,
[:scope,
[:block,
[:args, :arg1],
[:if,
[:call, [:lvar, :arg1], :==, [:array, [:lit, 0]]],
[:return, [:lit, 1]],
nil],
[:return, [:lit, 0]]]]]


%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{ruby_gemdir}
gem install --local --install-dir %{buildroot}%{ruby_gemdir} \
            --force --rdoc %{SOURCE0}

mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{ruby_gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{ruby_gemdir}/bin
find %{buildroot}%{ruby_gemdir}/gems/%{oname}-%{version}/bin -type f | xargs chmod 755
find %{buildroot}%{ruby_gemdir}/gems/%{oname}-%{version}/lib -type f | xargs chmod 644
find %{buildroot}%{ruby_gemdir}/gems/%{oname}-%{version}/test -type f | xargs chmod 755
find %{buildroot}%{ruby_gemdir}/gems/%{oname}-%{version}/demo -type f | xargs chmod 755
chmod 755 %{buildroot}%{ruby_gemdir}/gems/%{oname}-%{version}/validate.sh

#fix shebang once again...
ruby -pi -e 'sub(/\/usr\/local\/bin\/ruby/, "/usr/bin/env ruby")' %{buildroot}%{ruby_gemdir}/gems/%{oname}-%{version}/{bin/*,lib/parse_tree.rb,test/*.rb,demo/*}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{_bindir}/parse_tree_abc
%{_bindir}/parse_tree_audit
%{_bindir}/parse_tree_deps
%{_bindir}/parse_tree_show
%dir %{ruby_gemdir}/gems/%{oname}-%{version}/
%{ruby_gemdir}/gems/%{oname}-%{version}/.autotest
%{ruby_gemdir}/gems/%{oname}-%{version}/bin/
%{ruby_gemdir}/gems/%{oname}-%{version}/demo/
%{ruby_gemdir}/gems/%{oname}-%{version}/lib/
%{ruby_gemdir}/gems/%{oname}-%{version}/test/
%{ruby_gemdir}/gems/%{oname}-%{version}/.require_paths
%{ruby_gemdir}/gems/%{oname}-%{version}/validate.sh
%doc %{ruby_gemdir}/doc/%{oname}-%{version}
%doc %{ruby_gemdir}/gems/%{oname}-%{version}/History.txt
%doc %{ruby_gemdir}/gems/%{oname}-%{version}/Manifest.txt
%doc %{ruby_gemdir}/gems/%{oname}-%{version}/Rakefile
%doc %{ruby_gemdir}/gems/%{oname}-%{version}/README.txt
%{ruby_gemdir}/cache/%{oname}-%{version}.gem
%{ruby_gemdir}/specifications/%{oname}-%{version}.gemspec
