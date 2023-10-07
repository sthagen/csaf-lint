# Third Party Dependencies

<!--[[[fill sbom_sha256()]]]-->
The [SBOM in CycloneDX v1.4 JSON format](https://git.sr.ht/~sthagen/csaf-lint/blob/default/etc/sbom/cdx.json) with SHA256 checksum ([eacd7735 ...](https://git.sr.ht/~sthagen/csaf-lint/blob/default/etc/sbom/cdx.json.sha256 "sha256:eacd773599b5cb33930f8e2ca853b3a5e044cbe88ec813dd2e0f953e977519f6")).
<!--[[[end]]] (checksum: 97edb714ded9691cee689292fe44e39a)-->
## Licenses

JSON files with complete license info of: [direct dependencies](direct-dependency-licenses.json) | [all dependencies](all-dependency-licenses.json)

### Direct Dependencies

<!--[[[fill direct_dependencies_table()]]]-->
| Name                                                            | Version                                                | License     | Author                     | Description (from packaging data)                                                                |
|:----------------------------------------------------------------|:-------------------------------------------------------|:------------|:---------------------------|:-------------------------------------------------------------------------------------------------|
| [attrs](https://www.attrs.org/en/stable/changelog.html)         | [23.1.0](https://pypi.org/project/attrs/23.1.0/)       | MIT License | Hynek Schlawack <hs@ox.cx> | Classes Without Boilerplate                                                                      |
| [jsonschema](https://github.com/python-jsonschema/jsonschema)   | [4.19.1](https://pypi.org/project/jsonschema/4.19.1/)  | MIT License | Julian Berman              | An implementation of JSON Schema validation for Python                                           |
| [lxml](https://lxml.de/)                                        | [4.9.3](https://pypi.org/project/lxml/4.9.3/)          | BSD License | lxml dev team              | Powerful and Pythonic XML processing library combining libxml2/libxslt with the ElementTree API. |
| [referencing](https://github.com/python-jsonschema/referencing) | [0.30.2](https://pypi.org/project/referencing/0.30.2/) | MIT License | Julian Berman              | JSON Referencing + Python                                                                        |
| [xmlschema](https://github.com/sissaschool/xmlschema)           | [2.5.0](https://pypi.org/project/xmlschema/2.5.0/)     | MIT License | Davide Brunato             | An XML Schema validator and decoder                                                              |
<!--[[[end]]] (checksum: a9687a06ba05a791c944a93bf780fce7)-->

### Indirect Dependencies

<!--[[[fill indirect_dependencies_table()]]]-->
| Name                                                                                        | Version                                                                  | License     | Author         | Description (from packaging data)                                    |
|:--------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------|:------------|:---------------|:---------------------------------------------------------------------|
| [elementpath](https://github.com/sissaschool/elementpath)                                   | [4.1.5](https://pypi.org/project/elementpath/4.1.5/)                     | MIT License | Davide Brunato | XPath 1.0/2.0/3.0/3.1 parsers and selectors for ElementTree and lxml |
| [jsonschema-specifications](https://github.com/python-jsonschema/jsonschema-specifications) | [2023.6.1](https://pypi.org/project/jsonschema-specifications/2023.6.1/) | MIT License | Julian Berman  | The JSON Schema meta-schemas and vocabularies, exposed as a Registry |
| [rpds-py](https://github.com/crate-py/rpds)                                                 | [0.8.11](https://pypi.org/project/rpds-py/0.8.11/)                       | MIT License | Julian Berman  | Python bindings to Rust's persistent data structures (rpds)          |
<!--[[[end]]] (checksum: bc362607d49d8beab9c1afb80d75ab6f)-->

## Dependency Tree(s)

JSON file with the complete package dependency tree info of: [the full dependency tree](package-dependency-tree.json)

### Rendered SVG

Base graphviz file in dot format: [Trees of the direct dependencies](package-dependency-tree.dot.txt)

<img src="./package-dependency-tree.svg" alt="Trees of the direct dependencies" title="Trees of the direct dependencies"/>

### Console Representation

<!--[[[fill dependency_tree_console_text()]]]-->
````console
jsonschema==4.19.1
├── attrs [required: >=22.2.0, installed: 23.1.0]
├── jsonschema-specifications [required: >=2023.03.6, installed: 2023.6.1]
│   └── referencing [required: >=0.28.0, installed: 0.30.2]
│       ├── attrs [required: >=22.2.0, installed: 23.1.0]
│       └── rpds-py [required: >=0.7.0, installed: 0.8.11]
├── referencing [required: >=0.28.4, installed: 0.30.2]
│   ├── attrs [required: >=22.2.0, installed: 23.1.0]
│   └── rpds-py [required: >=0.7.0, installed: 0.8.11]
└── rpds-py [required: >=0.7.1, installed: 0.8.11]
lxml==4.9.3
xmlschema==2.5.0
└── elementpath [required: >=4.1.5,<5.0.0, installed: 4.1.5]
````
<!--[[[end]]] (checksum: 53f9eb01fa26d5f0c0dc574ae08e0d05)-->
