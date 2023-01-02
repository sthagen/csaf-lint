# Third Party Dependencies

<!--[[[fill sbom_sha256()]]]-->
The [SBOM in CycloneDX v1.4 JSON format](https://git.sr.ht/~sthagen/csaf-lint/blob/default/sbom.json) with SHA256 checksum ([7c82ef9f ...](https://git.sr.ht/~sthagen/csaf-lint/blob/default/sbom.json.sha256 "sha256:7c82ef9f7b1e9202c4ba2a10837d71bc56006f9bf292c982def444dda9faf558")).
<!--[[[end]]] (checksum: 1996d6278bdbc9cb32091779358098b0)-->
## Licenses

JSON files with complete license info of: [direct dependencies](direct-dependency-licenses.json) | [all dependencies](all-dependency-licenses.json)

### Direct Dependencies

<!--[[[fill direct_dependencies_table()]]]-->
| Name                                                                               | Version                                               | License     | Author          | Description (from packaging data)                                                                |
|:-----------------------------------------------------------------------------------|:------------------------------------------------------|:------------|:----------------|:-------------------------------------------------------------------------------------------------|
| [attrs](https://www.attrs.org/)                                                    | [22.2.0](https://pypi.org/project/attrs/22.2.0/)      | MIT License | Hynek Schlawack | Classes Without Boilerplate                                                                      |
| [jsonschema](https://github.com/python-jsonschema/jsonschema/blob/main/README.rst) | [4.17.3](https://pypi.org/project/jsonschema/4.17.3/) | MIT License | Julian Berman   | An implementation of JSON Schema validation for Python                                           |
| [lxml](https://lxml.de/)                                                           | [4.9.2](https://pypi.org/project/lxml/4.9.2/)         | BSD License | lxml dev team   | Powerful and Pythonic XML processing library combining libxml2/libxslt with the ElementTree API. |
| [xmlschema](https://github.com/sissaschool/xmlschema)                              | [2.1.1](https://pypi.org/project/xmlschema/2.1.1/)    | MIT License | Davide Brunato  | An XML Schema validator and decoder                                                              |
<!--[[[end]]] (checksum: fcb09a28ebb367c6c8e39e55fa765b82)-->

### Indirect Dependencies

<!--[[[fill indirect_dependencies_table()]]]-->
| Name                                                      | Version                                               | License     | Author            | Description (from packaging data)                                |
|:----------------------------------------------------------|:------------------------------------------------------|:------------|:------------------|:-----------------------------------------------------------------|
| [elementpath](https://github.com/sissaschool/elementpath) | [3.0.2](https://pypi.org/project/elementpath/3.0.2/)  | MIT License | Davide Brunato    | XPath 1.0/2.0/3.0 parsers and selectors for ElementTree and lxml |
| [pyrsistent](https://github.com/tobgu/pyrsistent/)        | [0.19.2](https://pypi.org/project/pyrsistent/0.19.2/) | MIT License | Tobias Gustafsson | Persistent/Functional/Immutable data structures                  |
<!--[[[end]]] (checksum: 6e7bff0419762d7d7775dd0cf4f5dbd2)-->

## Dependency Tree(s)

JSON file with the complete package dependency tree info of: [the full dependency tree](package-dependency-tree.json)

### Rendered SVG

Base graphviz file in dot format: [Trees of the direct dependencies](package-dependency-tree.dot.txt)

<img src="./package-dependency-tree.svg" alt="Trees of the direct dependencies" title="Trees of the direct dependencies"/>

### Console Representation

<!--[[[fill dependency_tree_console_text()]]]-->
````console
jsonschema==4.17.3
  - attrs [required: >=17.4.0, installed: 22.2.0]
  - pyrsistent [required: >=0.14.0,!=0.17.2,!=0.17.1,!=0.17.0, installed: 0.19.2]
lxml==4.9.2
xmlschema==2.1.1
  - elementpath [required: >=3.0.0,<4.0.0, installed: 3.0.2]
````
<!--[[[end]]] (checksum: f94f8b29776df34f4b393462b9c8a86c)-->
